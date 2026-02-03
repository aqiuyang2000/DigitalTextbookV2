# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_set_active_session.py
#
# 功能: 提供 set_active_session 方法，用于切换当前的活动页面/会话。

# 移除了 QApplication 和 QTimer 的导入，因为不再需要复杂的滚动逻辑

class SetActiveSessionMixin:
    """
    一个 Mixin 类，包含设置当前活动编辑会话的核心方法。
    """

    def set_active_session(self, index: int, scroll_to_widget=True):
        """
        将指定索引的页面设置为当前的活动会话。

        此方法现在将 QStackedWidget 的当前页面切换到指定索引，
        并同步更新独立滚动条的值。

        Args:
            index (int): 要激活的页面在 self.sessions 列表中的索引。
            scroll_to_widget (bool): 在新模式下，此参数用于控制是否
                                     同步更新滚动条的值。默认为 True。
        """
        if not (0 <= index < len(self.sessions)):
            if not self.sessions:
                self.active_session_index = -1
                self.update_ui_for_active_session()
            return

        # --- *** 核心修改: 切换页面和滚动条 *** ---

        # 1. 取消上一个活动 viewer 的高亮状态 (逻辑保持不变)
        if 0 <= self.active_session_index < len(self.viewer_widgets):
            # 注意：旧的 viewer 可能已经被销毁（例如在撤销删除页面时）
            # 所以在访问前最好做个检查
            old_viewer = self.viewer_widgets[self.active_session_index]
            if old_viewer:
                old_viewer.set_active(False)

        # 2. 更新当前活动索引 (逻辑保持不变)
        self.active_session_index = index

        # 3. 切换 QStackedWidget 到新的页面索引
        if self.page_stack:
            self.page_stack.setCurrentIndex(index)

        # 4. 设置新 viewer 的状态 (逻辑基本不变)
        active_viewer = self.viewer_widgets[self.active_session_index]
        active_viewer.set_active(True)
        # fit_to_height() 仍然适用，确保图片在垂直方向上填满
        active_viewer.fit_to_height()

        # 5. (可选) 同步更新滚动条的值
        if scroll_to_widget and self.page_scrollbar:
            # a. 设置标志，防止 on_scroll 被触发，避免信号循环
            self._is_scrolling_programmatically = True

            # b. 设置滚动条的新值
            self.page_scrollbar.setValue(index)

            # c. 立即重置标志 (不再需要QTimer，因为值设置是即时的)
            self._is_scrolling_programmatically = False

        # 6. 更新提纲编辑器的默认页码 (逻辑保持不变)
        self.outline_widget.set_current_page_for_new_items(index + 1)

        # 7. 全面刷新UI (逻辑保持不变)
        self.update_ui_for_active_session()