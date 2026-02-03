# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_go_to_page.py
#
# 功能: 提供 go_to_page 方法，用于从提纲跳转到指定页面。

class GoToPageMixin:
    """
    一个 Mixin 类，包含 go_to_page 槽函数，用于响应提纲项的点击。
    """
    def go_to_page(self, page_num: int):
        """
        跳转到指定页码的槽函数。

        此方法由 `OutlineEditorWidget` 的 `item_clicked` 信号触发。
        它接收一个页码（从1开始），将其转换为从0开始的索引，
        并调用 `set_active_session` 来执行跳转。

        Args:
            page_num (int): 要跳转到的目标页码 (基于 1 的索引)。
        """
        # 将基于 1 的页码转换为基于 0 的列表索引
        target_index = page_num - 1
        
        # 检查转换后的索引是否在当前 viewer 列表的有效范围内
        # (检查 viewer_widgets 比 sessions 更直接，因为它们是UI元素)
        if 0 <= target_index < len(self.viewer_widgets):
            # 如果有效，则调用核心方法设置活动会话
            # 默认情况下，这会滚动视图到目标页面
            self.set_active_session(target_index)