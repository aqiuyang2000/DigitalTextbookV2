# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_export_all_formats.py
#
# 功能: 提供 export_all_formats 方法，用于一键导出所有支持的网页格式。

import traceback

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox, QProgressDialog, QApplication
from PySide6.QtCore import Qt

# --- Project-specific Imports ---
from exporter import HtmlExporter
from exporter_flip import export_as_modular_flipbook

class ExportAllFormatsMixin:
    """
    一个 Mixin 类，包含一键导出所有网页格式的功能。
    """
    def export_all_formats(self):
        """
        “一键导出所有格式”按钮的槽函数。

        此方法会依次调用三种不同格式的导出函数，并使用一个
        `QProgressDialog` 来向用户显示长时间操作的进度。

        流程：
        1. 检查项目是否已保存且有内容可供导出。
        2. 创建并显示一个进度对话框。
        3. 按顺序执行三种导出：
           - 双页画册 (export_as_modular_flipbook)
           - 单页画册 (HtmlExporter.export_as_single_page_flipbook)
           - 动态网页 (HtmlExporter.export_as_dynamic_page)
        4. 在每个步骤之间更新进度对话框，并检查用户是否点击了“取消”。
        5. 所有导出完成后，显示成功信息并启用预览按钮。
        6. 捕获任何异常或用户的取消操作，并给出相应提示。
        """
        # 1. 前置检查
        if not self.project_path:
            QMessageBox.warning(self, "无项目", "请先保存或打开一个项目再进行导出。")
            return
        if not self.sessions:
            QMessageBox.warning(self, "无内容", "项目中没有任何页面可供导出。")
            return

        output_dir = self._get_output_directory()
        if not output_dir:
            QMessageBox.critical(self, "错误", "无法确定项目输出目录。")
            return

        # 2. 创建并显示进度对话框
        progress = QProgressDialog("正在一键导出所有格式...", "取消", 0, 3, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle("批量导出")
        progress.show()

        try:
            # --- 步骤 1: 导出双页画册 ---
            QApplication.processEvents() # 确保对话框能立即显示
            progress.setLabelText("正在导出为双页画册...")
            export_as_modular_flipbook(self, output_dir)
            progress.setValue(1)

            # --- 步骤 2: 导出单页画册 ---
            QApplication.processEvents() # 刷新UI
            if progress.wasCanceled(): 
                raise InterruptedError("用户取消") # 自定义一个错误以便捕获
            progress.setLabelText("正在导出为单页画册...")
            HtmlExporter.export_as_single_page_flipbook(self, output_dir)
            progress.setValue(2)

            # --- 步骤 3: 导出动态网页 ---
            QApplication.processEvents() # 刷新UI
            if progress.wasCanceled(): 
                raise InterruptedError("用户取消")
            progress.setLabelText("正在导出为动态网页...")
            HtmlExporter.export_as_dynamic_page(self, output_dir)
            progress.setValue(3)

            # 5. 成功完成
            self.btn_preview.setEnabled(True)
            self.statusBar().showMessage("一键导出成功！所有格式已导出到项目输出目录。", 5000)

        except InterruptedError:
            self.statusBar().showMessage("导出操作被用户取消。", 3000)
        except Exception as e:
            # 6. 捕获其他异常
            QMessageBox.critical(self, "导出失败", f"批量导出过程中发生错误: {e}\n{traceback.format_exc()}")
        finally:
            # 确保进度对话框总是被关闭
            progress.close()

# 为了在 try...except 中使用，我们可以在模块级别定义这个简单的异常
class InterruptedError(Exception):
    pass