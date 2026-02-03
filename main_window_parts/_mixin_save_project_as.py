# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_save_project_as.py
#
# 功能: 提供 save_project_as 方法，用于将当前项目另存为新文件。

# --- Qt Imports ---
from PySide6.QtWidgets import QFileDialog

class SaveProjectAsMixin:
    """
    一个 Mixin 类，包含用于将项目另存为的 save_project_as 方法。
    """
    def save_project_as(self) -> bool:
        """
        处理“另存为”流程。

        此方法总是会弹出一个文件保存对话框，让用户选择一个新的路径和文件名。
        如果用户确认选择：
        1. 更新 `self.project_path` 为新的路径。
        2. 确保与新项目文件配套的输出目录 (`_out`) 被创建。
        3. 更新窗口标题以反映新的文件名。
        4. 调用 `self.save_project()` 方法来执行实际的文件写入操作。

        Returns:
            bool: 如果项目成功保存到新位置则返回 True，否则（例如用户
                  在对话框中点击了取消）返回 False。
        """
        # 1. 弹出文件保存对话框
        path, _ = QFileDialog.getSaveFileName(
            self, 
            "项目另存为", 
            "", 
            "项目文件 (*.json)"
        )
        
        # 如果用户取消对话框，则返回 False 表示操作未完成
        if not path:
            return False
            
        # 2. 更新实例的 project_path
        self.project_path = path
        
        # 3. 确保新的输出目录存在
        self._ensure_output_directory()
        
        # 4. 更新窗口标题
        self.update_window_title()
        
        # 5. 调用常规的保存方法
        return self.save_project()