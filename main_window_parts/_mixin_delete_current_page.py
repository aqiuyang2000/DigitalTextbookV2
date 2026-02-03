# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_delete_current_page.py
#
# 功能: 提供 delete_current_page 方法，用于删除当前活动页面。

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox

# --- Project-specific Imports ---
from commands import DeletePageCommand

class DeleteCurrentPageMixin:
    """
    一个 Mixin 类，包含用于删除当前活动页面的 delete_current_page 方法。
    """
    def delete_current_page(self):
        """
        处理删除当前活动页面的逻辑。

        此方法会弹出一个确认对话框，以防止用户误操作。如果用户确认，
        它不会直接执行删除操作，而是创建一个 `DeletePageCommand` 命令
        实例，并将其推送到项目级的撤销/重做栈 (`project_undo_stack`)。
        """
        if not self.active_session:
            return

        session_to_delete = self.active_session
        index_to_delete = self.active_session_index
        page_num = index_to_delete + 1

        reply = QMessageBox.question(
            self,
            "确认删除",
            f"您确定要永久删除第 {page_num} 页吗？\n此操作可通过 Ctrl+Z 撤销。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            command = DeletePageCommand(self, session_to_delete, index_to_delete)
            self.project_undo_stack.push(command)