# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_on_scroll.py
#
# 功能: 提供 on_scroll 槽函数，用于在用户滚动翻页条时更新活动会话。

class OnScrollMixin:
    """
    一个 Mixin 类，包含 on_scroll 槽函数，用于处理页面滚动事件。
    """
    def on_scroll(self, value: int):
        """
        当独立的翻页滚动条值改变时被调用的槽函数。

        在新的 QStackedWidget 布局下，滚动条的值直接对应于页面的索引。
        此方法简单地将这个值作为新的页面索引，并调用 set_active_session
        来切换页面。

        它依然使用 _is_scrolling_programmatically 标志来防止在由代码
        （如点击按钮）触发页面切换时，再次错误地触发此逻辑。

        Args:
            value (int): 滚动条的当前值，即目标页面的索引 (0-based)。
        """
        # 如果滚动是由程序代码（如 set_active_session）触发的，则忽略此事件
        if self._is_scrolling_programmatically:
            return

        # 滚动条的值 (value) 现在直接就是目标页面的索引
        target_index = value

        # 检查索引是否有效，并且是否与当前的活动索引不同
        if 0 <= target_index < len(self.sessions) and self.active_session_index != target_index:
            # 如果是，则设置新的活动会话。
            # scroll_to_widget=False 避免了再次触发滚动条值的改变，防止循环。
            self.set_active_session(target_index, scroll_to_widget=False)