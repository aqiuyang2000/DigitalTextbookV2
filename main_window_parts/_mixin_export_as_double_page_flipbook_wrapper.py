# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_export_as_double_page_flipbook_wrapper.py
#
# 功能: 提供 export_as_double_page_flipbook_wrapper 方法，作为导出双页画册的入口。

# --- Project-specific Imports ---
from exporter_flip import export_as_modular_flipbook

class ExportAsDoublePageFlipbookWrapperMixin:
    """
    一个 Mixin 类，包含一个包装方法，用于触发“导出为双页画册”的操作。
    """
    def export_as_double_page_flipbook_wrapper(self):
        """
        “导出为双页画册”菜单项的槽函数。

        这是一个包装器 (wrapper) 方法。它不包含任何复杂的逻辑，
        其唯一职责是调用通用的导出执行器 `_run_export`，并将
        实际的导出函数 `export_as_modular_flipbook` 作为参数传递给它。

        这种模式将通用的检查（如项目是否保存）和特定的导出操作解耦。
        """
        # 调用通用导出执行器，并将特定的导出函数作为参数传入
        self._run_export(export_as_modular_flipbook)