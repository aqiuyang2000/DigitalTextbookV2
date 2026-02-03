# FILE: color_picker_button_parts/_base.py
#
# 功能: 包含 ColorPickerButton 类的 __init__ 方法和核心属性。
#       这是颜色选择器按钮功能组合的基础。

from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal


class ColorPickerButtonBase(QPushButton):
    """
    ColorPickerButton 的基础类。

    这个类只包含 __init__ 方法和 colorChanged 信号，用于设置按钮的
    初始状态和核心事件。它被设计为所有其他功能性 Mixin 类的基础。
    """
    colorChanged = Signal(QColor)

    def __init__(self, initial_color=QColor("blue"), parent=None):
        super().__init__(parent)
        self._color = initial_color
        self.setText("选择颜色...")

        # 注意：这里的 self.pick_color 和 self._update_button_color
        # 将由后续的 Mixin 类提供。
        self.clicked.connect(self.pick_color)
        self._update_button_color()