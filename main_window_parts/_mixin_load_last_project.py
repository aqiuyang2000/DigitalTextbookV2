# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_load_last_project.py
#
# 功能: 提供 _load_last_project 方法，用于在程序启动时自动加载上次的项目。

import os

# --- Qt Imports ---
from PySide6.QtCore import QSettings

class LoadLastProjectMixin:
    """
    一个 Mixin 类，包含在应用程序启动时加载上一个项目的功能。
    """
    def _load_last_project(self):
        """
        尝试在程序启动时加载用户上次打开的项目。

        此方法在 `HotspotEditorBase.__init__` 的末尾被调用。
        它会从 QSettings 中读取 "last_project_path" 的值。如果该值存在，
        并且对应的项目文件也真实存在于磁盘上，则调用 
        `_perform_project_load` 来加载它。
        """
        # 1. 创建 QSettings 实例来访问应用程序的持久化设置
        settings = QSettings("MyCompany", "HotspotEditor")
        
        # 2. 读取上次保存的项目路径，如果没有则返回 None
        last_project_path = settings.value("last_project_path", None)
        
        # 3. 检查路径有效且文件存在
        if last_project_path and os.path.exists(last_project_path):
            print(f"找到上次的项目路径: {last_project_path}，正在尝试加载...")
            # 如果有效，则调用核心加载方法
            self._perform_project_load(last_project_path)
        else:
            # 如果无效，则打印信息并保持应用为空白状态
            print("未找到有效的上次项目路径。")