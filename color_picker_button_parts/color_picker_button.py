# FILE: color_picker_button.py (New Assembler File)
#
# 功能: 这是 ColorPickerButton 类的最终组合文件。
#       它从 'color_picker_button_parts' 目录中导入基类和所有功能性的
#       Mixin 类，并通过多重继承将它们组合成一个功能完整的 ColorPickerButton 类。

# --- A. 基础类别 ---
from color_picker_button_parts._base import ColorPickerButtonBase

# --- B. Mixin 模块 ---
from color_picker_button_parts._mixin_pick_color import PickColorMixin
from color_picker_button_parts._mixin_properties import ColorPropertiesMixin
from color_picker_button_parts._mixin_update_ui import UpdateUiMixin


class ColorPickerButton(
    # --- 继承顺序 ---
    ColorPickerButtonBase,
    PickColorMixin,
    ColorPropertiesMixin,
    UpdateUiMixin
):
    """
    通过多重继承组合所有功能性 Mixin 类，构建最终的 ColorPickerButton。
    这个类是一个独立的、可重用的UI组件。
    """
    pass