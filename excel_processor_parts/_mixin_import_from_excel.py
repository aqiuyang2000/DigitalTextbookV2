# FILE: _mixin_import_from_excel.py
#
# 功能: 为 ExcelProcessor 添加从 Excel 导入大纲数据的功能

import openpyxl


class ExcelProcessorImportFromExcelMixin:
    """
    为 ExcelProcessor 添加从 Excel 文件导入大纲数据的功能。
    """

    @staticmethod
    def import_from_excel(file_path: str) -> list:
        """
        从 Excel 文件导入大纲数据。

        Args:
            file_path (str): Excel 文件路径

        Returns:
            list: 大纲数据列表
        """
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        outline_data = []
        parent_stack = [outline_data]

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not any(row):
                continue

            try:
                level, title, page = row[0], row[1], row[2]
                if not isinstance(level, int) or level < 1 or title is None or page is None:
                    continue

                node = {'title': str(title), 'page': int(page), 'children': []}

                if level > len(parent_stack):
                    level = len(parent_stack)

                while len(parent_stack) > level:
                    parent_stack.pop()

                parent_list = parent_stack[-1]
                parent_list.append(node)
                parent_stack.append(node['children'])

            except (ValueError, TypeError) as e:
                print(f"警告：处理行时出错，已跳过 - Row: {row}, Error: {e}")
                continue

        return outline_data