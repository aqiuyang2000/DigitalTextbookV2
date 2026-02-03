# D:\projects-singlepage\hotspot_editor\main_window_parts\_mixin_get_current_shape.py
#
# 功能: 提供 get_current_shape 辅助方法，用于获取当前选中的绘图形状。

class GetCurrentShapeMixin:
    """
    一个 Mixin 类，包含一个辅助方法，用于获取当前选中的绘图形状。
    """
    def get_current_shape(self) -> str:
        """
        获取“绘制形状”下拉框 (`shape_combo`) 当前选中的项的文本。

        这个方法主要被 `PhotoViewer` 在完成一次新的矩形框选操作后调用，
        以决定应该创建一个 `ResizableRectItem` 还是 `ResizableEllipseItem`。

        Returns:
            str: 当前选中的形状名称，例如 "Rectangle" 或 "Ellipse"。
        """
        # 直接返回 shape_combo 控件的当前文本值
        # 在调用此方法时，shape_combo 应该已经被创建
        if self.shape_combo:
            return self.shape_combo.currentText()
        
        # 提供一个默认值以防万一
        return "Rectangle"