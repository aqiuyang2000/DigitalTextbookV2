# FILE: excel_processor.py
#
# 功能: 组合所有 ExcelProcessor 的功能，提供统一的导入接口

from excel_processor_parts._base import ExcelProcessorBase
from excel_processor_parts._mixin_copy_file_with_conflict_resolution import ExcelProcessorCopyFileMixin
from excel_processor_parts._mixin_import_from_excel import ExcelProcessorImportFromExcelMixin
from excel_processor_parts._mixin_export_to_excel import ExcelProcessorExportToExcelMixin
from excel_processor_parts._mixin_export_hotspots_to_excel import ExcelProcessorExportHotspotsToExcelMixin
from excel_processor_parts._mixin_export_single_page_hotspots_to_excel import ExcelProcessorExportSinglePageHotspotsToExcelMixin
from excel_processor_parts._mixin_import_hotspots_from_excel import ExcelProcessorImportHotspotsFromExcelMixin


class ExcelProcessor(
    ExcelProcessorBase,
    ExcelProcessorCopyFileMixin,
    ExcelProcessorImportFromExcelMixin,
    ExcelProcessorExportToExcelMixin,
    ExcelProcessorExportHotspotsToExcelMixin,
    ExcelProcessorExportSinglePageHotspotsToExcelMixin,
    ExcelProcessorImportHotspotsFromExcelMixin
):
    """
    完整的 Excel 处理器类，通过多继承组合所有功能。
    """
    pass