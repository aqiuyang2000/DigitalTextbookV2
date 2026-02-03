# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_handle_viewer_press.py
#
# 功能: 提供 handle_viewer_press 方法，用于处理对页面视图的点击事件。

# --- Qt Imports ---
from PySide6.QtGui import QMouseEvent

# --- Project-specific Imports ---
# 导入 PhotoViewer 用于类型提示和调用其原始方法
from photo_viewer import PhotoViewer

class HandleViewerPressMixin:
    """
    一个 Mixin 类，包含 handle_viewer_press 方法，用于在点击 PhotoViewer 时
    正确设置活动会话。
    """
    def handle_viewer_press(self, event: QMouseEvent, viewer: PhotoViewer):
        """
        在 PhotoViewer 的 mousePressEvent 之前被调用的自定义处理函数。

        当用户在滚动区域点击任何一个 PhotoViewer 时，这个方法会首先被触发。
        它的主要职责是检查被点击的 viewer 是否是当前活动的 viewer。如果不是，
        它会先调用 `set_active_session_by_viewer` 将其设为活动状态，然后
        再调用 PhotoViewer 原始的 `mousePressEvent` 来处理后续的绘图或
        选择操作。

        这种“拦截并处理”的模式确保了用户的操作总是作用于他们刚刚点击的
        那个页面上。

        Args:
            event (QMouseEvent): 鼠标点击事件对象。
            viewer (PhotoViewer): 被点击的 PhotoViewer 实例。
        """
        # 检查被点击的 viewer 是否是当前活动的 viewer
        if self.active_session.viewer != viewer:
            # 如果不是，则通过 viewer 实例来设置新的活动会话
            self.set_active_session_by_viewer(viewer)
        
        # 在完成会话切换后，调用 PhotoViewer 类原始的 mousePressEvent 方法，
        # 以确保其默认行为（如开始绘制热区）能够继续执行。
        PhotoViewer.mousePressEvent(viewer, event)