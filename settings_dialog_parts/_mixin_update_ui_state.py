# FILE: settings_dialog_parts/_mixin_update_ui_state.py
#
# 功能: 提供 update_border_controls_state 方法，用于动态更新UI控件的启用状态。

class UpdateUiStateMixin:
    """
    一个 Mixin 类，为 SettingsDialog 提供根据复选框状态动态更新UI的方法。
    """

    def update_border_controls_state(self):
        """
        根据“显示边框”复选框 (self.export_border_check) 的状态，
        来启用或禁用与边框相关的控件（颜色选择器和宽度输入框）。
        """
        # self.export_border_check, self.export_border_color_btn,
        # 和 self.export_border_width_spin 都在 _base 中创建。
        enabled = self.export_border_check.isChecked()
        self.export_border_color_btn.setEnabled(enabled)
        self.export_border_width_spin.setEnabled(enabled)