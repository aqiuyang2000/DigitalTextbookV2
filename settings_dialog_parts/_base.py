# FILE: settings_dialog_parts/_base.py
#
# 功能: 包含 SettingsDialog 类的 __init__ 方法和核心属性。
#       负责创建所有UI控件、设置布局，并连接基础信号。

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QGroupBox, QCheckBox, QSpinBox,
    QDialogButtonBox, QComboBox, QDoubleSpinBox
)
from PySide6.QtCore import Signal


class SettingsDialogBase(QDialog):
    """
    SettingsDialog 的基础类。
    """
    settings_applied = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("首选项")
        self.setMinimumWidth(450)

        from settings_dialog import ColorPickerButton

        # --- 1. PDF 处理设置 ---
        pdf_group = QGroupBox("PDF 处理设置")
        pdf_layout = QFormLayout(pdf_group)
        self.pdf_dpi_combo = QComboBox()
        self.pdf_dpi_combo.addItem("标准 (150 DPI)", 150)
        self.pdf_dpi_combo.addItem("高清 (300 DPI)", 300)
        self.pdf_dpi_combo.addItem("超清 (600 DPI)", 600)
        pdf_layout.addRow("图片导出分辨率:", self.pdf_dpi_combo)

        # --- 2. 编辑器热区样式 ---
        editor_group = QGroupBox("编辑器热区样式")
        editor_layout = QFormLayout(editor_group)
        self.editor_fill_color_btn = ColorPickerButton()
        self.editor_border_color_btn = ColorPickerButton()
        self.editor_opacity_spin = QSpinBox()
        self.editor_opacity_spin.setRange(0, 100)
        self.editor_opacity_spin.setSuffix(" %")
        editor_layout.addRow("填充颜色:", self.editor_fill_color_btn)
        editor_layout.addRow("边框颜色:", self.editor_border_color_btn)
        editor_layout.addRow("填充不透明度:", self.editor_opacity_spin)

        # --- 3. 导出网页热区样式 ---
        export_group = QGroupBox("导出网页热区样式")
        export_layout = QFormLayout(export_group)
        self.export_fill_color_btn = ColorPickerButton()
        self.export_border_check = QCheckBox("显示边框")
        self.export_border_color_btn = ColorPickerButton()
        self.export_border_width_spin = QSpinBox()
        self.export_border_width_spin.setRange(0, 10)
        self.export_border_width_spin.setSuffix(" px")
        self.export_opacity_spin = QSpinBox()
        self.export_opacity_spin.setRange(0, 100)
        self.export_opacity_spin.setSuffix(" %")
        self.export_control_icon_size_spin = QSpinBox()
        self.export_control_icon_size_spin.setRange(12, 64)
        self.export_control_icon_size_spin.setSuffix(" px")
        self.export_control_icon_size_spin.setToolTip("设置导出后视频/Iframe播放器中关闭、播放、全屏等控制按钮的大小。")

        export_layout.addRow("高亮颜色:", self.export_fill_color_btn)
        export_layout.addRow("高亮不透明度:", self.export_opacity_spin)
        export_layout.addRow(self.export_border_check)
        export_layout.addRow("边框颜色:", self.export_border_color_btn)
        export_layout.addRow("边框宽度:", self.export_border_width_spin)
        export_layout.addRow("控件图标大小:", self.export_control_icon_size_spin)

        # --- *** 核心修改: 4. 提纲/目录设置 *** ---
        outline_group = QGroupBox("提纲/目录设置")
        outline_layout = QFormLayout(outline_group)

        # 位置选择
        self.outline_position_combo = QComboBox()
        self.outline_position_combo.addItem("左下角 (默认)", "bottom-left")
        self.outline_position_combo.addItem("左上角", "top-left")
        self.outline_position_combo.addItem("右下角", "bottom-right")
        self.outline_position_combo.addItem("右上角", "top-right")

        # 行为选择
        self.outline_behavior_combo = QComboBox()
        self.outline_behavior_combo.addItem("自动隐藏 (点击内容区关闭)", "auto_hide")
        self.outline_behavior_combo.addItem("固定显示 (点击内容区不关闭)", "fixed")

        # 字号设置
        self.outline_font_size_spin = QSpinBox()
        self.outline_font_size_spin.setRange(12, 36)
        self.outline_font_size_spin.setSuffix(" px")
        self.outline_font_size_spin.setValue(16)  # 默认值

        # 缩进设置
        self.outline_indent_spin = QDoubleSpinBox()
        self.outline_indent_spin.setRange(0.0, 5.0)
        self.outline_indent_spin.setSingleStep(0.1)
        self.outline_indent_spin.setSuffix(" em")
        self.outline_indent_spin.setValue(1.0)  # 默认值

        outline_layout.addRow("显示位置:", self.outline_position_combo)
        outline_layout.addRow("交互行为:", self.outline_behavior_combo)
        outline_layout.addRow("文字大小:", self.outline_font_size_spin)
        outline_layout.addRow("层级缩进:", self.outline_indent_spin)
        # --- *** 修改结束 *** ---

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply
        )

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(pdf_group)
        main_layout.addWidget(editor_group)
        main_layout.addWidget(export_group)
        main_layout.addWidget(outline_group)  # 添加新组到主布局
        main_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QDialogButtonBox.Apply).clicked.connect(self.apply_settings)
        self.export_border_check.stateChanged.connect(self.update_border_controls_state)

        self.load_settings()
        self.update_border_controls_state()