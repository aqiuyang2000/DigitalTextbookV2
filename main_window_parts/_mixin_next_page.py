# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_next_page.py
#
# 功能: 提供 next_page 方法，用于导航到下一页。

class NextPageMixin:
    """
    一个 Mixin 类，包含用于切换到下一页的 next_page 方法。
    """
    def next_page(self):
        """
        将活动会话切换到下一页的槽函数。

        它会检查当前活动页面是否不是最后一页，然后将活动会话索引加 1，
        并调用 `set_active_session`。
        """
        if self.active_session_index < len(self.sessions) - 1:
            self.set_active_session(self.active_session_index + 1)