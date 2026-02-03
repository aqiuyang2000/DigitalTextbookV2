# FILE: _command_data_change.py
#
# 功能: 定义 DataChangeCommand，用于支持对热区非几何属性（如链接、说明）修改的撤销/重做。

from PySide6.QtGui import QUndoCommand


class DataChangeCommand(QUndoCommand):
    """
    用于撤销/重做对单个热区项的数据属性（存储在 item.data(0) 中）修改的命令。
    """

    def __init__(self, item, old_data: dict, new_data: dict, parent=None):
        """
        初始化数据属性修改命令。

        Args:
            item (QGraphicsItem): 被修改的热区项。
            old_data (dict): 修改前的完整数据字典。
            new_data (dict): 修改后的完整数据字典。
        """
        super().__init__("修改数据属性", parent)
        self.item = item
        self.old_data = old_data
        self.new_data = new_data

    def undo(self):
        """
        撤销操作：将 item 的数据恢复为旧数据。
        """
        self.item.setData(0, self.old_data)

        # 操作完成后发信号更新UI
        if self.item.scene():
            self.item.scene().selectionChanged.emit()

    def redo(self):
        """
        重做或首次执行操作：将 item 的数据设置为新数据。
        """
        self.item.setData(0, self.new_data)

        # 操作完成后发信号更新UI
        if self.item.scene():
            self.item.scene().selectionChanged.emit()