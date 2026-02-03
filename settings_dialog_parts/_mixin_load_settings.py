# FILE: settings_dialog_parts/_mixin_load_settings.py
#
# 功能: 提供 load_settings 方法，用于从 QSettings 加载配置并填充UI。

from PySide6.QtGui import QColor
from PySide6.QtCore import QSettings, Qt


class LoadSettingsMixin:
    """
    一个 Mixin 类，为 SettingsDialog 提供从持久化存储中加载设置的功能。
    """

    def load_settings(self):
        """
        从 QSettings 中读取所有配置项，并用这些值来设置UI控件的初始状态。
        """
        settings = QSettings("MyCompany", "HotspotEditor")

        # --- 1. 加载 PDF 设置 ---
        saved_dpi = settings.value("pdf/resolution_dpi", 150, type=int)
        index_to_set = self.pdf_dpi_combo.findData(saved_dpi)
        if index_to_set != -1:
            self.pdf_dpi_combo.setCurrentIndex(index_to_set)
        else:
            self.pdf_dpi_combo.setCurrentIndex(0)

        # --- 2. 加载编辑器设置 ---
        self.editor_fill_color_btn.setColor(settings.value("editor/fill_color", QColor(Qt.blue)))
        self.editor_border_color_btn.setColor(settings.value("editor/border_color", QColor(Qt.blue)))
        self.editor_opacity_spin.setValue(settings.value("editor/opacity_percent", 15, type=int))

        # --- 3. 加载导出设置 ---
        self.export_fill_color_btn.setColor(settings.value("export/fill_color", QColor(64, 158, 255)))
        self.export_opacity_spin.setValue(settings.value("export/opacity_percent", 30, type=int))
        self.export_border_check.setChecked(settings.value("export/has_border", True, type=bool))
        self.export_border_color_btn.setColor(settings.value("export/border_color", QColor(64, 158, 255)))
        self.export_border_width_spin.setValue(settings.value("export/border_width", 1, type=int))
        self.export_control_icon_size_spin.setValue(settings.value("export/control_icon_size", 24, type=int))

        # --- *** 核心修改: 4. 加载提纲/目录设置 *** ---

        # 位置 (默认: 左下角 bottom-left)
        outline_pos = settings.value("outline/position", "bottom-left")
        pos_index = self.outline_position_combo.findData(outline_pos)
        if pos_index != -1:
            self.outline_position_combo.setCurrentIndex(pos_index)
        else:
            self.outline_position_combo.setCurrentIndex(0)

        # 行为 (默认: 自动隐藏 auto_hide)
        outline_behavior = settings.value("outline/behavior", "auto_hide")
        behav_index = self.outline_behavior_combo.findData(outline_behavior)
        if behav_index != -1:
            self.outline_behavior_combo.setCurrentIndex(behav_index)
        else:
            self.outline_behavior_combo.setCurrentIndex(0)

        # 字号 (默认: 16px)
        self.outline_font_size_spin.setValue(settings.value("outline/font_size", 16, type=int))

        # 缩进 (默认: 1.0em)
        # 注意: QSettings 读取 float 有时需要显式转换，或者提供 float 类型的默认值
        self.outline_indent_spin.setValue(settings.value("outline/indent", 1.0, type=float))
        # --- *** 修改结束 *** ---