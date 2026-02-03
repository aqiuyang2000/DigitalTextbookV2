# FILE: settings_dialog_parts/_mixin_apply_logic.py
#
# 功能: 提供 apply_settings 方法，用于应用当前设置并发出信号。

class ApplyLogicMixin:
    """
    一个 Mixin 类，为 SettingsDialog 提供应用设置的核心逻辑。
    """

    def apply_settings(self):
        """
        应用当前在对话框中设置的选项。

        此方法会调用 self.save_settings() 将更改持久化，
        然后发出 self.settings_applied 信号，通知主窗口等其他组件
        设置已发生变化，以便它们可以刷新UI。
        """
        # self.save_settings 和 self.settings_applied
        # 将分别由 _mixin_save_settings 和 _base 提供。
        self.save_settings()
        self.settings_applied.emit()