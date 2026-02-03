# FILE: D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_setup_properties_panel.py

# --- Qt Imports ---
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit, QComboBox,
    QStackedWidget, QPushButton, QLabel
)


class SetupPropertiesPanelMixin:
    """
    一个 Mixin 类，包含构建热区属性编辑面板的 setup_properties_panel 方法。
    """

    def setup_properties_panel(self):
        """
        初始化和布局属性面板中的所有UI控件。
        """
        # --- 1. 基础属性表单 ---
        form_layout = QFormLayout()
        self.txt_id = QLineEdit();
        self.txt_id.setReadOnly(True);
        self.txt_id.setPlaceholderText("系统自动生成")
        form_layout.addRow("唯一ID:", self.txt_id)
        self.txt_description = QTextEdit();
        self.txt_description.setPlaceholderText("输入热区的内部说明或备注...");
        self.txt_description.setFixedHeight(60)
        form_layout.addRow("说明:", self.txt_description)
        self.txt_x = QLineEdit();
        self.txt_y = QLineEdit();
        self.txt_width = QLineEdit();
        self.txt_height = QLineEdit()
        form_layout.addRow("X:", self.txt_x);
        form_layout.addRow("Y:", self.txt_y);
        form_layout.addRow("宽:", self.txt_width);
        form_layout.addRow("高:", self.txt_height)
        self.type_combo = QComboBox();
        self.type_combo.addItems(["链接 (URL)", "本地文件"])
        form_layout.addRow("类型:", self.type_combo)
        self.icon_type_combo = QComboBox();
        self.icon_type_combo.addItems(["默认图标", "链接符号", "音频符号", "视频符号", "图片符号", "PDF符号"])
        self.icon_type_map = {"默认图标": "default", "链接符号": "link", "音频符号": "audio", "视频符号": "video",
                              "图片符号": "image", "PDF符号": "pdf"}
        self.icon_type_map_reverse = {v: k for k, v in self.icon_type_map.items()}
        form_layout.addRow("显示图标:", self.icon_type_combo)
        self.controls_layout.addLayout(form_layout)

        # --- 2. 链接类型详情 (使用 QStackedWidget) ---
        self.stacked_widget = QStackedWidget()
        self.controls_layout.addWidget(self.stacked_widget)

        # --- 通用宽高比设置 ---
        aspect_ratios = ["自由调整", "16:9 (宽屏)", "4:3 (标准)", "9:16 (竖屏)", "1:1 (方形)"]
        self.aspect_ratio_map = {"自由调整": "free", "16:9 (宽屏)": "16:9", "4:3 (标准)": "4:3", "9:16 (竖屏)": "9:16",
                                 "1:1 (方形)": "1:1"}
        self.aspect_ratio_map_reverse = {v: k for k, v in self.aspect_ratio_map.items()}

        # --- 2a. URL 链接页面 ---
        page_url = QWidget()
        url_layout = QFormLayout(page_url)
        self.txt_url = QLineEdit()
        self.combo_target = QComboBox();
        self.combo_target.addItems(["在新标签页中打开", "在当前页面打开", "在弹窗中打开", "嵌入页面"])
        self.target_map = {"在新标签页中打开": "_blank", "在当前页面打开": "_self", "在弹窗中打开": "popup",
                           "嵌入页面": "embed"}
        self.target_map_reverse = {v: k for k, v in self.target_map.items()}
        url_layout.addRow("链接:", self.txt_url)
        url_layout.addRow("打开方式:", self.combo_target)

        # --- *** 核心修改 1/2: 添加URL面板的宽高比下拉框 *** ---
        self.url_aspect_ratio_combo = QComboBox()
        self.url_aspect_ratio_combo.addItems(aspect_ratios)
        url_layout.addRow("宽高比:", self.url_aspect_ratio_combo)
        # --- *** 修改结束 *** ---

        self.lbl_url_popup_width = QLabel("弹窗/嵌入宽度:");
        self.txt_url_popup_width = QLineEdit("800")
        self.lbl_url_popup_height = QLabel("弹窗/嵌入高度:");
        self.txt_url_popup_height = QLineEdit("600")
        url_layout.addRow(self.lbl_url_popup_width, self.txt_url_popup_width)
        url_layout.addRow(self.lbl_url_popup_height, self.txt_url_popup_height)
        self.stacked_widget.addWidget(page_url)

        # --- 2b. 本地文件页面 ---
        page_file = QWidget()
        file_layout = QFormLayout(page_file)
        self.btn_upload = QPushButton("上传文件...");
        self.lbl_filename = QLabel("<i>未选择文件</i>");
        self.lbl_filename.setWordWrap(True)
        file_layout.addRow(self.btn_upload, self.lbl_filename)
        self.combo_file_display = QComboBox();
        self.combo_file_display.addItems(["弹窗", "嵌入"])
        file_layout.addRow("显示方式:", self.combo_file_display)

        # --- *** 核心修改 2/2: 添加文件面板的宽高比下拉框 *** ---
        self.file_aspect_ratio_combo = QComboBox()
        self.file_aspect_ratio_combo.addItems(aspect_ratios)
        file_layout.addRow("宽高比:", self.file_aspect_ratio_combo)
        # --- *** 修改结束 *** ---

        self.lbl_popup_width = QLabel("弹窗/嵌入宽度:");
        self.txt_popup_width = QLineEdit("800")
        self.lbl_popup_height = QLabel("弹窗/嵌入高度:");
        self.txt_popup_height = QLineEdit("600")
        file_layout.addRow(self.lbl_popup_width, self.txt_popup_width)
        file_layout.addRow(self.lbl_popup_height, self.txt_popup_height)
        self.stacked_widget.addWidget(page_file)