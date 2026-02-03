# D:\projects\singlepage\hotspot_editor\tools\tool_extract_tables.py (已修复签名)
import os
import fitz
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMessageBox, QWidget, QFormLayout,
    QComboBox, QLabel, QSpinBox, QFrame
)

from tools.base_tool import AbstractPdfTool
from commands import BatchAddHotspotsCommand
from utils import create_default_data


class TableOptionsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        self.link_type_combo = QComboBox()
        self.link_type_combo.addItems(["本地文件", "链接 (URL)"])
        self.link_type_map = {"本地文件": "file", "链接 (URL)": "url"}
        self.link_type_combo.setCurrentIndex(0)
        layout.addRow(QLabel("热区默认类型:"), self.link_type_combo)
        separator = QFrame(frameShape=QFrame.HLine, frameShadow=QFrame.Sunken)
        layout.addRow(separator)
        self.x_tolerance_spin = QSpinBox()
        self.x_tolerance_spin.setRange(0, 100)
        self.x_tolerance_spin.setValue(5)
        self.y_tolerance_spin = QSpinBox()
        self.y_tolerance_spin.setRange(0, 100)
        self.y_tolerance_spin.setValue(5)
        self.v_merge_spin = QSpinBox()
        self.v_merge_spin.setRange(0, 100)
        self.v_merge_spin.setValue(0)
        self.h_merge_spin = QSpinBox()
        self.h_merge_spin.setRange(0, 100)
        self.h_merge_spin.setValue(0)
        layout.addRow(QLabel("<b>智能合并设置:</b>"))
        layout.addRow("横坐标偏差数:", self.x_tolerance_spin)
        layout.addRow("纵坐标偏差数:", self.y_tolerance_spin)
        layout.addRow("纵向合并数:", self.v_merge_spin)
        layout.addRow("横向合并数:", self.h_merge_spin)
        self.v_merge_spin.valueChanged.connect(self.on_v_merge_changed)
        self.h_merge_spin.valueChanged.connect(self.on_h_merge_changed)
    def on_v_merge_changed(self, value):
        if value > 0:
            self.h_merge_spin.blockSignals(True)
            self.h_merge_spin.setValue(0)
            self.h_merge_spin.blockSignals(False)
    def on_h_merge_changed(self, value):
        if value > 0:
            self.v_merge_spin.blockSignals(True)
            self.v_merge_spin.setValue(0)
            self.v_merge_spin.blockSignals(False)
    def get_values(self) -> dict:
        selected_text = self.link_type_combo.currentText()
        return {
            'link_type': self.link_type_map[selected_text],
            'x_tolerance': self.x_tolerance_spin.value(),
            'y_tolerance': self.y_tolerance_spin.value(),
            'v_merge_count': self.v_merge_spin.value(),
            'h_merge_count': self.h_merge_spin.value(),
        }


class AutoHotspotFromTablesTool(AbstractPdfTool):
    name = "从表格自动创建热区"
    description = (
        "自动扫描PDF页面中的表格，并为每个单元格创建热区。\n\n"
        "支持智能合并功能，可按行或列将指定的单元格数量合并成一个更大的热区。"
    )

    # --- *** 核心修复: 添加 main_window 参数以匹配基类签名 *** ---
    def get_options_widget(self, main_window) -> QWidget:
        return TableOptionsWidget()

    def run(self, main_window):
        session = main_window.active_session
        if not session or not session.source_pdf_path:
            QMessageBox.warning(main_window, "操作无效", "此工具仅适用于从PDF文件导入的页面。")
            return

        link_type = self.options.get('link_type', 'file')
        x_tolerance = self.options.get('x_tolerance', 5)
        y_tolerance = self.options.get('y_tolerance', 5)
        v_merge_count = self.options.get('v_merge_count', 0)
        h_merge_count = self.options.get('h_merge_count', 0)

        try:
            image_pixel_width = session.scene.width()
            doc = fitz.open(session.original_multipage_pdf_path or session.source_pdf_path)
            page = doc.load_page(session.source_page_index)
            page_point_width = page.rect.width
            doc.close()
            if page_point_width == 0:
                raise ValueError("PDF页面宽度为0，无法计算缩放比例。")
            scale_factor = image_pixel_width / page_point_width
        except Exception as e:
            QMessageBox.critical(main_window, "计算失败", f"无法计算正确的缩放比例: {e}")
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        success, initial_cells = self._get_table_cell_info(session.source_pdf_path, 0)
        if not success:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(main_window, "提取失败", initial_cells)
            return

        final_hotspots = self._merge_hotspots(
            initial_cells, v_merge_count, h_merge_count, x_tolerance, y_tolerance
        )
        QApplication.restoreOverrideCursor()

        hotspot_count = len(final_hotspots)
        if hotspot_count == 0:
            QMessageBox.information(main_window, "提示", "未能从表格中提取任何有效的单元格。")
            return

        reply = QMessageBox.question(main_window, "确认创建",
                                     f"成功处理并生成了 {hotspot_count} 个热区。\n是否确认创建？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        hotspots_to_add = []
        for cell_info in final_hotspots:
            pos = {'x': cell_info['x'] * scale_factor, 'y': cell_info['y'] * scale_factor}
            rect = {'w': cell_info['width'] * scale_factor, 'h': cell_info['height'] * scale_factor}
            data = create_default_data()
            data['description'] = cell_info.get('text', '')
            data['hotspot_type'] = link_type
            hotspots_to_add.append({'pos': pos, 'rect': rect, 'type': 'rectangle', 'data': data})

        command = BatchAddHotspotsCommand(session.scene, session.viewer, main_window, hotspots_to_add)
        main_window.active_session.undo_stack.push(command)
        QMessageBox.information(main_window, "操作成功", f"已成功创建 {hotspot_count} 个热区。")

    def _merge_hotspots(self, cells, v_merge_count, h_merge_count, x_tolerance, y_tolerance):
        if v_merge_count <= 0 and h_merge_count <= 0:
            return cells
        merged_cells = []
        if v_merge_count > 0:
            columns = []
            if not cells: return []
            sorted_cells = sorted(cells, key=lambda c: (c['x'], c['y']))
            current_column = [sorted_cells[0]]
            for cell in sorted_cells[1:]:
                if abs(cell['x'] - current_column[0]['x']) < x_tolerance:
                    current_column.append(cell)
                else:
                    columns.append(current_column)
                    current_column = [cell]
            columns.append(current_column)
            for column in columns:
                column.sort(key=lambda c: c['y'])
                i = 0
                while i < len(column):
                    chunk = column[i:i + v_merge_count]
                    if not chunk: break
                    min_x = min(c['x'] for c in chunk)
                    min_y = min(c['y'] for c in chunk)
                    max_x1 = max(c['x'] + c['width'] for c in chunk)
                    max_y1 = max(c['y'] + c['height'] for c in chunk)
                    combined_text = " ".join(c['text'] for c in chunk if c['text'])
                    merged_cells.append({
                        "x": min_x, "y": min_y,
                        "width": max_x1 - min_x, "height": max_y1 - min_y,
                        "text": combined_text
                    })
                    i += v_merge_count
        elif h_merge_count > 0:
            rows = []
            if not cells: return []
            sorted_cells = sorted(cells, key=lambda c: (c['y'], c['x']))
            current_row = [sorted_cells[0]]
            for cell in sorted_cells[1:]:
                if abs(cell['y'] - current_row[0]['y']) < y_tolerance:
                    current_row.append(cell)
                else:
                    rows.append(current_row)
                    current_row = [cell]
            rows.append(current_row)
            for row in rows:
                row.sort(key=lambda c: c['x'])
                i = 0
                while i < len(row):
                    chunk = row[i:i + h_merge_count]
                    if not chunk: break
                    min_x = min(c['x'] for c in chunk)
                    min_y = min(c['y'] for c in chunk)
                    max_x1 = max(c['x'] + c['width'] for c in chunk)
                    max_y1 = max(c['y'] + c['height'] for c in chunk)
                    combined_text = " ".join(c['text'] for c in chunk if c['text'])
                    merged_cells.append({
                        "x": min_x, "y": min_y,
                        "width": max_x1 - min_x, "height": max_y1 - min_y,
                        "text": combined_text
                    })
                    i += h_merge_count
        return merged_cells

    def _get_table_cell_info(self, pdf_path, page_num):
        try:
            doc = fitz.open(pdf_path)
            if not 0 <= page_num < len(doc):
                doc.close()
                return False, f"错误: 页面索引 {page_num} 超出范围。"
            page = doc[page_num]
            tables = page.find_tables()
            all_cells_info = []
            if tables.tables:
                for table in tables:
                    if not table.cells: continue
                    for cell_bbox in table.cells:
                        if cell_bbox is None: continue
                        cell_text = page.get_textbox(cell_bbox)
                        x0, y0, x1, y1 = cell_bbox
                        all_cells_info.append({
                            "x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0,
                            "text": cell_text.strip() if cell_text else ""
                        })
            doc.close()
            if not all_cells_info:
                return False, f"在页面 {page_num + 1} 上未能自动识别出任何表格。"
            return True, all_cells_info
        except Exception as e:
            return False, f"处理PDF时发生错误: {e}"