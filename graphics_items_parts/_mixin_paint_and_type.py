# FILE: _mixin_paint_and_type.py
#
# 功能: 提供 ResizableRectItem 和 ResizableEllipseItem 各自的 paint 和 type 方法。

from PySide6.QtWidgets import QGraphicsRectItem


class PaintAndTypeMixin:
    """
    一个 Mixin 类，包含用于具体形状子类的 paint 和 type 方法。
    这些方法将通过多重继承被添加到最终的子类中。
    """

    # --- Method for AbstractResizableItem ---
    # 我们也把基类的 type 方法放在这里，以保持一致性。

    def type_abstract(self):
        """
        AbstractResizableItem 的 type 方法实现。
        """
        return QGraphicsRectItem.UserType + 1

    # --- Methods for ResizableRectItem ---

    def paint_rect(self, painter, option, widget):
        """
        ResizableRectItem 的 paint 方法实现。
        绘制一个矩形。
        """
        painter.setPen(self.pen())
        painter.setBrush(self.brush())
        painter.drawRect(self.rect())

    def type_rect(self):
        """
        ResizableRectItem 的 type 方法实现。
        返回一个唯一的类型标识符，用于 Qt 的内部类型转换和识别。
        """
        return QGraphicsRectItem.UserType + 2

    # --- Methods for ResizableEllipseItem ---

    def paint_ellipse(self, painter, option, widget):
        """
        ResizableEllipseItem 的 paint 方法实现。
        在其边界矩形内绘制一个椭圆。
        """
        painter.setPen(self.pen())
        painter.setBrush(self.brush())
        painter.drawEllipse(self.rect())

    def type_ellipse(self):
        """
        ResizableEllipseItem 的 type 方法实现。
        返回一个唯一的类型标识符。
        """
        return QGraphicsRectItem.UserType + 3