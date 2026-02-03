# FILE: settings_dialog_parts/_mixin_save_settings.py
#
# 功能: 提供 save_settings 方法，用于将UI控件的当前状态保存到 QSettings。

from PySide6.QtCore import QSettings

class SaveSettingsMixin:
    """
    一个 Mixin 类，为 SettingsDialog 提供将当前设置保存到持久化存储的功能。
    """

    def save_settings(self):
        """
        读取所有UI控件的当前值，并将它们写入到 QSettings 中进行持久化保存。
        """
        settings = QSettings("MyCompany", "HotspotEditor")

        # --- 1. 保存 PDF 设置 ---
        selected_dpi = self.pdf_dpi_combo.currentData()
        settings.setValue("pdf/resolution_dpi", selected_dpi)

        # --- 2. 保存编辑器设置 ---
        settings.setValue("editor/fill_color", self.editor_fill_color_btn.color())
        settings.setValue("editor/border_color", self.editor_border_color_btn.color())
        settings.setValue("editor/opacity_percent", self.editor_opacity_spin.value())

        # --- 3. 保存导出设置 ---
        settings.setValue("export/fill_color", self.export_fill_color_btn.color())
        settings.setValue("export/opacity_percent", self.export_opacity_spin.value())
        settings.setValue("export/has_border", self.export_border_check.isChecked())
        settings.setValue("export/border_color", self.export_border_color_btn.color())
        settings.setValue("export/border_width", self.export_border_width_spin.value())
        settings.setValue("export/control_icon_size", self.export_control_icon_size_spin.value())

        # --- *** 核心修改: 4. 保存提纲/目录设置 *** ---
        settings.setValue("outline/position", self.outline_position_combo.currentData())
        settings.setValue("outline/behavior", self.outline_behavior_combo.currentData())
        settings.setValue("outline/font_size", self.outline_font_size_spin.value())
        settings.setValue("outline/indent", self.outline_indent_spin.value())
        # --- *** 修改结束 *** ---