# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_export_as_single_page_flipbook_wrapper.py
#
# 功能: 提供 export_as_single_page_flipbook_wrapper 方法，作为导出单页画册的入口。

# --- Project-specific Imports ---
from exporter import HtmlExporter

class ExportAsSinglePageFlipbookWrapperMixin:
    """
    一个 Mixin 类，包含一个包装方法，用于触发“导出为单页画册”的操作。
    """
    def export_as_single_page_flipbook_wrapper(self):
        """
        “导出为单页画册 (左右翻)”菜单项的槽函数。

        这是一个包装器 (wrapper) 方法，调用通用的导出执行器 `_run_export`，
        并将实际的导出函数 `HtmlExporter.export_as_single_page_flipbook` 
        作为参数传递给它。
        """
        # 调用通用导出执行器，并将特定的导出函数作为参数传入
        self._run_export(HtmlExporter.export_as_single_page_flipbook)