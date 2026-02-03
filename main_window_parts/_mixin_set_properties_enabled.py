# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_set_properties_enabled.py
#
# 功能: 提供 set_properties_enabled 方法，用于批量启用/禁用属性面板控件。

class SetPropertiesEnabledMixin:
    """
    一个 Mixin 类，包含用于批量切换属性面板控件可用状态的辅助方法。
    """
    def set_properties_enabled(self, enabled: bool):
        """
        根据给定的状态，批量启用或禁用右侧属性面板中的所有相关控件。

        Args:
            enabled (bool): 如果为 True，则启用所有属性控件；
                            如果为 False，则禁用它们。
        """
        # 创建一个包含所有需要控制的UI控件的列表
        widgets_to_toggle = [
            self.txt_id, 
            self.txt_description, 
            self.txt_x, 
            self.txt_y, 
            self.txt_width, 
            self.txt_height,
            self.type_combo, 
            self.stacked_widget
        ]
        
        # 遍历列表，为每个控件设置启用状态
        for widget in widgets_to_toggle:
            if widget: # 确保控件已经被创建，避免在初始化早期阶段出错
                widget.setEnabled(enabled)