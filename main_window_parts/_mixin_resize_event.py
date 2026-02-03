# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_resize_event.py
#
# 功能: 提供 resizeEvent 事件处理器，用于在窗口尺寸改变时触发布局更新。

# --- Qt Imports ---
from PySide6.QtCore import QTimer
from PySide6.QtGui import QResizeEvent

class ResizeEventMixin:
    """
    一个 Mixin 类，重写了 QMainWindow 的 resizeEvent 方法。
    """
    def resizeEvent(self, event: QResizeEvent):
        """
        当主窗口大小发生改变时自动调用的事件处理器。

        为了避免在用户拖拽调整窗口大小时过于频繁地调用布局更新函数
        (这可能会导致卡顿)，这里使用了一个单次触发的 QTimer (防抖)。
        只有在窗口停止调整大小 50 毫秒后，才会真正执行
        `self.update_viewers_layout()`。

        Args:
            event (QResizeEvent): 包含了新旧尺寸信息的事件对象。
        """
        # 首先，调用父类的 resizeEvent 实现，以确保所有基础处理都已完成
        super().resizeEvent(event)
        
        # --- 防抖 (debounce) 逻辑 ---
        # 检查防抖计时器是否存在，如果不存在则创建它
        if not hasattr(self, '_resize_timer'):
            self._resize_timer = QTimer(self)
            self._resize_timer.setSingleShot(True)  # 设置为单次触发模式
            # 连接计时器的 timeout 信号到实际的布局更新方法
            self._resize_timer.timeout.connect(self.update_viewers_layout)
        
        # (重新)启动计时器。如果在 50 毫秒内再次触发 resizeEvent，
        # 旧的计时会被取消，新的计时会开始。
        self._resize_timer.start(50)