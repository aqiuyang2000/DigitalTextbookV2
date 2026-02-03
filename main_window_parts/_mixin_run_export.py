# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_run_export.py
#
# 功能: 提供 _run_export 通用执行器方法，处理所有“完整导出”的通用逻辑。

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox

class RunExportMixin:
    """
    一个 Mixin 类，包含用于执行完整导出操作的通用方法 `_run_export`。
    """
    def _run_export(self, export_function, *args):
        """
        一个通用的“完整导出”执行器。

        这个方法封装了所有完整导出操作（区别于“片段更新”）的通用流程：
        1. 检查项目是否已保存。
        2. 获取项目的输出目录。
        3. 如果上述检查通过，则调用传入的 `export_function` 来执行
           具体的导出工作。
        4. 导出成功后，启用“在浏览器中预览”按钮。

        Args:
            export_function (callable): 实际要执行的导出函数
                                        (例如, `export_as_modular_flipbook`)。
            *args: 传递给 `export_function` 的额外参数 (尽管当前未使用，
                   但保留以增加灵活性)。
        """
        # 1. 检查项目是否已保存
        if not self.project_path:
            QMessageBox.warning(self, "无项目", "请先保存或打开一个项目再进行导出。")
            return

        # 2. 获取输出目录
        output_dir = self._get_output_directory()
        if not output_dir:
            # _get_output_directory 理论上在 project_path 存在时总会返回路径，
            # 这是一个双重保险。
            return

        # 3. 调用具体的导出函数
        #    主窗口实例(self)和输出目录(output_dir)是标准参数
        export_function(self, output_dir, *args)
        
        # 4. 导出成功后，启用预览按钮
        if self.btn_preview:
            self.btn_preview.setEnabled(True)