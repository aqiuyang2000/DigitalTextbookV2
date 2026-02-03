# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_set_active_session_by_viewer.py
#
# 功能: 提供 set_active_session_by_viewer 方法，通过 viewer 实例来设置活动会话。

# --- Project-specific Imports ---
# 导入 PhotoViewer 用于类型提示
from photo_viewer import PhotoViewer

class SetActiveSessionByViewerMixin:
    """
    一个 Mixin 类，包含一个辅助方法，用于通过 PhotoViewer 实例来设置活动会话。
    """
    def set_active_session_by_viewer(self, viewer_widget: PhotoViewer):
        """
        根据给定的 PhotoViewer 控件实例，查找其对应的索引并设置为活动会话。

        这是一个便利的辅助函数，主要用在 `handle_viewer_press` 中。
        当用户直接点击某个 viewer 时，我们只知道被点击的控件是哪个，
        此方法可以帮助我们从该控件反向找到它在 `self.viewer_widgets` 
        列表中的索引，然后调用核心的 `set_active_session` 方法。

        Args:
            viewer_widget (PhotoViewer): 用户点击的 PhotoViewer 实例。
        """
        # 检查给定的 viewer 是否在我们管理的 viewer 列表中
        if viewer_widget in self.viewer_widgets:
            # 如果是，获取它在列表中的索引
            index = self.viewer_widgets.index(viewer_widget)
            
            # 调用核心方法来设置活动会话
            self.set_active_session(index)