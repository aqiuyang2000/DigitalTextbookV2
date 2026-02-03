# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_on_settings_applied.py
#
# 功能: 提供 _on_settings_applied 槽函数，用于在首选项更改后更新UI。

# --- Project-specific Imports ---
# 导入 AbstractResizableItem 用于类型检查
from graphics_items import AbstractResizableItem


class OnSettingsAppliedMixin:
    """
    一个 Mixin 类，包含 _on_settings_applied 槽函数。
    """

    def _on_settings_applied(self):
        """
        在设置对话框中的设置被应用（Apply/OK）后调用的槽函数。

        此方法会重新获取最新的画笔和画刷设置，并遍历当前所有会话
        中的所有热区项，将新的样式应用给它们，最后刷新视图。
        """
        # 从 QSettings 中获取更新后的画笔和画刷
        new_pen = self.get_hotspot_pen()
        new_brush = self.get_hotspot_brush()

        # 遍历所有已加载的会话 (pages)
        for session in self.sessions:
            # 遍历当前会话场景中的所有图形项
            for item in session.scene.items():
                # 检查该项是否是我们的自定义热区项
                if isinstance(item, AbstractResizableItem):
                    # 应用新的画笔和画刷
                    item.setPen(new_pen)
                    item.setBrush(new_brush)

        # 如果存在活动的会话和视图，强制重绘视图以立即显示更改
        if self.active_session and self.active_session.viewer:
            self.active_session.viewer.viewport().update()