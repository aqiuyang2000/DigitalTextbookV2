# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_update_viewers_layout.py
#
# 功能: 提供 update_viewers_layout 方法，用于在窗口尺寸变化时重新计算页面布局。

class UpdateViewersLayoutMixin:
    """
    一个 Mixin 类，包含 update_viewers_layout 方法，用于响应式地调整页面视图布局。
    """

    def update_viewers_layout(self):
        """
        在 QStackedWidget 模式下，当窗口尺寸改变时，此方法被调用以
        确保当前显示的页面能正确地适应新的尺寸。

        它不再需要进行复杂的布局计算，因为 QStackedWidget 会自动处理
        其子控件的尺寸。我们只需要调用当前活动 viewer 的 fit_to_height
        方法来重新缩放其内部的图片即可。
        """

        # --- *** 核心修改: 简化布局更新逻辑 *** ---
        # 1. 检查是否存在活动会话和对应的 viewer
        if self.active_session and self.active_session.viewer:
            # 2. 调用 fit_to_height()。
            #    这将重新计算图片的缩放比例，使其高度与 viewer 的新高度匹配，
            #    从而实现了响应式的缩放效果。
            #    对于 QStackedWidget，我们使用 fit_to_height 更合适，
            #    因为它提供了更一致的垂直填充感。
            self.active_session.viewer.fit_to_height()

        # 原有的所有关于 QScrollArea 和 QVBoxLayout 的复杂计算都已移除。