# FILE: outline_editor_widget.py (已优化提纲添加逻辑)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeView, QMenu, QToolBar, QMessageBox,
    QInputDialog, QFileDialog, QHeaderView, QLabel, QLineEdit
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction, QIntValidator
from PySide6.QtCore import Qt, Signal, QModelIndex

from excel_processor import ExcelProcessor


class OutlineEditorWidget(QWidget):
    outline_changed = Signal(list)
    item_clicked = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(250)

        # --- 新增: 用于生成默认标题的计数器 ---
        self._new_item_counter = 1
        self._current_page_for_new_items = 1

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.toolbar = QToolBar()
        layout.addWidget(self.toolbar)

        self.tree_view = QTreeView()
        self.tree_view.setDragDropMode(QTreeView.InternalMove)
        self.tree_view.setSelectionMode(QTreeView.ExtendedSelection)
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setHeaderHidden(False)
        # 允许通过双击或按F2来编辑
        self.tree_view.setEditTriggers(QTreeView.DoubleClicked | QTreeView.EditKeyPressed)
        layout.addWidget(self.tree_view)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['提纲标题', '页码'])
        self.tree_view.setModel(self.model)

        header = self.tree_view.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self._setup_toolbar()
        self._connect_signals()

    def _setup_toolbar(self):
        self.add_toplevel_action = QAction("+ 添加", self)
        self.import_action = QAction("导入...", self)
        self.export_action = QAction("导出...", self)

        self.toolbar.addAction(self.add_toplevel_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.import_action)
        self.toolbar.addAction(self.export_action)

        self.toolbar.addSeparator()
        self.toolbar.addWidget(QLabel(" 调页:"))

        self.offset_edit = QLineEdit(self)
        self.offset_edit.setPlaceholderText("+/-数")
        self.offset_edit.setFixedWidth(80)
        self.offset_edit.setValidator(QIntValidator())
        self.toolbar.addWidget(self.offset_edit)

    def _connect_signals(self):
        self.tree_view.clicked.connect(self._on_item_clicked)
        self.tree_view.customContextMenuRequested.connect(self._open_context_menu)
        self.model.itemChanged.connect(self._on_model_changed)
        self.model.rowsMoved.connect(self._on_model_changed)
        self.model.rowsRemoved.connect(self._on_model_changed)
        self.model.rowsInserted.connect(self._on_model_changed)
        self.add_toplevel_action.triggered.connect(self._add_toplevel_item)
        self.import_action.triggered.connect(self._import_from_excel)
        self.export_action.triggered.connect(self._export_to_excel)
        self.offset_edit.returnPressed.connect(self._apply_page_offset)

    def _apply_page_offset(self):
        offset_text = self.offset_edit.text()
        if not offset_text: return
        try:
            offset = int(offset_text)
        except ValueError:
            self.offset_edit.clear(); return
        if offset == 0: return
        self.model.blockSignals(True)

        def recursive_offset(parent_item):
            for row in range(parent_item.rowCount()):
                page_item = parent_item.child(row, 1)
                if page_item:
                    try:
                        current_page = int(page_item.text())
                        new_page = max(1, current_page + offset)
                        page_item.setText(str(new_page))
                    except (ValueError, TypeError):
                        pass
                title_item = parent_item.child(row, 0)
                if title_item and title_item.hasChildren(): recursive_offset(title_item)

        recursive_offset(self.model.invisibleRootItem())
        self.model.blockSignals(False)
        self.outline_changed.emit(self.get_tree_data())
        self.offset_edit.clear();
        self.offset_edit.clearFocus()
        QMessageBox.information(self, "操作成功", f"所有提纲页码已整体调整 {offset:+} 页。")

    def set_current_page_for_new_items(self, page_num: int):
        self._current_page_for_new_items = page_num

    def populate_tree(self, outline_data: list):
        self.model.blockSignals(True)
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['提纲标题', '页码'])

        def _recursive_add(parent_item, nodes):
            for node in nodes:
                title_item = QStandardItem(node['title'])
                page_item = QStandardItem(str(node.get('page', 1)))
                parent_item.appendRow([title_item, page_item])
                if node.get('children'): _recursive_add(title_item, node['children'])

        _recursive_add(self.model.invisibleRootItem(), outline_data)
        self.model.blockSignals(False)
        self.tree_view.expandAll()
        self._new_item_counter = 1  # 重置计数器

    def get_tree_data(self) -> list:
        # ... 此方法保持不变 ...
        data = [];

        def _recursive_get(parent_item, data_list):
            for row in range(parent_item.rowCount()):
                title_item = parent_item.child(row, 0);
                page_item = parent_item.child(row, 1)
                if not title_item or not page_item: continue
                node = {'title': title_item.text(), 'page': int(page_item.text()) if page_item.text().isdigit() else 1,
                        'children': []}
                data_list.append(node)
                if title_item.hasChildren(): _recursive_get(title_item, node['children'])

        _recursive_get(self.model.invisibleRootItem(), data);
        return data

    def _on_item_clicked(self, index: QModelIndex):
        page_item = self.model.itemFromIndex(index.siblingAtColumn(1))
        if page_item and page_item.text().isdigit(): self.item_clicked.emit(int(page_item.text()))

    def _on_model_changed(self, *args):
        # ... 此方法保持不变 ...
        if args and isinstance(args[0], QStandardItem):
            item = args[0]
            if item.column() == 1:
                text = item.text()
                if not text.isdigit() or int(text) < 1:
                    QMessageBox.warning(self, "输入无效", "页码必须是一个大于等于1的整数。");
                    self.model.blockSignals(True)
                    item.setText("1");
                    self.model.blockSignals(False)
        self.outline_changed.emit(self.get_tree_data())

    def _get_selected_items(self) -> (list, list):
        indexes = self.tree_view.selectionModel().selectedRows()
        items = [self.model.itemFromIndex(index) for index in indexes]
        return items, indexes

    def _add_toplevel_item(self):
        self._add_item(self.model.invisibleRootItem())

    # --- *** 核心修改：重写 _add_item 方法，不再使用 QInputDialog *** ---
    def _add_item(self, parent_item, row=-1):
        """直接在模型中添加一个新项，并使其立即可编辑。"""
        # 生成默认标题
        title = f"新提纲 {self._new_item_counter}"
        self._new_item_counter += 1

        title_item = QStandardItem(title)
        page_item = QStandardItem(str(self._current_page_for_new_items))

        # 将新项添加到模型
        if row == -1:
            parent_item.appendRow([title_item, page_item])
        else:
            parent_item.insertRow(row, [title_item, page_item])

        # 展开父节点
        self.tree_view.expand(parent_item.index())

        # 获取新项的索引，并立即进入编辑模式
        new_item_index = title_item.index()
        self.tree_view.setCurrentIndex(new_item_index)  # 选中新项
        self.tree_view.edit(new_item_index)  # 开始编辑

    def _delete_items(self):
        # ... 此方法保持不变 ...
        items, indexes = self._get_selected_items()
        if not items: return
        reply = QMessageBox.question(self, "确认删除", f"确定要删除选中的 {len(items)} 个提纲项吗？\n此操作不可撤销。",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for index in sorted(indexes, key=lambda idx: idx.row(), reverse=True):
                (self.model.itemFromIndex(index.parent()) or self.model.invisibleRootItem()).removeRow(index.row())

    def _open_context_menu(self, position):
        menu = QMenu();
        items, indexes = self._get_selected_items()
        item = items[0] if items else None;
        index = indexes[0] if indexes else None
        add_toplevel_action = menu.addAction("+ 添加顶级提纲");
        menu.addSeparator()
        add_child_action = menu.addAction("添加子项");
        insert_above_action = menu.addAction("在上方插入")
        insert_below_action = menu.addAction("在下方插入");
        rename_action = menu.addAction("重命名")
        delete_action = menu.addAction("删除");
        is_single_selection = len(items) == 1
        add_child_action.setEnabled(is_single_selection);
        insert_above_action.setEnabled(is_single_selection)
        insert_below_action.setEnabled(is_single_selection);
        rename_action.setEnabled(is_single_selection)
        delete_action.setEnabled(bool(items));
        action = menu.exec(self.tree_view.viewport().mapToGlobal(position))

        if action == add_toplevel_action: self._add_toplevel_item(); return
        if not action or not item: return

        if action == add_child_action:
            self._add_item(parent_item=item)
        elif action == insert_above_action:
            self._add_item(parent_item=(item.parent() or self.model.invisibleRootItem()), row=index.row())
        elif action == insert_below_action:
            self._add_item(parent_item=(item.parent() or self.model.invisibleRootItem()), row=index.row() + 1)
        elif action == rename_action:
            self.tree_view.edit(index.siblingAtColumn(0))  # 直接进入编辑模式
        elif action == delete_action:
            self._delete_items()

    def _import_from_excel(self):
        # ... 此方法保持不变 ...
        path, _ = QFileDialog.getOpenFileName(self, "从 Excel 导入提纲", "", "Excel 文件 (*.xlsx)")
        if not path: return
        reply = QMessageBox.question(self, "确认导入", "导入将覆盖当前所有提纲，确定要继续吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                data = ExcelProcessor.import_from_excel(path);
                self.populate_tree(data)
                self.outline_changed.emit(self.get_tree_data())
            except Exception as e:
                QMessageBox.critical(self, "导入失败", f"无法解析Excel文件：\n{e}")

    def _export_to_excel(self):
        # ... 此方法保持不变 ...
        path, _ = QFileDialog.getSaveFileName(self, "导出提纲到 Excel", "outline.xlsx", "Excel 文件 (*.xlsx)")
        if not path: return
        try:
            data = self.get_tree_data();
            ExcelProcessor.export_to_excel(data, path)
            QMessageBox.information(self, "导出成功", f"提纲已成功导出到:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"无法写入Excel文件：\n{e}")