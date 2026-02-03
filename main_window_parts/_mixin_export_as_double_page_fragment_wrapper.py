# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_export_as_double_page_fragment_wrapper.py
#
# 功能: 提供 export_as_double_page_fragment_wrapper 方法，作为更新双页画册片段的入口。

# --- Project-specific Imports ---
from exporter_flip import export_double_page_fragment

class ExportAsDoublePageFragmentWrapperMixin:
    """
    一个 Mixin 类，包含一个包装方法，用于触发“更新双页画册片段”的操作。
    """
    def export_as_double_page_fragment_wrapper(self):
        """
        “更新双页画册片段”菜单项的槽函数。

        这是一个包装器 (wrapper) 方法。它首先获取通用的输出目录，
        如果获取成功，则直接调用特定的片段导出函数 
        `export_double_page_fragment`。
        
        注意：在原始代码中，这里使用了另一个执行器 `_get_common_output_dir`，
        但为了更清晰地分离，我们可以将其逻辑直接包含或调用一个更简单的执行器。
        为了与原始代码保持一致，我们将调用一个辅助方法来获取目录。
        """
        # 1. 获取通用的输出目录
        output_dir = self._get_common_output_dir()
        
        # 2. 如果成功获取目录，则执行特定的片段导出函数
        if output_dir:
            export_double_page_fragment(self, output_dir)
            
# 在更精细的分解中，_get_common_output_dir 也可以被看作一个独立的执行器。
# 但为了保持与原始代码相似的结构，这里直接调用。
# 另一个替代方案是创建一个 _run_fragment_export 执行器，如下所示：
#
# from exporter_flip import export_double_page_fragment
# class ExportAsDoublePageFragmentWrapperMixin:
#     def export_as_double_page_fragment_wrapper(self):
#         self._run_fragment_export(export_double_page_fragment)
#
# 这个替代方案更符合之前完整导出的模式。原始代码的实现则稍微有些不同。
# 这里我们选择与原始代码 `export_as_double_page_fragment_wrapper` 实现
# 更接近的逻辑。