# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_clear_project.py
#
# 功能: 提供 clear_project 方法，用于重置和清空当前工作区。

class ClearProjectMixin:
    """
    一个 Mixin 类，包含用于清空当前项目工作区的 clear_project 方法。
    """

    def clear_project(self, keep_path=False):
        """
        重置应用程序状态，清空所有项目相关的数据。
        """
        # --- *** 核心修改: 更新 UI 重置逻辑 *** ---
        # 1. 遍历 QStackedWidget 中的所有页面
        if self.page_stack:
            while self.page_stack.count() > 0:
                # 逐个移除 widget
                widget = self.page_stack.widget(0)
                self.page_stack.removeWidget(widget)
                # 安全地销毁它
                widget.deleteLater()

        # --- 2. 清空内部数据结构 (这部分保持不变) ---
        self.sessions.clear()
        self.viewer_widgets.clear()
        self.active_session_index = -1

        if not keep_path:
            self.project_path = None

        self.project_id = None
        self.clipboard = []
        self.outline_data = []

        # --- 3. 重置相关组件的状态 (这部分保持不变) ---
        self.outline_widget.populate_tree([])
        self.project_undo_stack.clear()

        # --- 4. 更新整个 UI 的状态以反映已清空 (这部分保持不变) ---
        self.update_ui_for_active_session()
        self.set_dirty(False)