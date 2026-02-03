# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_toggle_outline_panel.py
#
# 功能: 提供 toggle_outline_panel 方法，用于显示或隐藏提纲面板。

class ToggleOutlinePanelMixin:
    """
    一个 Mixin 类，包含用于切换提纲/目录面板可见性的槽函数。
    """
    def toggle_outline_panel(self, checked: bool):
        """
        “显示/隐藏提纲面板”菜单项的槽函数。

        根据菜单项的勾选状态来显示或隐藏位于主窗口左侧的提纲面板
        (`self.outline_widget`)。同时，它也会更新菜单项自身的文本，
        在“显示提纲面板”和“隐藏提纲面板”之间切换，以提供更清晰的
        用户指示。

        Args:
            checked (bool): QAction 的 `triggered` 信号在 action 是
                            checkable 时会传递其当前的勾选状态。
                            True 表示被勾选（应显示），False 表示
                            未被勾选（应隐藏）。
        """
        # 1. 根据 checked 参数设置 outline_widget 的可见性
        self.outline_widget.setVisible(checked)
        
        # 2. 动态更新菜单项的文本
        if checked:
            self.toggle_outline_action.setText("隐藏提纲面板")
        else:
            self.toggle_outline_action.setText("显示提纲面板")