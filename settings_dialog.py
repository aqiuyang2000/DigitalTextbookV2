# FILE: settings_dialog.py (Corrected Final Assembler)
#
# 功能: 这是 settings_dialog 模块的最终组合文件。
#       它首先从 'color_picker_button_parts' 中组装出完整的 ColorPickerButton 类，
#       然后再从 'settings_dialog_parts' 中组装出完整的 SettingsDialog 类。
#       通过在同一个文件中定义这两个紧密耦合的类，我们解决了模块导入错误。

# --- 1. ColorPickerButton 组件组装 ---

# 1a. 导入 ColorPickerButton 的基础和 Mixin 部分
from color_picker_button_parts._base import ColorPickerButtonBase
from color_picker_button_parts._mixin_pick_color import PickColorMixin
from color_picker_button_parts._mixin_properties import ColorPropertiesMixin
from color_picker_button_parts._mixin_update_ui import UpdateUiMixin

# 1b. 组装最终的 ColorPickerButton 类
class ColorPickerButton(
    ColorPickerButtonBase,
    PickColorMixin,
    ColorPropertiesMixin,
    UpdateUiMixin
):
    """
    一个点击后会弹出颜色选择器的按钮。
    通过多重继承组合所有功能性 Mixin 类构建而成。
    """
    pass


# --- 2. SettingsDialog 主对话框组装 ---

# 2a. 导入 SettingsDialog 的基础和 Mixin 部分
from settings_dialog_parts._base import SettingsDialogBase
from settings_dialog_parts._mixin_update_ui_state import UpdateUiStateMixin
from settings_dialog_parts._mixin_load_settings import LoadSettingsMixin
from settings_dialog_parts._mixin_save_settings import SaveSettingsMixin
from settings_dialog_parts._mixin_apply_logic import ApplyLogicMixin
from settings_dialog_parts._mixin_events import DialogEventsMixin


# 2b. 组装最终的 SettingsDialog 类
class SettingsDialog(
    SettingsDialogBase,
    UpdateUiStateMixin,
    LoadSettingsMixin,
    SaveSettingsMixin,
    ApplyLogicMixin,
    DialogEventsMixin
):
    """
    用于编辑热区外观和行为的设置对话框。
    通过多重继承组合所有功能性 Mixin 类构建而成。
    """
    pass