# FILE: _command_delete.py
#
# 功能: 定义 DeleteCommand，用于支持删除热区操作的撤销/重做。

from PySide6.QtGui import QUndoCommand


class DeleteCommand(QUndoCommand):
    """
    用于撤销/重做删除一个或多个热区项操作的命令。
    """

    def __init__(self, scene, items: list, parent=None):
        """
        初始化删除命令。

        Args:
            scene (QGraphicsScene): 热区项所在的场景。
            items (list): 一个包含将要被删除的 QGraphicsItem 的列表。
        """
        super().__init__("删除热区", parent)
        self.scene = scene
        # 创建一个副本，以防原始列表在其他地方被修改
        self.items = list(items)

    def undo(self):
        """
        撤销操作：将所有已删除的项重新添加回场景中，并恢复其选中状态。
        """
        for item in self.items:
            self.scene.addItem(item)
            item.setSelected(True)

        # 发出信号以更新属性面板等UI
        if self.scene:
            self.scene.selectionChanged.emit()

    def redo(self):
        """
        重做或首次执行操作：从场景中移除所有指定的项。
        """
        for item in self.items:
            # 检查以确保该项仍在场景中（以防万一）
            if item.scene() == self.scene:
                self.scene.removeItem(item)

        # 发出信号以更新属性面板等UI
        if self.scene:
            self.scene.selectionChanged.emit()