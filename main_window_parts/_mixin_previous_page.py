# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_previous_page.py
#
# 功能: 提供 previous_page 方法，用于导航到上一页。

class PreviousPageMixin:
    """
    一个 Mixin 类，包含用于切换到上一页的 previous_page 方法。
    """
    def previous_page(self):
        """
        将活动会话切换到上一页的槽函数。

        它会检查当前活动页面是否不是第一页，然后将活动会话索引减 1，
        并调用 `set_active_session`。
        """
        # 检查当前活动会话索引是否大于 0 (即不是第一页)
        if self.active_session_index > 0:
            # 如果条件满足，则调用核心方法来激活上一页
            self.set_active_session(self.active_session_index - 1)