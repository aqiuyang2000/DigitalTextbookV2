# FILE: D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_update_popup_size_visibility.py (FIXED)

class UpdatePopupSizeVisibilityMixin:
    """
    一个 Mixin 类，包含根据文件显示方式更新弹窗尺寸控件可见性的方法。
    """

    def update_popup_size_visibility(self):
        """
        检查“显示方式”下拉框的当前选项，并据此显示或隐藏尺寸相关设置。
        """
        if not hasattr(self, 'combo_file_display') or self.combo_file_display is None:
            return

        # --- *** 核心修复: 当选择“弹窗”或“嵌入”时，都显示尺寸设置 *** ---
        # 因为这两个选项都需要用户输入尺寸
        is_size_setting_visible = self.combo_file_display.currentText() in ["弹窗", "嵌入"]
        # --- *** 修复结束 *** ---

        # 宽高比下拉框也应该遵循同样的逻辑
        if hasattr(self, 'file_aspect_ratio_combo'):
            self.file_aspect_ratio_combo.setVisible(is_size_setting_visible)

        popup_widgets = [
            self.lbl_popup_width,
            self.txt_popup_width,
            self.lbl_popup_height,
            self.txt_popup_height
        ]

        for widget in popup_widgets:
            if widget:
                widget.setVisible(is_size_setting_visible)

    def update_url_popup_size_visibility(self):
        """
        检查URL“打开方式”下拉框，如果选择“弹窗”或“嵌入”，则显示尺寸设置。
        """
        if not hasattr(self, 'combo_target') or self.combo_target is None:
            return

        # --- *** 核心修复: 当选择“弹窗”或“嵌入”时，都显示尺寸设置 *** ---
        is_size_setting_visible = self.combo_target.currentText() in ["在弹窗中打开", "嵌入页面"]
        # --- *** 修复结束 *** ---

        # 宽高比下拉框也应该遵循同样的逻辑
        if hasattr(self, 'url_aspect_ratio_combo'):
            self.url_aspect_ratio_combo.setVisible(is_size_setting_visible)

        url_popup_widgets = [
            self.lbl_url_popup_width,
            self.txt_url_popup_width,
            self.lbl_url_popup_height,
            self.txt_url_popup_height
        ]

        for widget in url_popup_widgets:
            if widget:
                widget.setVisible(is_size_setting_visible)