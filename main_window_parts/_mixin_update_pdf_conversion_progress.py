# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_update_pdf_conversion_progress.py
#
# 功能: 提供 _update_pdf_conversion_progress 槽函数，用于在状态栏显示PDF处理进度。

# --- Qt Imports ---
from PySide6.QtWidgets import QApplication

class UpdatePdfConversionProgressMixin:
    """
    一个 Mixin 类，包含用于响应 PDFProcessor 进度更新的槽函数。
    """
    def _update_pdf_conversion_progress(self, current_page: int, total_pages: int):
        """
        当 `PdfProcessor` 正在转换 PDF 页面时被调用的槽函数。

        它接收当前处理的页码和总页数，并将格式化后的进度信息显示在
        主窗口底部的状态栏上。

        `QApplication.processEvents()` 的调用是关键，它强制 Qt 事件循环
        立即处理UI更新，确保即使用户界面在后台处于繁忙状态，状态栏的
        文本也能实时刷新。

        Args:
            current_page (int): 当前正在处理的页面编号 (从1开始)。
            total_pages (int): PDF文件的总页数。
        """
        # 1. 在状态栏显示格式化的进度文本
        self.statusBar().showMessage(
            f"正在转换 PDF: 第 {current_page} / {total_pages} 页..."
        )
        
        # 2. 强制处理UI事件
        #    因为 PDF 处理可能是一个耗时的阻塞操作，如果不调用此方法，
        #    状态栏的文本更新可能会被延迟到整个转换过程结束后才显示，
        #    从而失去了实时进度的意义。
        QApplication.processEvents()