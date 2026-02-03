# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_run_fragment_export.py
#
# 功能: 提供 _run_fragment_export 通用执行器方法，处理所有“片段更新”的通用逻辑。
# 注意: 此文件是基于原始代码的结构优化而创建的，以统一导出逻辑。

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox

class RunFragmentExportMixin:
    """
    一个 Mixin 类，包含用于执行片段导出/更新操作的通用方法 `_run_fragment_export`。
    """
    def _run_fragment_export(self, export_function, *args):
        """
        一个通用的“片段更新”执行器。

        这个方法封装了所有片段更新操作的通用流程：
        1. 检查项目是否已保存（因为需要输出目录）。
        2. 获取项目的输出目录。
        3. 如果上述检查通过，则调用传入的 `export_function` 来执行
           具体的片段导出工作。

        与 `_run_export` 相比，它更轻量，不包含“启用预览按钮”等后处理。

        Args:
            export_function (callable): 实际要执行的片段导出函数
                                        (例如, `export_double_page_fragment`)。
            *args: 传递给 `export_function` 的额外参数。
        """
        # 1. 检查项目是否已保存
        if not self.project_path:
            QMessageBox.warning(self, "无项目", "请先保存或打开一个项目再进行导出。")
            return

        # 2. 获取输出目录
        output_dir = self._get_common_output_dir()
        if not output_dir:
            return

        # 3. 调用具体的片段导出函数
        #    片段导出函数也需要主窗口实例(self)和输出目录(output_dir)
        export_function(self, output_dir, *args)
        
# **说明**:
# 采用这个新的执行器后，之前的片段导出包装器 Mixin (如
# _mixin_export_as_double_page_fragment_wrapper.py) 的代码
# 就可以被简化为：
#
# def export_as_double_page_fragment_wrapper(self):
#     self._run_fragment_export(export_double_page_fragment)
#
# 这样就和完整导出的模式完全统一了。