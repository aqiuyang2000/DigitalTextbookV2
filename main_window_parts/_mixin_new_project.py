# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_new_project.py
#
# 功能: 提供 new_project 方法，用于处理新建项目的流程。

import uuid

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox, QFileDialog

class NewProjectMixin:
    """
    一个 Mixin 类，包含用于创建新项目的 new_project 方法。
    """
    def new_project(self):
        """
        处理“新建项目”的完整流程。

        流程包括：
        1. 检查当前项目是否有未保存的更改 (`is_dirty`)，并提示用户。
        2. 如果用户选择保存但失败（例如，在文件对话框中点了取消），则中止新建流程。
        3. 弹出一个 "另存为" 对话框，让用户为新项目选择位置和文件名。
        4. 如果用户选择了路径，则清空当前所有会话和数据。
        5. 为新项目生成一个唯一的 project_id。
        6. 创建项目的输出目录结构。
        7. 立即执行一次保存，以生成初始的 `.json` 项目文件。
        """
        # 1. 检查当前项目状态
        if self.is_dirty:
            reply = QMessageBox.question(
                self, 
                "新建项目", 
                "您想在新建项目前保存当前项目的更改吗？",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Cancel
            )
            if reply == QMessageBox.Save and not self.save_project():
                # 如果用户选择保存但操作失败或取消，则中止新建项目
                return
            elif reply == QMessageBox.Cancel:
                # 如果用户选择取消，则中止新建项目
                return
        
        # 2. 弹出文件对话框让用户指定新项目路径
        path, _ = QFileDialog.getSaveFileName(self, "新建项目", "", "项目文件 (*.json)")
        if not path:
            # 如果用户未选择路径（点了取消），则中止
            return
            
        # 3. 设置新项目路径并清空工作区
        self.project_path = path
        self.clear_project(keep_path=True) # 清空数据，但保留 project_path

        # 4. 初始化新项目属性
        self.project_id = f"PROJ_{uuid.uuid4().hex[:8]}"
        
        # 5. 创建输出目录
        self._ensure_output_directory()
        
        # 6. 保存空的初始项目文件
        self.save_project()
        
        # 7. 将新项目的状态设置为未修改
        self.set_dirty(False)