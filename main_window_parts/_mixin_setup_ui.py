# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_setup_ui.py
#
# 功能: 提供 setup_ui 方法，负责构建和布局主窗口的所有核心UI控件。

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QComboBox, QGroupBox, QFrame, QScrollArea, QCheckBox,
    # --- *** 核心修改 1/4: 导入新控件 *** ---
    QStackedWidget, QScrollBar
)
from PySide6.QtCore import Qt


class SetupUiMixin:
    """
    一个 Mixin 类，包含构建主窗口 UI 元素的 setup_ui 方法。
    """

    def setup_ui(self):
        """
        初始化和布局主窗口的所有UI控件。
        """
        # --- 1. 左侧提纲面板 ---
        self.main_splitter.addWidget(self.outline_widget)
        self.outline_widget.hide()

        # --- *** 核心修改 2/4: 重构中间主编辑区 *** ---
        # 1. 创建一个总容器
        self.editor_container = QWidget()
        editor_layout = QHBoxLayout(self.editor_container)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)

        # 2. 创建 QStackedWidget 用于显示页面
        self.page_stack = QStackedWidget()
        editor_layout.addWidget(self.page_stack)

        # 3. 创建独立的垂直滚动条用于翻页
        self.page_scrollbar = QScrollBar(Qt.Vertical)
        editor_layout.addWidget(self.page_scrollbar)

        # 4. 将总容器添加到主切分窗口
        self.main_splitter.addWidget(self.editor_container)

        # --- 3. 右侧控制与属性面板 ---
        # (这部分代码完全保持不变)
        controls_container = QWidget()
        self.controls_layout = QVBoxLayout(controls_container)
        self.controls_layout.setContentsMargins(8, 8, 8, 8)
        shape_layout = QHBoxLayout()
        shape_layout.addWidget(QLabel("绘制形状:"))
        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["Rectangle", "Ellipse"])
        shape_layout.addWidget(self.shape_combo)
        self.controls_layout.addLayout(shape_layout)
        self.info_label = QLabel("选中热区属性:")
        self.controls_layout.addWidget(self.info_label)
        self.setup_properties_panel()
        nav_layout = QHBoxLayout()
        self.btn_prev = QPushButton("上一页")
        self.btn_next = QPushButton("下一页")
        self.lbl_page_info = QLabel("0 / 0")
        self.txt_page_input = QLineEdit()
        self.txt_page_input.setFixedWidth(40)
        self.txt_page_input.setAlignment(Qt.AlignCenter)
        self.txt_page_input.setPlaceholderText("页码")
        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.lbl_page_info)
        nav_layout.addWidget(self.txt_page_input)
        nav_layout.addWidget(self.btn_next)
        self.btn_delete_page = QPushButton("删除本页")
        nav_layout.addWidget(self.btn_delete_page)
        self.controls_layout.addLayout(nav_layout)
        self.controls_layout.addSpacing(10)
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setFrameShadow(QFrame.Sunken)
        self.controls_layout.addWidget(separator1)
        self.controls_layout.addSpacing(10)
        export_group_box = QGroupBox("网页工具")
        export_layout = QVBoxLayout(export_group_box)
        self.btn_export_all = QPushButton("一键导出所有格式")
        export_layout.addWidget(self.btn_export_all)
        self.btn_preview = QPushButton("在浏览器中预览...")
        self.btn_preview.setEnabled(False)
        export_layout.addWidget(self.btn_preview)
        preview_options_layout = QHBoxLayout()
        preview_options_layout.setContentsMargins(0, 0, 0, 0)
        self.chk_preview_dual = QCheckBox("双页")
        self.chk_preview_dual.setChecked(True)
        self.chk_preview_dual.setToolTip("预览双页翻书效果 (index.html)")
        self.chk_preview_single = QCheckBox("单页")
        self.chk_preview_single.setChecked(True)
        self.chk_preview_single.setToolTip("预览单页翻书效果 (index_single.html)")
        self.chk_preview_scroll = QCheckBox("滚动")
        self.chk_preview_scroll.setChecked(True)
        self.chk_preview_scroll.setToolTip("预览长网页滚动效果 (index_scroll.html)")
        preview_options_layout.addWidget(self.chk_preview_dual)
        preview_options_layout.addWidget(self.chk_preview_single)
        preview_options_layout.addWidget(self.chk_preview_scroll)
        export_layout.addLayout(preview_options_layout)
        export_layout.addSpacing(8)
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        export_layout.addWidget(separator2)
        export_layout.addSpacing(8)
        self.btn_update_all_fragments = QPushButton("一键更新所有格式片段")
        export_layout.addWidget(self.btn_update_all_fragments)
        self.controls_layout.addWidget(export_group_box)
        data_tools_group_box = QGroupBox("数据工具")
        data_tools_layout = QVBoxLayout(data_tools_group_box)
        self.btn_batch_import = QPushButton("批量导入当页热区...")
        self.btn_export_hotspot_data = QPushButton("导出所有热区数据 (Excel)")
        self.btn_export_current_page_data = QPushButton("导出当前页数据 (Excel)")
        self.btn_pdf_toolbox = QPushButton("PDF 工具箱...")
        data_tools_layout.addWidget(self.btn_batch_import)
        data_tools_layout.addWidget(self.btn_export_hotspot_data)
        data_tools_layout.addWidget(self.btn_export_current_page_data)
        data_tools_layout.addSpacing(5)
        data_tools_layout.addWidget(self.btn_pdf_toolbox)
        self.btn_batch_scale = QPushButton("缩放选中项...")
        data_tools_layout.addWidget(self.btn_batch_scale)
        self.controls_layout.addWidget(data_tools_group_box)
        self.controls_layout.addStretch()
        self.main_splitter.addWidget(controls_container)

        # --- *** 核心修改 3/4 & 4/4: 移除旧代码，调整 Splitter 尺寸 *** ---
        # 原有的 QScrollArea 相关代码已全部移除
        self.main_splitter.setSizes([250, 800, 350])
        self.main_splitter.setStretchFactor(1, 1)