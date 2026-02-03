# FILE: _mixin_interaction_events.py (全新优化版)
#
# 功能: 统一提供所有用户交互事件的实现，并修复了所有已知问题。

from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QCursor
from PySide6.QtCore import Qt, QRectF, QPointF


class InteractionEventsMixin:
    """
    一个统一的 Mixin 类，为 AbstractResizableItem 提供所有交互事件的处理逻辑。
    """

    # --- 1. 状态变化与移动约束 ---
    def itemChange(self, change, value):
        # (满足优化点 1) 处理选中状态，用于显示/隐藏控制柄
        if change == QGraphicsRectItem.ItemSelectedChange:
            for handle in self.handles:
                handle.setVisible(value)
            if value:
                self.updateForViewTransform()

        # (满足优化点 2) 处理位置即将变化，用于移动时的边界约束
        elif change == QGraphicsRectItem.ItemPositionChange and self.scene():
            # 关键修复：如果当前正在进行缩放操作，则不应用此处的移动约束，
            # 因为 mouseMoveEvent 会处理缩放时的边界，这可以防止逻辑冲突。
            if self.is_resizing:
                return super().itemChange(change, value)

            new_pos = value
            if self.bounds:
                new_rect = QRectF(new_pos, self.rect().size())
                if new_rect.left() < self.bounds.left():
                    new_pos.setX(self.bounds.left())
                elif new_rect.right() > self.bounds.right():
                    new_pos.setX(self.bounds.right() - self.rect().width())

                if new_rect.top() < self.bounds.top():
                    new_pos.setY(self.bounds.top())
                elif new_rect.bottom() > self.bounds.bottom():
                    new_pos.setY(self.bounds.bottom() - self.rect().height())
            return new_pos

        # 当项移动完成后，发出信号通知UI更新。
        elif change == QGraphicsRectItem.ItemPositionHasChanged:
            if self.scene() and hasattr(self.scene(), 'selectionChanged'):
                self.scene().selectionChanged.emit()

        return super().itemChange(change, value)

    # --- 2. 悬停事件 ---
    def hoverMoveEvent(self, event):
        handle_at_pos = -1
        for i, handle in enumerate(self.handles):
            if handle.sceneBoundingRect().contains(event.scenePos()):
                handle_at_pos = i
                break

        if handle_at_pos != -1:
            if handle_at_pos in [0, 2]:
                self.setCursor(QCursor(Qt.SizeFDiagCursor))
            else:
                self.setCursor(QCursor(Qt.SizeBDiagCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

        super().hoverMoveEvent(event)

    # --- 3. 鼠标点击、拖拽与缩放事件 ---
    def mousePressEvent(self, event):
        self.is_resizing = False
        # (满足优化点 1) 检查是否点击在控制柄上
        for i, handle in enumerate(self.handles):
            if handle.sceneBoundingRect().contains(event.scenePos()):
                self.current_handle = i
                self.is_resizing = True
                self.mouse_press_rect = self.rect()
                break

        if not self.is_resizing:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_resizing:
            self.prepareGeometryChange()
            mouse_pos = QPointF(event.scenePos())

            # (满足优化点 2) 缩放时的边界约束
            if self.bounds:
                mouse_pos.setX(max(self.bounds.left(), min(mouse_pos.x(), self.bounds.right())))
                mouse_pos.setY(max(self.bounds.top(), min(mouse_pos.y(), self.bounds.bottom())))

            # 根据拖动的控制柄确定锚点
            if self.current_handle == 0: anchor = self.mapToScene(self.mouse_press_rect.bottomRight())
            elif self.current_handle == 1: anchor = self.mapToScene(self.mouse_press_rect.bottomLeft())
            elif self.current_handle == 2: anchor = self.mapToScene(self.mouse_press_rect.topLeft())
            else: anchor = self.mapToScene(self.mouse_press_rect.topRight())

            new_rect = QRectF(anchor, mouse_pos).normalized()
            self.setPos(new_rect.topLeft())
            self.setRect(0, 0, new_rect.width(), new_rect.height())

            self.update_handles_pos()

            # (满足优化点 3) 缩放时实时更新属性面板
            if self.scene() and hasattr(self.scene(), 'selectionChanged'):
                self.scene().selectionChanged.emit()
        else:
            # 调用父类方法以实现默认的拖拽移动
            super().mouseMoveEvent(event)
            # (满足优化点 3) 移动时实时更新属性面板
            if self.isMovable() and self.scene() and hasattr(self.scene(), 'selectionChanged'):
                 self.scene().selectionChanged.emit()

    def mouseReleaseEvent(self, event):
        if self.is_resizing:
            self.is_resizing = False
            self.current_handle = None
            self.setCursor(QCursor(Qt.ArrowCursor))
            # 最终更新
            if self.scene() and hasattr(self.scene(), 'selectionChanged'):
                self.scene().selectionChanged.emit()
        else:
            super().mouseReleaseEvent(event)