# FILE: _command_delete_page.py
#
# 功能: 定义 DeletePageCommand，用于支持删除页面操作的撤销/重做。

from PySide6.QtGui import QUndoCommand


class DeletePageCommand(QUndoCommand):
    """
    用于撤销/重做删除页面操作的命令。
    """

    def __init__(self, main_window, session_to_delete, index: int, parent=None):
        """
        初始化删除页面命令。
        """
        super().__init__("删除页面", parent)
        self.main_window = main_window
        self.session = session_to_delete
        self.viewer = session_to_delete.viewer
        self.index = index

    def undo(self):
        """
        撤销操作：将删除的页面重新插入到原来的位置。
        """
        # --- *** 核心修改: 适配 QStackedWidget *** ---
        # 重新插入会话和视图到数据列表
        self.main_window.sessions.insert(self.index, self.session)
        self.main_window.viewer_widgets.insert(self.index, self.viewer)

        # 使用 page_stack.insertWidget 重新将 viewer 插入到 UI
        self.main_window.page_stack.insertWidget(self.index, self.viewer)

        # 激活恢复的页面
        self.main_window.set_active_session(self.index)

        self.main_window.set_dirty(True)
        # set_active_session 已经调用了 update_ui_for_active_session，这里无需重复

    def redo(self):
        """
        重做或首次执行操作：删除指定的页面。
        """
        if self.session not in self.main_window.sessions:
            return

        current_index = self.main_window.sessions.index(self.session)

        # --- *** 核心修改: 适配 QStackedWidget *** ---
        # 从数据列表中移除
        self.main_window.sessions.pop(current_index)
        self.main_window.viewer_widgets.pop(current_index)

        # 使用 page_stack.removeWidget 从 UI 中移除
        self.main_window.page_stack.removeWidget(self.viewer)

        # 注意：这里不再需要 setParent(None) 和 hide()，
        # removeWidget 已经处理了从布局中脱离的操作。

        # 计算新的活动页面索引
        new_index = current_index
        if new_index >= len(self.main_window.sessions):
            new_index = len(self.main_window.sessions) - 1

        # 移除后，更新UI状态
        if new_index >= 0:
            self.main_window.set_active_session(new_index)
        else:
            # 如果没有页面了，手动重置
            self.main_window.active_session_index = -1
            self.main_window.update_ui_for_active_session()

        self.main_window.set_dirty(True)