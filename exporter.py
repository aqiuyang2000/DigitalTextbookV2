# D:\projects\singlepage\hotspot_editor\exporter.py
#
# 功能: 这是 HtmlExporter 的最终组合文件。
#       它导入了所有功能性的 Mixin 类，并通过多重继承将它们
#       组合成一个功能完整的 HtmlExporter 类。

# --- 基础类别 ---
from exporter_parts._base import HtmlExporterBase

# --- Mixin 模块 ---
from exporter_parts._mixin_get_hotspot_style_context import GetHotspotStyleContextMixin
from exporter_parts._mixin_generate_outline_html import GenerateOutlineHtmlMixin
from exporter_parts._mixin_generate_media_tag import GenerateMediaTagMixin
from exporter_parts._mixin_collect_hotspots_for_session import CollectHotspotsForSessionMixin
from exporter_parts._mixin_export_to_html import ExportToHtmlMixin
from exporter_parts._mixin_export_as_dynamic_page import ExportAsDynamicPageMixin
from exporter_parts._mixin_export_as_single_page_flipbook import ExportAsSinglePageFlipbookMixin
from exporter_parts._mixin_export_single_flipbook_page import ExportSingleFlipbookPageMixin


class HtmlExporter(
    # --- 继承顺序 ---
    HtmlExporterBase,
    GetHotspotStyleContextMixin,
    GenerateOutlineHtmlMixin,
    GenerateMediaTagMixin,
    CollectHotspotsForSessionMixin,
    ExportToHtmlMixin,
    ExportAsDynamicPageMixin,
    ExportAsSinglePageFlipbookMixin,
    ExportSingleFlipbookPageMixin
):
    """
    通过多重继承组合所有功能性 Mixin 类，构建最终的 HtmlExporter。
    此类中的所有方法都应为 classmethod，以便在 Mixin 内部可以
    通过 `cls.` 调用其他方法。
    """
    pass