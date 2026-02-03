# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_export_to_html_wrapper.py
#
# 功能: 提供 export_to_html_wrapper 方法，作为更新动态长网页片段的入口。

# --- Project-specific Imports ---
from exporter import HtmlExporter

class ExportToHtmlWrapperMixin:
    """
    一个 Mixin 类，包含一个包装方法，用于触发“更新长网页片段”的操作。
    """
    def export_to_html_wrapper(self):
        """
        “更新长网页片段”菜单项的槽函数。

        此方法获取通用的输出目录，如果成功，则直接调用特定的
        片段导出函数 `HtmlExporter.export_to_html`。
        """
        # 1. 获取通用的输出目录
        output_dir = self._get_common_output_dir()
        
        # 2. 如果成功获取目录，则执行特定的片段导出函数
        if output_dir:
            HtmlExporter.export_to_html(self, output_dir)