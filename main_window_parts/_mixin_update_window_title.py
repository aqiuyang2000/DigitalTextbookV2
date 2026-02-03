# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_update_window_title.py
#
# 功能: 提供 update_window_title 方法，用于更新主窗口的标题栏。

import os

class UpdateWindowMixin:
    """
    一个 Mixin 类，包含用于更新主窗口标题的 update_window_title 方法。
    """
    def update_window_title(self, dirty=False):
        """
        根据当前项目状态更新主窗口的标题栏。

        标题格式会根据项目是否已保存以及是否有未保存的更改 (`dirty`) 
        来动态调整。
        
        Args:
            dirty (bool): 如果为 True, 表示有未保存的更改，标题末尾会添加 "*".
        """
        base_title = "图片热区链接添加工具"
        
        # 根据 dirty 状态决定是否显示星号
        dirty_indicator = " *" if dirty else ""

        # 根据 self.project_path 是否存在来构建最终标题
        if self.project_path:
            # 如果有项目路径，显示 "项目文件名* - 基础标题"
            project_filename = os.path.basename(self.project_path)
            full_title = f"{project_filename}{dirty_indicator} - {base_title}"
        else:
            # 如果没有项目路径，显示 "未命名项目* - 基础标题"
            full_title = f"未命名项目{dirty_indicator} - {base_title}"
            
        # 调用 QMainWindow 的 setWindowTitle 方法设置标题
        self.setWindowTitle(full_title)