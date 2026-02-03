# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_select_hotspot_file.py

import os
import shutil

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox, QFileDialog

# --- Project-specific Imports ---
from commands import DataChangeCommand
from utils import create_default_data


class SelectHotspotFileMixin:
    """
    一个 Mixin 类，包含 select_hotspot_file 方法，用于处理文件类型热区的文件选择。
    """

    def select_hotspot_file(self):
        """
        “上传文件...”按钮的槽函数。
        """
        if not self.active_session or not self.active_session.scene.selectedItems():
            return

        if not self.project_path:
            QMessageBox.warning(self, "需要保存项目", "在上传文件前，请先保存您的项目。")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "选择要链接的本地文件")

        if file_path:
            try:
                output_dir = self._get_output_directory()
                if not output_dir:
                    QMessageBox.critical(self, "错误", "无法确定项目输出目录。")
                    return

                media_dir = os.path.join(output_dir, "media")
                os.makedirs(media_dir, exist_ok=True)

                filename = os.path.basename(file_path)
                destination_path = os.path.join(media_dir, filename)

                shutil.copy(file_path, destination_path)

                item = self.active_session.scene.selectedItems()[0]
                old_data = item.data(0) or create_default_data()
                new_data = old_data.copy()

                # --- *** 核心修改: 根据文件扩展名自动匹配图标类型 *** ---
                _, ext = os.path.splitext(filename.lower())
                icon_type = 'default'  # 默认图标
                if ext in ['.mp3', '.wav', '.ogg', '.m4a']:
                    icon_type = 'audio'
                elif ext in ['.mp4', '.mov', '.webm', '.avi']:
                    icon_type = 'video'
                elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.bmp']:
                    icon_type = 'image'
                elif ext in ['.pdf']:
                    icon_type = 'pdf'
                elif ext in ['.html', '.htm']:
                    icon_type = 'link'

                new_data['icon_type'] = icon_type
                # --- *** 修改结束 *** ---

                if "file_data" not in new_data:
                    new_data["file_data"] = create_default_data()["file_data"]
                else:
                    new_data["file_data"] = new_data["file_data"].copy()

                new_data["file_data"]["source_path"] = destination_path

                # 更新UI标签以提供即时反馈
                self.lbl_filename.setText(f"<i>{filename}</i>")

                command = DataChangeCommand(item, old_data, new_data)
                self.active_session.undo_stack.push(command)

            except Exception as e:
                QMessageBox.critical(self, "文件错误", f"无法复制文件: {e}")