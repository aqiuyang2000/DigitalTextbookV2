# FILE: _command_batch_items_geometry.py
#
# 功能: 定义 BatchItemsGeometryCommand，用于支持对多个热区进行部分或全部几何属性修改的撤销/重做。

from PySide6.QtGui import QUndoCommand
from PySide6.QtCore import QPointF


class BatchItemsGeometryCommand(QUndoCommand):
    """
    用于撤销/重做对多个热区进行部分或全部几何属性修改的命令。
    例如，只统一修改X坐标，或同时修改宽度和高度。
    """

    def __init__(self, items: list, geo_changes: dict, parent=None):
        """
        初始化批量修改几何属性命令。

        Args:
            items (list): 需要修改的 QGraphicsItem 列表。
            geo_changes (dict): 一个包含要修改属性的字典，
                                e.g., {'x': 100.0, 'h': 50.0}
        """
        super().__init__("批量修改几何属性", parent)
        self.items = list(items)
        self.geo_changes = geo_changes

        # 在执行前，保存每个 item 的原始完整几何状态
        self.old_states = []
        for item in self.items:
            self.old_states.append({
                'item': item,
                'pos': item.pos(),
                'size': item.rect().size()
            })

    def undo(self):
        """
        撤销操作：恢复所有 item 到它们的原始状态。
        """
        for state in self.old_states:
            item = state['item']
            item.setPos(state['pos'])
            item.setRect(0, 0, state['size'].width(), state['size'].height())

        # 操作完成后发信号更新UI
        if self.items and self.items[0].scene():
            self.items[0].scene().selectionChanged.emit()

    def redo(self):
        """
        重做或首次执行操作：应用新的几何属性。
        """
        for state in self.old_states:
            item = state['item']
            old_pos = state['pos']
            old_size = state['size']

            # 根据 geo_changes 字典计算新的位置和尺寸
            # 如果某个维度没有在字典中指定，则保留其原始值
            new_x = self.geo_changes.get('x', old_pos.x())
            new_y = self.geo_changes.get('y', old_pos.y())
            new_w = self.geo_changes.get('w', old_size.width())
            new_h = self.geo_changes.get('h', old_size.height())

            item.setPos(QPointF(new_x, new_y))
            item.setRect(0, 0, new_w, new_h)

        # 操作完成后发信号更新UI
        if self.items and self.items[0].scene():
            self.items[0].scene().selectionChanged.emit()