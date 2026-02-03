# FILE: _command_geometry_change.py
#
# 功能: 定义 GeometryChangeCommand，用于支持对单个热区几何属性修改的撤销/重做。

from PySide6.QtGui import QUndoCommand
from PySide6.QtCore import QSizeF


class GeometryChangeCommand(QUndoCommand):
    """
    用于撤销/重做对单个热区项几何属性（位置和尺寸）修改的命令。
    """

    def __init__(self, item, old_pos, old_size: QSizeF, new_pos, new_size: QSizeF, parent=None):
        """
        初始化几何属性修改命令。

        Args:
            item (QGraphicsItem): 被修改的热区项。
            old_pos (QPointF): 修改前的位置。
            old_size (QSizeF): 修改前的尺寸。
            new_pos (QPointF): 修改后的位置。
            new_size (QSizeF): 修改后的尺寸。
        """
        super().__init__("修改几何属性", parent)
        self.item = item
        self.old_pos = old_pos
        self.old_size = old_size
        self.new_pos = new_pos
        self.new_size = new_size

    def undo(self):
        """
        撤销操作：将 item 的位置和尺寸恢复为旧值。
        """
        self.item.setPos(self.old_pos)
        self.item.setRect(0, 0, self.old_size.width(), self.old_size.height())

        # 操作完成后发信号更新UI
        if self.item.scene():
            self.item.scene().selectionChanged.emit()

    def redo(self):
        """
        重做或首次执行操作：将 item 的位置和尺寸设置为新值。
        """
        self.item.setPos(self.new_pos)
        self.item.setRect(0, 0, self.new_size.width(), self.new_size.height())

        # 操作完成后发信号更新UI
        if self.item.scene():
            self.item.scene().selectionChanged.emit()