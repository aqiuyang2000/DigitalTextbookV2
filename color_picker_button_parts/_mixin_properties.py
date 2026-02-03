# FILE: color_picker_button_parts/_mixin_properties.py
#
# 功能: 提供 color getter 和 setColor setter 方法，用于管理按钮的颜色状态。

from PySide6.QtGui import QColor


class ColorPropertiesMixin:
    """
    一个 Mixin 类，为 ColorPickerButton 提供颜色属性的 getter 和 setter。
    """

    def color(self) -> QColor:
        """
        获取当前按钮关联的颜色。

        Returns:
            QColor: 当前的颜色对象。
        """
        return self._color

    def setColor(self, color: QColor):
        """
        设置按钮的新颜色，并触发相应的信号和UI更新。

        如果新设置的颜色与当前颜色不同，它会：
        1. 更新内部的 _color 状态。
        2. 发出 colorChanged 信号，通知外部监听者。
        3. 调用 _update_button_color() 来刷新按钮的背景色。

        Args:
            color (QColor): 要设置的新颜色对象。
        """
        # self._color, self.colorChanged, 和 self._update_button_color
        # 分别由 _base 和 _mixin_update_ui 提供
        if self._color != color:
            self._color = color
            self.colorChanged.emit(self._color)
            self._update_button_color()