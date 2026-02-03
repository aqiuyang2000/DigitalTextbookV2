# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_export_current_page_data.py
#
# 功能: 提供 export_current_page_data 方法，用于将当前页面的热区数据导出到 Excel 文件。

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox, QFileDialog

# --- Project-specific Imports ---
from excel_processor import ExcelProcessor
from graphics_items import AbstractResizableItem, ResizableEllipseItem
from utils import create_default_data

class ExportCurrentPageDataMixin:
    """
    一个 Mixin 类，包含将当前活动页面的热区数据导出到 Excel 的功能。
    """
    def export_current_page_data(self):
        """
        “导出当前页数据 (Excel)”按钮的槽函数。

        此方法会收集当前活动会话（页面）中的所有热区数据，并调用
        `ExcelProcessor.export_single_page_hotspots_to_excel` 方法来
        生成一个单工作表的 Excel 文件。
        """
        # 1. 前置检查
        if not self.active_session:
            QMessageBox.warning(self, "无活动页面", "没有可导出的当前页面。")
            return
        
        # 2. 弹出文件保存对话框
        page_num = self.active_session_index + 1
        default_filename = f"page_{page_num}_hotspots.xlsx"
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "导出当前页热区数据", 
            default_filename, 
            "Excel 文件 (*.xlsx)"
        )
        if not file_path:
            return

        # 3. 构建 `page_data` 字典
        page_data = {
            'page_index': page_num, 
            'hotspots': []
        }
        session = self.active_session
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

        # 4. 调用 ExcelProcessor 执行导出
        try:
            ExcelProcessor.export_single_page_hotspots_to_excel(page_data, file_path)
            QMessageBox.information(
                self,
                "导出成功",
                f"当前页的热区数据已成功导出到:\n{file_path}"
            )
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"写入Excel文件时发生错误：\n{e}")