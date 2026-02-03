# FILE: settings_dialog_parts/_mixin_events.py
#
# 功能: 提供 accept 方法的重写实现，以确保在点击 "OK" 时应用设置。

class DialogEventsMixin:
    """
    一个 Mixin 类，为 SettingsDialog 重写标准的对话框事件处理。
    """

    def accept(self):
        """
        重写 QDialog 的 accept 方法。

        当用户点击 "OK" 按钮时，此方法被调用。它首先调用
        self.apply_settings() 来确保所有更改都被保存和应用，
        然后才调用父类的 accept() 方法来关闭对话框。
        """
        # self.apply_settings 将由 _mixin_apply_logic 提供
        self.apply_settings()
        super().accept()