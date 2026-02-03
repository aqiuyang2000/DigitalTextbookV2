# FILE: _mixin_import_hotspots_from_excel.py

import openpyxl
import os  # <-- 核心修改 1/3: 导入os模块
from utils import create_default_data
from ._mixin_copy_file_with_conflict_resolution import ExcelProcessorCopyFileMixin


class ExcelProcessorImportHotspotsFromExcelMixin:
    """
    为 ExcelProcessor 添加从 Excel 文件批量导入热区数据的功能。
    """

    @staticmethod
    def import_hotspots_from_excel(file_path: str, media_dir: str) -> list:
        """
        从 Excel 文件批量导入热区数据。
        """
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        header_row = [cell.value for cell in sheet[1]]
        try:
            header_map = {
                "id": header_row.index("id"), "shape": header_row.index("绘制形状"),
                "x": header_row.index("x"), "y": header_row.index("y"),
                "w": header_row.index("宽"), "h": header_row.index("高"),
                "link_type": header_row.index("类型"), "link_file": header_row.index("链接/文件"),
                "target": header_row.index("打开方式"), "description": header_row.index("说明"),
            }
        except ValueError as e:
            print(f"Excel表头格式不正确，缺少列: {e}")
            return None

        hotspots_to_add = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not any(row):
                continue

            try:
                data = create_default_data()
                pos = {}
                rect = {}

                shape_type = row[header_map["shape"]]
                pos['x'] = float(row[header_map["x"]])
                pos['y'] = float(row[header_map["y"]])
                rect['w'] = float(row[header_map["w"]])
                rect['h'] = float(row[header_map["h"]])

                data['description'] = row[header_map["description"]] or ""
                data['hotspot_type'] = row[header_map["link_type"]]
                link_or_file_path = row[header_map["link_file"]]

                # --- *** 核心修改 2/3: 根据链接/文件路径自动匹配图标类型 *** ---
                icon_type = 'default'
                if link_or_file_path:
                    _, ext = os.path.splitext(link_or_file_path.lower())
                    if ext in ['.mp3', '.wav', '.ogg', '.m4a']:
                        icon_type = 'audio'
                    elif ext in ['.mp4', '.mov', '.webm', '.avi']:
                        icon_type = 'video'
                    elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.bmp']:
                        icon_type = 'image'
                    elif ext in ['.html', '.htm']:
                        icon_type = 'link'
                    elif ext in ['.pdf']:
                        icon_type = 'pdf'
                    elif data['hotspot_type'] == 'url':  # 如果没有匹配的扩展名，但类型是URL，则默认为链接
                        icon_type = 'link'

                data['icon_type'] = icon_type
                # --- *** 修改结束 *** ---

                if data['hotspot_type'] == 'url':
                    data['url_data']['url'] = link_or_file_path
                    data['url_data']['target'] = row[header_map["target"]]

                elif data['hotspot_type'] == 'file':
                    source_file_path = link_or_file_path
                    if not source_file_path:
                        print(f"警告：类型为'file'的行链接文件路径为空，已跳过 - Row: {row}")
                        continue

                    # --- *** 核心修改 3/3: 确保ExcelProcessorCopyFileMixin的调用方式正确 *** ---
                    final_path = ExcelProcessorCopyFileMixin._copy_file_with_conflict_resolution(
                        source_file_path, media_dir
                    )

                    if final_path:
                        data['file_data']['source_path'] = final_path
                        data['file_data']['display'] = row[header_map["target"]]
                    else:
                        print(f"警告：源文件 '{source_file_path}' 不存在或无法复制，已跳过 - Row: {row}")
                        continue

                hotspots_to_add.append({
                    'pos': pos,
                    'rect': rect,
                    'type': shape_type,
                    'data': data
                })

            except (ValueError, TypeError, IndexError) as e:
                print(f"警告：处理行时数据格式错误，已跳过 - Row: {row}, Error: {e}")
                continue

        return hotspots_to_add