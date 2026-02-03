# FILE: color_picker_button_parts/_mixin_update_ui.py
#
# 功能: 提供私有方法 _update_button_color，用于刷新按钮的背景色。

from PySide6.QtGui import QPalette


class UpdateUiMixin:
    """
    一个 Mixin 类，为 ColorPickerButton 提供更新其背景色的私有方法。
    """

    def _update_button_color(self):
        """
        根据当前的 self._color 值，更新按钮的背景调色板。

        这个方法使得按钮的背景色能够直观地反映出它所代表的颜色值。
        """
        # self._color 将由 _base 提供
        palette = self.palette()
        palette.setColor(QPalette.Button, self._color)
        self.setPalette(palette)
        self.update()  # 强制重绘控件