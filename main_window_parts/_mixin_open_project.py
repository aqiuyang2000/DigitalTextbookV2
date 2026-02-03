# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_open_project.py
#
# 功能: 提供 open_project 方法，用于处理打开现有项目的流程。

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox, QFileDialog

class OpenProjectMixin:
    """
    一个 Mixin 类，包含用于打开现有项目的 open_project 方法。
    """
    def open_project(self):
        """
        处理“打开项目”的完整流程。

        流程包括：
        1. 检查当前项目是否有未保存的更改，并提示用户。
        2. 如果用户选择保存但失败，则中止打开流程。
        3. 弹出一个 "打开" 对话框，让用户选择一个 `.json` 项目文件。
        4. 如果用户选择了文件，则调用核心的 `_perform_project_load` 方法
           来执行实际的加载和解析工作。
        """
        # 1. 检查当前项目状态，与 new_project 中的逻辑相同
        if self.is_dirty:
            reply = QMessageBox.question(
                self, 
                "打开项目", 
                "您想在打开新项目前保存当前项目的更改吗？",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Cancel
            )
            if reply == QMessageBox.Save and not self.save_project():
                # 如果用户选择保存但操作失败或取消，则中止
                return
            elif reply == QMessageBox.Cancel:
                # 如果用户选择取消，则中止
                return
        
        # 2. 弹出文件对话框让用户选择项目文件
        path, _ = QFileDialog.getOpenFileName(
            self, 
            "打开项目", 
            "", 
            "项目文件 (*.json)"
        )
        if not path:
            # 如果用户未选择文件，则中止
            return

        # 3. 调用核心加载方法
        self._perform_project_load(path)