# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_update_ui_for_active_session.py
#
# 功能: 提供 update_ui_for_active_session 方法，用于根据当前程序状态刷新整个UI。

from PySide6.QtGui import QKeySequence


class UpdateUiForActiveSessionMixin:
    """
    一个 Mixin 类，包含核心的 UI 状态更新方法 update_ui_for_active_session。
    """

    def update_ui_for_active_session(self):
        """
        根据当前活动会话和项目状态，全面更新UI控件的启用/禁用状态和文本内容。
        """
        # --- 1. 动态更新撤销/重做菜单 (这部分逻辑保持不变) ---
        if hasattr(self, 'undo_action') and self.undo_action:
            self.edit_menu.removeAction(self.undo_action)
            self.undo_action.deleteLater()
        if hasattr(self, 'redo_action') and self.redo_action:
            self.edit_menu.removeAction(self.redo_action)
            self.redo_action.deleteLater()
        page_stack = self.active_session.undo_stack if self.active_session else None
        page_stack_has_actions = page_stack and (page_stack.canUndo() or page_stack.canRedo())
        primary_stack = page_stack if page_stack_has_actions else self.project_undo_stack
        self.undo_action = primary_stack.createUndoAction(self, "撤销")
        self.redo_action = primary_stack.createRedoAction(self, "重做")
        self.undo_action.setShortcut(QKeySequence.Undo)
        self.redo_action.setShortcut(QKeySequence.Redo)
        actions = self.edit_menu.actions()
        separator = next((action for action in actions if action.isSeparator()), None)
        if separator:
            self.edit_menu.insertAction(separator, self.redo_action)
            self.edit_menu.insertAction(self.redo_action, self.undo_action)
        else:
            first_action = actions[0] if actions else None
            self.edit_menu.insertAction(first_action, self.redo_action)
            self.edit_menu.insertAction(self.redo_action, self.undo_action)

        # --- 2. 根据状态更新按钮和菜单项的可用性 (这部分逻辑保持不变) ---
        has_active_session = self.active_session is not None
        page_count = len(self.sessions)
        is_project_open = self.project_path is not None
        self.btn_export_all.setEnabled(page_count > 0 and is_project_open)
        # ... (所有按钮和菜单项的 setEnabled 调用都保持不变) ...
        self.export_flipbook_action.setEnabled(page_count > 0 and is_project_open)
        self.export_single_flipbook_action.setEnabled(page_count > 0 and is_project_open)
        self.export_dynamic_page_action.setEnabled(page_count > 0 and is_project_open)
        self.export_all_action.setEnabled(page_count > 0 and is_project_open)
        self.update_flipbook_fragment_action.setEnabled(has_active_session and is_project_open)
        self.update_single_flipbook_fragment_action.setEnabled(has_active_session and is_project_open)
        self.update_dynamic_fragment_action.setEnabled(has_active_session and is_project_open)
        self.btn_update_all_fragments.setEnabled(has_active_session and is_project_open)
        self.btn_export_hotspot_data.setEnabled(page_count > 0 and is_project_open)
        self.btn_export_current_page_data.setEnabled(has_active_session and is_project_open)
        self.btn_batch_import.setEnabled(has_active_session and is_project_open)
        self.btn_pdf_toolbox.setEnabled(has_active_session and is_project_open)
        self.btn_prev.setEnabled(self.active_session_index > 0)
        self.btn_next.setEnabled(self.active_session_index < page_count - 1)
        self.btn_delete_page.setEnabled(has_active_session)

        # --- 3. 更新标签和文本框内容 (这部分逻辑保持不变) ---
        self.lbl_page_info.setText(f"{self.active_session_index + 1} / {page_count}" if has_active_session else "0 / 0")
        self.txt_page_input.setEnabled(has_active_session)
        if has_active_session:
            self.txt_page_input.blockSignals(True)
            self.txt_page_input.setText(str(self.active_session_index + 1))
            self.txt_page_input.blockSignals(False)
        else:
            self.txt_page_input.clear()

        # --- *** 核心修改: 更新滚动条的状态 *** ---
        if self.page_scrollbar:
            # 如果没有页面或只有一页，禁用滚动条
            self.page_scrollbar.setEnabled(page_count > 1)
            # 设置滚动条的范围。最小值是0，最大值是最后一页的索引。
            self.page_scrollbar.setMinimum(0)
            self.page_scrollbar.setMaximum(max(0, page_count - 1))
            # 设置步长，pageStep用于点击空白区域，singleStep用于点击箭头
            self.page_scrollbar.setPageStep(1)
            self.page_scrollbar.setSingleStep(1)

            # 确保滚动条的当前值与活动页面索引同步
            if has_active_session:
                # 临时阻塞信号，防止 setValue 触发 on_scroll
                self.page_scrollbar.blockSignals(True)
                self.page_scrollbar.setValue(self.active_session_index)
                self.page_scrollbar.blockSignals(False)
            else:
                self.page_scrollbar.setValue(0)

        # --- 4. 调用其他更新方法 (这部分逻辑保持不变) ---
        self.update_window_title(dirty=self.is_dirty)
        self.update_hotspot_info()