# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_create_menus.py
#
# 功能: 提供 create_menus 方法，负责创建主窗口的菜单栏。

# --- Qt Imports ---
from PySide6.QtGui import QAction, QKeySequence


class CreateMenusMixin:
    """
    一个 Mixin 类，包含创建主窗口菜单栏的 create_menus 方法。
    """

    def create_menus(self):
        """
        初始化主窗口的菜单栏 (QMenuBar) 及其所有菜单和操作 (QAction)。
        """
        menu_bar = self.menuBar()

        # --- 1. 文件菜单 ("File") ---
        file_menu = menu_bar.addMenu("文件")

        new_action = QAction("新建项目", self)
        new_action.triggered.connect(self.new_project)

        open_action = QAction("打开项目", self)
        open_action.triggered.connect(self.open_project)

        add_pages_action = QAction("添加页面到项目...", self)
        add_pages_action.triggered.connect(self.open_image)

        save_action = QAction("保存项目", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_project)

        save_as_action = QAction("另存为...", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_project_as)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(add_pages_action)
        file_menu.addSeparator()
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)

        # --- 2. 编辑菜单 ("Edit") ---
        self.edit_menu = menu_bar.addMenu("编辑")

        # 撤销/重做动作的占位符，它们将在 update_ui_for_active_session 中被动态创建
        self.undo_action = QAction("撤销", self)
        self.redo_action = QAction("重做", self)
        self.undo_action.setShortcut(QKeySequence.Undo)
        self.redo_action.setShortcut(QKeySequence.Redo)
        self.edit_menu.addAction(self.undo_action)
        self.edit_menu.addAction(self.redo_action)
        self.edit_menu.addSeparator()

        copy_action = QAction("复制", self)
        copy_action.setShortcut(QKeySequence.Copy)
        paste_action = QAction("粘贴", self)
        paste_action.setShortcut(QKeySequence.Paste)
        delete_action = QAction("删除", self)
        delete_action.setShortcut(QKeySequence.Delete)

        copy_action.triggered.connect(self.copy_selected_hotspots)
        # 使用 lambda 确保在点击时动态获取当前 session 和鼠标位置
        paste_action.triggered.connect(
            lambda: self.active_session and self.paste_hotspots(
                self.active_session.viewer.mapToScene(
                    self.active_session.viewer.mapFromGlobal(self.cursor().pos())
                )
            )
        )
        delete_action.triggered.connect(self.delete_selected_hotspot)

        self.edit_menu.addAction(copy_action)
        self.edit_menu.addAction(paste_action)
        self.edit_menu.addAction(delete_action)
        self.edit_menu.addSeparator()

        preferences_action = QAction("首选项...", self)
        preferences_action.triggered.connect(self.open_settings_dialog)
        self.edit_menu.addAction(preferences_action)

        # --- 3. 视图菜单 ("View") ---
        view_menu = menu_bar.addMenu("视图")

        self.toggle_outline_action = QAction("显示提纲面板", self)
        self.toggle_outline_action.setCheckable(True)
        self.toggle_outline_action.triggered.connect(self.toggle_outline_panel)
        view_menu.addAction(self.toggle_outline_action)

        # --- 4. 导出菜单 ("Export") ---
        export_menu = menu_bar.addMenu("导出")

        self.export_flipbook_action = QAction("导出为双页画册", self)
        self.export_single_flipbook_action = QAction("导出为单页画册 (左右翻)", self)
        self.export_dynamic_page_action = QAction("导出为动态网页 (长滚动)", self)

        export_menu.addAction(self.export_flipbook_action)
        export_menu.addAction(self.export_single_flipbook_action)
        export_menu.addAction(self.export_dynamic_page_action)
        export_menu.addSeparator()

        self.export_all_action = QAction("一键导出所有格式", self)
        export_menu.addAction(self.export_all_action)
        export_menu.addSeparator()

        update_fragment_menu = export_menu.addMenu("更新单个页面片段")

        self.update_flipbook_fragment_action = QAction("更新双页画册片段", self)
        self.update_single_flipbook_fragment_action = QAction("更新单页画册片段", self)
        self.update_dynamic_fragment_action = QAction("更新长网页片段", self)

        update_fragment_menu.addAction(self.update_flipbook_fragment_action)
        update_fragment_menu.addAction(self.update_single_flipbook_fragment_action)
        update_fragment_menu.addAction(self.update_dynamic_fragment_action)

        # --- 5. 连接导出菜单项的信号 ---
        self.export_flipbook_action.triggered.connect(self.export_as_double_page_flipbook_wrapper)
        self.export_single_flipbook_action.triggered.connect(self.export_as_single_page_flipbook_wrapper)
        self.export_dynamic_page_action.triggered.connect(self.export_as_dynamic_page_wrapper)
        self.export_all_action.triggered.connect(self.export_all_formats)

        self.update_flipbook_fragment_action.triggered.connect(self.export_as_double_page_fragment_wrapper)
        self.update_single_flipbook_fragment_action.triggered.connect(self.export_as_single_flipbook_page_wrapper)
        self.update_dynamic_fragment_action.triggered.connect(self.export_to_html_wrapper)