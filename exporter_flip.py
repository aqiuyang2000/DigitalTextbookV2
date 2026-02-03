# FILE: exporter_flip.py (Corrected Final Assembler with Facade)
#
# 功能: 这是 ExporterFlip 模块的最终组合文件。
#       它首先在内部组装出功能完整的 ExporterFlip 类，
#       然后定义了与原始文件完全相同的公共函数接口。
#       这些公共函数作为“门面(Facade)”，将调用转发给内部的类方法，
#       从而在不影响外部调用的前提下，实现了内部结构的重构。

# --- 1. 内部实现: 组装 ExporterFlip 类 ---

# 1a. 导入基础和 Mixin 部分
from exporter_flip_parts._base import ExporterFlipBase
from exporter_flip_parts._mixin_generate_media_tag import GenerateMediaTagMixin
from exporter_flip_parts._mixin_generate_outline import GenerateOutlineMixin
from exporter_flip_parts._mixin_export_as_modular_flipbook import ExportAsModularFlipbookMixin
from exporter_flip_parts._mixin_export_double_page_fragment import ExportDoublePageFragmentMixin

# 1b. 组装内部核心类
class _ExporterFlip(
    ExporterFlipBase,
    GenerateMediaTagMixin,
    GenerateOutlineMixin,
    ExportAsModularFlipbookMixin,
    ExportDoublePageFragmentMixin
):
    """
    内部实现类，通过多重继承组合了所有功能。
    以"_"开头表示这是本模块的私有实现细节。
    """
    pass


# --- 2. 公共接口: 提供与重构前完全相同的函数 ---

def export_as_modular_flipbook(parent_window, project_path: str):
    """
    公共接口函数。
    它将调用转发给内部 _ExporterFlip 类的同名方法。
    """
    return _ExporterFlip.export_as_modular_flipbook(parent_window, project_path)

def export_double_page_fragment(parent_window, output_dir):
    """
    公共接口函数。
    它将调用转发给内部 _ExporterFlip 类的同名方法。
    """
    return _ExporterFlip.export_double_page_fragment(parent_window, output_dir)