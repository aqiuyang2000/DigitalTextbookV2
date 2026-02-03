# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_save_project.py
#
# 功能: 提供 save_project 方法，用于保存当前项目到磁盘。

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QSettings

class SaveProjectMixin:
    """
    一个 Mixin 类，包含用于保存当前项目的 save_project 方法。
    """
    def save_project(self) -> bool:
        """
        将当前项目的所有数据保存到 `self.project_path` 指定的文件中。

        如果 `self.project_path` 尚未设置，它会调用 `save_project_as`
        来让用户选择一个保存位置。

        流程包括：
        1. 检查项目路径是否存在，若不存在则转到“另存为”。
        2. 调用 `self.project_manager` 来执行实际的序列化和文件写入。
        3. 成功后，更新状态栏信息。
        4. 将项目路径保存到 QSettings 以便下次启动时能“记住”。
        5. 将所有页面的撤销栈标记为“干净”(clean)。
        6. 调用 `set_dirty(False)` 更新UI状态。

        Returns:
            bool: 如果项目成功保存则返回 True，否则（例如用户取消了
                  另存为对话框）返回 False。
        """
        # 1. 如果没有项目路径，则等同于“另存为”
        if not self.project_path:
            return self.save_project_as()

        try:
            # 2. 调用 ProjectManager 执行核心保存逻辑
            self.project_manager.save_project(
                self.sessions,
                self.project_path,
                self.project_id,
                self.outline_data
            )
            
            # 3. 更新状态栏
            self.statusBar().showMessage("项目已保存！", 2000)
            
            # 4. 记住最后保存的项目路径
            settings = QSettings("MyCompany", "HotspotEditor")
            settings.setValue("last_project_path", self.project_path)
            
            # 5. 将所有页面的 undo_stack 标记为干净状态
            for session in self.sessions:
                session.undo_stack.setClean()
            
            # 6. 更新窗口的 dirty 状态
            self.set_dirty(False)
            
            return True

        except Exception as e:
            # 如果保存过程中发生任何错误，显示错误信息
            QMessageBox.critical(self, "保存失败", f"无法保存项目文件：{e}")
            return False