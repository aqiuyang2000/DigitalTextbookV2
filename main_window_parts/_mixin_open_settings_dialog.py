# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_open_settings_dialog.py
#
# 功能: 提供 open_settings_dialog 方法，用于打开应用程序的首选项对话框。

# --- Project-specific Imports ---
from settings_dialog import SettingsDialog


class OpenSettingsDialogMixin:
    """
    一个 Mixin 类，包含用于打开设置对话框的 open_settings_dialog 方法。
    """

    def open_settings_dialog(self):
        """
        创建并显示首选项（SettingsDialog）对话框。

        这个方法处理了对话框的实例化，并将其 `settings_applied` 信号
        连接到主窗口的 `_on_settings_applied` 槽函数，以确保在设置
        被应用后，主窗口的UI能够得到相应的更新（例如，热区的颜色）。
        """
        # 创建 SettingsDialog 实例，父窗口为 self (主窗口)
        dialog = SettingsDialog(self)

        # 将对话框的 settings_applied 信号连接到主窗口的槽函数
        # 这样，当用户在对话框中点击 "Apply" 或 "OK" 时，
        # _on_settings_applied 方法就会被调用，以刷新UI。
        dialog.settings_applied.connect(self._on_settings_applied)

        # 以模态方式执行对话框，会阻塞主窗口直到对话框关闭
        dialog.exec()