# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_open_pdf_toolbox.py
#
# 功能: 提供 open_pdf_toolbox 方法，用于打开 PDF 工具箱对话框。

# --- Project-specific Imports ---
from pdf_toolbox_dialog import PdfToolboxDialog

class OpenPdfToolboxMixin:
    """
    一个 Mixin 类，包含用于打开 PDF 工具箱对话框的功能。
    """
    def open_pdf_toolbox(self):
        """
        “PDF 工具箱...”按钮的槽函数。

        此方法会创建一个 `PdfToolboxDialog` 实例并以模态方式显示它。
        `PdfToolboxDialog` 自身负责动态加载所有可用的 PDF 工具、
        显示工具的选项 UI，并在用户点击“运行工具”时执行所选工具的
        `run` 方法。
        """
        # 1. 创建 PdfToolboxDialog 实例，父窗口为 self (主窗口)
        dialog = PdfToolboxDialog(self)
        
        # 2. 以模态方式执行对话框
        #    程序流程会在这里暂停，直到用户关闭工具箱对话框。
        dialog.exec()