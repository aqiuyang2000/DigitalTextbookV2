# FILE: _command_batch_scale.py
#
# 功能: 定义 BatchScaleCommand，用于支持对多个热区进行批量缩放操作的撤销/重做。

from PySide6.QtGui import QUndoCommand
from PySide6.QtCore import QPointF


class BatchScaleCommand(QUndoCommand):
    """
    用于撤销/重做对多个热区进行批量缩放操作的命令。
    缩放操作始终保持每个热区的中心点不变。
    """

    def __init__(self, items: list, scale_factor: float, scale_mode: str, parent=None):
        """
        初始化批量缩放命令。

        Args:
            items (list): 需要缩放的 QGraphicsItem 列表。
            scale_factor (float): 缩放系数，例如 1.5 或 0.8。
            scale_mode (str): 缩放模式，'horizontal', 'vertical', 或 'overall'。
        """
        super().__init__("批量缩放热区", parent)
        self.items = list(items)
        self.scale_factor = scale_factor
        self.scale_mode = scale_mode

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
        重做或首次执行操作：应用缩放。
        """
        for state in self.old_states:
            item = state['item']
            old_pos = state['pos']
            old_size = state['size']

            # 1. 计算原始中心点 (相对于 item 自身的 (0,0) 点)
            center_x_local = old_size.width() / 2
            center_y_local = old_size.height() / 2

            # 将局部中心点映射到场景坐标
            center_scene = item.mapToScene(QPointF(center_x_local, center_y_local))

            # 2. 根据模式计算新的宽度和高度
            new_w, new_h = old_size.width(), old_size.height()
            if self.scale_mode == 'horizontal':
                new_w *= self.scale_factor
            elif self.scale_mode == 'vertical':
                new_h *= self.scale_factor
            elif self.scale_mode == 'overall':
                new_w *= self.scale_factor
                new_h *= self.scale_factor

            # 3. 计算新的左上角坐标，以保持场景中心点不变
            new_top_left_scene_x = center_scene.x() - (new_w / 2)
            new_top_left_scene_y = center_scene.y() - (new_h / 2)

            # 4. 应用新的位置和尺寸
            item.setPos(QPointF(new_top_left_scene_x, new_top_left_scene_y))
            item.setRect(0, 0, new_w, new_h)

        # 操作完成后发信号更新UI
        if self.items and self.items[0].scene():
            self.items[0].scene().selectionChanged.emit()