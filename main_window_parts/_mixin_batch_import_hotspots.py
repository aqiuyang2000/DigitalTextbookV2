# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_batch_import_hotspots.py
#
# 功能: 提供 batch_import_hotspots 方法，用于从 Excel 文件批量导入热区。

import os

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox, QFileDialog

# --- Project-specific Imports ---
from excel_processor import ExcelProcessor
from commands import BatchAddHotspotsCommand

class BatchImportHotspotsMixin:
    """
    一个 Mixin 类，包含用于从 Excel 文件批量导入热区的功能。
    """
    def batch_import_hotspots(self):
        """
        处理“批量导入当页热区”按钮点击事件的槽函数。

        流程：
        1. 检查是否有活动页面以及项目是否已保存（需要 media 目录）。
        2. 弹出一个文件打开对话框，让用户选择一个 `.xlsx` Excel 文件。
        3. 调用 `ExcelProcessor.import_hotspots_from_excel` 来解析文件。
           这个过程包括数据验证和处理文件类型热区的文件复制。
        4. 如果解析成功并返回了有效数据，则创建一个 `BatchAddHotspotsCommand`。
        5. 将命令推送到当前页面的撤销栈以执行导入，并显示成功信息。
        6. 处理所有可能的错误（如文件格式错误、解析异常）并向用户报告。
        """
        # 1. 前置检查
        if not self.active_session:
            QMessageBox.warning(self, "无活动页面", "请先选择一个页面以导入热区。")
            return
            
        output_dir = self._get_output_directory()
        if not output_dir:
            QMessageBox.warning(self, "项目未保存", "请先保存项目，以便确定媒体文件的存放位置。")
            return
            
        media_dir = os.path.join(output_dir, "media")
        os.makedirs(media_dir, exist_ok=True)

        # 2. 弹出文件选择对话框
        path, _ = QFileDialog.getOpenFileName(self, "批量导入当页热区", "", "Excel 文件 (*.xlsx)")
        if not path:
            return

        try:
            # 3. 调用 ExcelProcessor 解析文件
            hotspots_to_add = ExcelProcessor.import_hotspots_from_excel(path, media_dir)
            
            # ExcelProcessor 在表头格式不正确时会返回 None
            if hotspots_to_add is None:
                QMessageBox.critical(self, "导入失败", "Excel文件表头格式不正确，请检查是否包含所有必需的列。")
                return
            
            # 如果文件有效但没有数据行
            if not hotspots_to_add:
                QMessageBox.information(self, "导入完成", "文件中没有找到有效的热区数据。")
                return
            
            # 4. 创建批量添加命令
            command = BatchAddHotspotsCommand(
                self.active_session.scene, 
                self.active_session.viewer, 
                self, 
                hotspots_to_add
            )
            
            # 5. 推送命令到撤销栈
            self.active_session.undo_stack.push(command)
            QMessageBox.information(self, "导入成功", f"成功导入 {len(hotspots_to_add)} 个热区。")

        except Exception as e:
            # 6. 捕获其他未知异常
            QMessageBox.critical(self, "导入失败", f"处理Excel文件时发生未知错误：\n{e}")