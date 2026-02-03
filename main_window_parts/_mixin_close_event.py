# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_close_event.py
#
# 功能: 提供 closeEvent 事件处理器，用于在关闭窗口前处理未保存的更改。

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QCloseEvent

class CloseEventMixin:
    """
    一个 Mixin 类，重写了 QMainWindow 的 closeEvent 方法。
    """
    def closeEvent(self, event: QCloseEvent):
        """
        当用户尝试关闭主窗口时自动调用的事件处理器。

        此方法会检查 `self.is_dirty` 标志。如果有未保存的更改，
        它会弹出一个对话框，询问用户是保存、丢弃更改还是取消关闭操作。
        根据用户的选择来接受或忽略关闭事件。

        Args:
            event (QCloseEvent): 包含了关闭事件信息的对象。可以通过调用
                                 event.accept() 或 event.ignore() 来控制
                                 窗口是否真的关闭。
        """
        if self.is_dirty:
            # 如果项目有未保存的更改，则弹出确认对话框
            reply = QMessageBox.question(
                self, 
                "退出前保存", 
                "项目有未保存的更改，您想保存吗？",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save  # 默认选中的按钮
            )

            if reply == QMessageBox.Save:
                # 用户选择“保存”
                # 尝试保存项目。如果保存成功，则接受关闭事件。
                # 如果用户在保存对话框中点击了取消，save_project() 会返回 False，
                # 此时应忽略关闭事件，让用户留在应用中。
                if self.save_project():
                    event.accept()
                else:
                    event.ignore()
            elif reply == QMessageBox.Discard:
                # 用户选择“丢弃”，直接接受关闭事件，不保存
                event.accept()
            else: # reply == QMessageBox.Cancel
                # 用户选择“取消”，忽略关闭事件，窗口保持打开
                event.ignore()
        else:
            # 如果没有未保存的更改，直接接受关闭事件
            event.accept()