# FILE: graphics_items.py (FINAL ASSEMBLER)
#
# 功能: 这是 graphics_items 模块的公共接口。
#       它从 'graphics_items_parts' 目录中导入所有独立的组件，
#       并通过多重继承将它们组装成功能完整的图形项类。

from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QPen, QBrush, QCursor
from PySide6.QtCore import Qt, QRectF, QPointF

# --- 图形项类 ---

class AbstractResizableItem(QGraphicsRectItem):
    """
    一个抽象基类，提供了可调整大小的控制柄和边界约束功能。
    是所有热区形状的父类。
    """
    def __init__(self, *args, bounds=None, viewer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.handles = []
        self.handle_size = 8.0
        self.current_handle = None
        self.is_resizing = False
        self.bounds = bounds
        self.viewer = viewer # 引用视图以获取缩放比例
        self.mouse_press_rect = None # 添加缺失的属性初始化

        self.setAcceptHoverEvents(True)
        self.setFlags(
            QGraphicsRectItem.ItemIsSelectable |
            QGraphicsRectItem.ItemIsMovable |
            QGraphicsRectItem.ItemSendsGeometryChanges
        )

        for i in range(4):
            handle = QGraphicsRectItem(0, 0, self.handle_size, self.handle_size, self)
            handle.setBrush(QBrush(Qt.white))
            handle.setPen(QPen(Qt.black, 1.0))
            handle.setVisible(False)
            self.handles.append(handle)
        self.update_handles_pos()

    def type(self):
        return QGraphicsRectItem.UserType + 1

    def update_handles_pos(self):
        if not self.viewer: return
        try:
            scale_factor = self.viewer.transform().m11()
            if scale_factor < 1e-6: return # 避免除以零
            adjusted_size = self.handle_size / scale_factor
            s = adjusted_size / 2
            for handle in self.handles:
                handle.setRect(-s, -s, adjusted_size, adjusted_size)

            r = self.rect()
            self.handles[0].setPos(r.topLeft())
            self.handles[1].setPos(r.topRight())
            self.handles[2].setPos(r.bottomRight())
            self.handles[3].setPos(r.bottomLeft())
        except Exception:
            # 在 viewer 无效的极端情况下提供保护
            pass


    def updateForViewTransform(self):
        self.update_handles_pos()

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemSelectedChange:
            for handle in self.handles:
                handle.setVisible(value)
            if value:
                self.updateForViewTransform()
        elif change == QGraphicsRectItem.ItemPositionChange and self.scene():
            if self.is_resizing: # *** 关键修复 ***
                return value    # 在缩放时不应用移动约束，但允许事件继续

            new_pos = value
            if self.bounds:
                new_rect = QRectF(new_pos, self.rect().size())
                if new_rect.left() < self.bounds.left(): new_pos.setX(self.bounds.left())
                elif new_rect.right() > self.bounds.right(): new_pos.setX(self.bounds.right() - self.rect().width())
                if new_rect.top() < self.bounds.top(): new_pos.setY(self.bounds.top())
                elif new_rect.bottom() > self.bounds.bottom(): new_pos.setY(self.bounds.bottom() - self.rect().height())
            return new_pos
        elif change == QGraphicsRectItem.ItemPositionHasChanged:
            if self.scene() and hasattr(self.scene(), 'selectionChanged'):
                self.scene().selectionChanged.emit()
        return super().itemChange(change, value)

    def hoverMoveEvent(self, event):
        handle_at_pos = -1
        for i, handle in enumerate(self.handles):
            if handle.sceneBoundingRect().contains(event.scenePos()):
                handle_at_pos = i
                break

        if handle_at_pos != -1:
            if handle_at_pos in [0, 2]: self.setCursor(QCursor(Qt.SizeFDiagCursor))
            else: self.setCursor(QCursor(Qt.SizeBDiagCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        self.is_resizing = False
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

            if self.bounds:
                mouse_pos.setX(max(self.bounds.left(), min(mouse_pos.x(), self.bounds.right())))
                mouse_pos.setY(max(self.bounds.top(), min(mouse_pos.y(), self.bounds.bottom())))

            if self.current_handle == 0: anchor = self.mapToScene(self.mouse_press_rect.bottomRight())
            elif self.current_handle == 1: anchor = self.mapToScene(self.mouse_press_rect.bottomLeft())
            elif self.current_handle == 2: anchor = self.mapToScene(self.mouse_press_rect.topLeft())
            else: anchor = self.mapToScene(self.mouse_press_rect.topRight())

            new_rect = QRectF(anchor, mouse_pos).normalized()
            self.setPos(new_rect.topLeft())
            self.setRect(0, 0, new_rect.width(), new_rect.height())
            self.update_handles_pos()
            if self.scene() and hasattr(self.scene(), 'selectionChanged'):
                self.scene().selectionChanged.emit()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.is_resizing:
            self.is_resizing = False
            self.current_handle = None
            self.setCursor(QCursor(Qt.ArrowCursor))
            if self.scene() and hasattr(self.scene(), 'selectionChanged'):
                self.scene().selectionChanged.emit()
        else:
            super().mouseReleaseEvent(event)

class ResizableRectItem(AbstractResizableItem):
    """可调整大小的矩形热区。"""
    def paint(self, painter, option, widget):
        painter.setPen(self.pen())
        painter.setBrush(self.brush())
        painter.drawRect(self.rect())

    def type(self):
        return QGraphicsRectItem.UserType + 2

class ResizableEllipseItem(AbstractResizableItem):
    """可调整大小的椭圆热区。"""
    def paint(self, painter, option, widget):
        painter.setPen(self.pen())
        painter.setBrush(self.brush())
        painter.drawEllipse(self.rect())

    def type(self):
        return QGraphicsRectItem.UserType + 3