# FILE: color_picker_button_parts/_mixin_pick_color.py
#
# 功能: 提供 pick_color 方法的实现，用于处理按钮点击事件并打开颜色选择对话框。

from PySide6.QtWidgets import QColorDialog


class PickColorMixin:
    """
    一个 Mixin 类，为 ColorPickerButton 提供 pick_color 方法。
    """

    def pick_color(self):
        """
        当按钮被点击时调用的槽函数。

        它会创建一个 QColorDialog 实例，并使用按钮当前的颜色
        作为初始颜色。如果用户在对话框中选择了一个新颜色并点击 "OK"，
        则调用 self.setColor() 更新按钮的颜色。
        """
        # self._color 和 self.setColor 将分别由 _base 和 _mixin_properties 提供
        dialog = QColorDialog(self._color, self)
        if dialog.exec():
            self.setColor(dialog.currentColor())