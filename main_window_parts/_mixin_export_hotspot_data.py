# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_export_hotspot_data.py
#
# 功能: 提供 export_hotspot_data 方法，用于将项目中所有页面的热区数据导出到 Excel 文件。

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox, QFileDialog

# --- Project-specific Imports ---
from excel_processor import ExcelProcessor
from graphics_items import AbstractResizableItem, ResizableEllipseItem
from utils import create_default_data

class ExportHotspotDataMixin:
    """
    一个 Mixin 类，包含将整个项目的所有热区数据导出到 Excel 的功能。
    """
    def export_hotspot_data(self):
        """
        “导出所有热区数据 (Excel)”按钮的槽函数。

        此方法会遍历项目中的每一个会话（页面），收集所有热区的位置、
        尺寸和自定义数据，然后将这些数据组织成 `ExcelProcessor` 期望的
        格式，并调用 `export_hotspots_to_excel` 方法来生成一个多工作表
        (multi-sheet) 的 Excel 文件，每个工作表对应项目中的一个页面。
        """
        # 1. 前置检查
        if not self.sessions:
            QMessageBox.warning(self, "无内容", "项目中没有任何页面可供导出数据。")
            return
        
        # 2. 弹出文件保存对话框
        default_filename = "all_pages_hotspots.xlsx"
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "导出所有热区数据", 
            default_filename, 
            "Excel 文件 (*.xlsx)"
        )
        if not file_path:
            return

        # 3. 构建 `project_data` 字典
        project_data = {'pages': []}
        for session in self.sessions:
            page_data = {'hotspots': []}
            for item in session.scene.items():
                if isinstance(item, AbstractResizableItem):
                    pos = item.pos()
                    rect = item.rect()
                    
                    hotspot_info = {
                        'pos': {'x': pos.x(), 'y': pos.y()},
                        'rect': {'w': rect.width(), 'h': rect.height()},
                        'type': 'ellipse' if isinstance(item, ResizableEllipseItem) else 'rectangle',
                        'data': item.data(0) or create_default_data()
                    }
                    page_data['hotspots'].append(hotspot_info)
            project_data['pages'].append(page_data)

        # 4. 调用 ExcelProcessor 执行导出
        try:
            ExcelProcessor.export_hotspots_to_excel(project_data, file_path)
            QMessageBox.information(
                self, 
                "导出成功",
                f"所有页面的热区数据已成功导出到:\n{file_path}"
            )
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"写入Excel文件时发生错误：\n{e}")