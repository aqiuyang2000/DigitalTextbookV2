# D:\projects\singlepage\hotspot_editor\tools\tool_extract_p_words.py (已优化默认参数)
import fitz
import re
from PySide6.QtCore import Qt, QRect, QSettings
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QApplication, QMessageBox, QWidget, QFormLayout,
    QLineEdit, QLabel, QComboBox
)

from tools.base_tool import AbstractPdfTool
from commands import BatchAddHotspotsCommand
from utils import create_default_data


# --- *** 核心修改 1/4: 让 PWordsOptionsWidget 接收 DPI 参数 *** ---
class PWordsOptionsWidget(QWidget):
    """
    为"P类单词提取器"提供用户可配置选项的UI控件。
    """

    def __init__(self, parent=None, current_dpi=150):  # <-- 增加 current_dpi 参数
        super().__init__(parent)
        layout = QFormLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.link_type_combo = QComboBox()
        self.link_type_combo.addItems(["本地文件", "链接 (URL)"])
        self.link_type_map = {"本地文件": "file", "链接 (URL)": "url"}
        self.link_type_combo.setCurrentIndex(0)

        # --- *** 核心修改 2/4: 根据 DPI 计算默认值 *** ---
        base_width = 385
        base_height = 28
        base_adjustment = 30

        # 根据DPI计算缩放比例
        if current_dpi == 300:
            scale = 2
        elif current_dpi == 600:
            scale = 4
        else:  # 默认为 150 DPI
            scale = 1

        # 使用计算出的默认值初始化 QLineEdit
        self.pattern_input = QLineEdit("p. *")
        self.custom_width_input = QLineEdit(str(base_width * scale))
        self.custom_height_input = QLineEdit(str(base_height * scale))
        self.x_offset_input = QLineEdit("0")
        self.y_offset_input = QLineEdit("0")
        self.height_adjust_input = QLineEdit(str(base_adjustment * scale))

        for editor in [self.custom_width_input, self.custom_height_input, self.height_adjust_input]:
            editor.setValidator(QIntValidator(0, 9999))
        for editor in [self.x_offset_input, self.y_offset_input]:
            editor.setValidator(QIntValidator(-9999, 9999))

        layout.addRow(QLabel("热区默认类型:"), self.link_type_combo)
        layout.addRow(QLabel("查找文本:"), self.pattern_input)
        layout.addRow(QLabel("固定宽度:"), self.custom_width_input)
        layout.addRow(QLabel("固定高度:"), self.custom_height_input)
        layout.addRow(QLabel("X 轴偏移:"), self.x_offset_input)
        layout.addRow(QLabel("Y 轴偏移:"), self.y_offset_input)
        layout.addRow(QLabel("P类高度调整:"), self.height_adjust_input)

    def get_values(self) -> dict:
        # ... (此方法保持不变) ...
        selected_text = self.link_type_combo.currentText()
        return {
            'link_type': self.link_type_map[selected_text],
            'pattern': self.pattern_input.text(),
            'custom_width': self.custom_width_input.text(),
            'custom_height': self.custom_height_input.text(),
            'x_offset': self.x_offset_input.text(),
            'y_offset': self.y_offset_input.text(),
            'height_adjustment': self.height_adjust_input.text()
        }


class ExtractPWordsTool(AbstractPdfTool):
    name = "P类单词热区提取器"
    description = (
        "根据指定的文本模式（默认为'p. *'）批量查找并创建热区。\n\n"
        "用户可以自定义生成热区的尺寸、偏移量，并对特殊的'p. *'模式进行上下文分析和高度调整，以适应段落间隔。"
    )

    # --- *** 核心修改 3/4: 在 get_options_widget 中读取 DPI 设置 *** ---
    def get_options_widget(self, main_window) -> QWidget:
        # 从 QSettings 读取当前保存的 DPI 值
        settings = QSettings("MyCompany", "HotspotEditor")
        current_dpi = settings.value("pdf/resolution_dpi", 150, type=int)

        # 将读取到的 DPI 值传递给 PWordsOptionsWidget
        return PWordsOptionsWidget(current_dpi=current_dpi)

    # --- *** 核心修改 4/4: 确保 run 和 _get_text_pattern_hotspots 保持不变 *** ---
    # 这两个方法已经使用了动态 scale_factor，因此无需再次修改。
    # 我们只贴出 run 方法以示完整性，其内容与之前修复后的一致。
    def run(self, main_window):
        # ... (此方法的所有内容都保持不变) ...
        session = main_window.active_session
        if not session or not session.source_pdf_path:
            QMessageBox.warning(main_window, "操作无效", "此工具仅适用于从PDF文件导入的页面。")
            return

        def to_int(text_value, default_val):
            return int(text_value) if text_value and text_value.lstrip('-').isdigit() else default_val

        link_type = self.options.get('link_type', 'file')
        pattern = self.options.get('pattern', 'p. *').strip()
        if not pattern:
            QMessageBox.warning(main_window, "输入错误", "查找的文本模式不能为空。")
            return

        custom_width = to_int(self.options.get('custom_width'), None)
        custom_height = to_int(self.options.get('custom_height'), None)
        x_offset = to_int(self.options.get('x_offset'), 0)
        y_offset = to_int(self.options.get('y_offset'), 0)
        height_adjustment = to_int(self.options.get('height_adjustment'), 30)

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
        page_index = 0
        success, result = self._get_text_pattern_hotspots(
            session.source_pdf_path, page_index, pattern,
            custom_width, custom_height, x_offset, y_offset, height_adjustment,
            scale_factor=scale_factor
        )
        QApplication.restoreOverrideCursor()

        if not success:
            QMessageBox.critical(main_window, "提取失败", result)
            return

        reply = QMessageBox.question(main_window, "确认创建",
                                     f"成功识别到 {len(result)} 个匹配项。\n是否为所有匹配项创建热区？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        hotspots_to_add = []
        for hotspot_data in result:
            q_rect = hotspot_data['rect']
            pos = {'x': q_rect.x(), 'y': q_rect.y()}
            rect = {'w': q_rect.width(), 'h': q_rect.height()}
            data = create_default_data()
            data['description'] = hotspot_data.get('description', '')
            data['hotspot_type'] = link_type
            hotspots_to_add.append({
                'pos': pos, 'rect': rect, 'type': 'rectangle', 'data': data
            })

        command = BatchAddHotspotsCommand(session.scene, session.viewer, main_window, hotspots_to_add)
        main_window.active_session.undo_stack.push(command)
        QMessageBox.information(main_window, "操作成功", f"已成功创建 {len(hotspots_to_add)} 个热区。")

    def _get_text_pattern_hotspots(self, pdf_path, page_num, pattern, custom_width, custom_height, x_offset, y_offset,
                                   height_adjustment, scale_factor):
        # ... (此方法的所有内容都保持不变) ...
        doc = None
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            return False, f"无法打开PDF文件: {e}"
        if not (0 <= page_num < len(doc)):
            if doc: doc.close()
            return False, f"页码 {page_num + 1} 超出范围"
        page = doc[page_num]
        found_rects_pdf = []
        if pattern.lower() == "p. *":
            words = page.get_text("words")
            if not words:
                doc.close();
                return False, "页面上未检测到任何文本。"
            i = 0
            while i < len(words) - 1:
                current_word, next_word = words[i], words[i + 1]
                if current_word[4].lower() == "p." and next_word[4].isdigit() and current_word[6] == next_word[6]:
                    rect1 = fitz.Rect(current_word[:4]);
                    rect2 = fitz.Rect(next_word[:4])
                    found_rects_pdf.append(rect1 | rect2);
                    i += 2
                else:
                    i += 1
        else:
            found_rects_pdf = page.search_for(pattern)
        if not found_rects_pdf:
            doc.close()
            return False, f"在页面 {page_num + 1} 上未找到文本 '{pattern}'。"
        final_rects_pixels = [fitz.Rect(r * scale_factor) for r in found_rects_pdf]
        rect_ids_to_extend = set()
        if pattern.lower() == "p. *":
            columns = [];
            tolerance = 10
            for rect in sorted(final_rects_pixels, key=lambda r: r.x0):
                placed = False
                for col in columns:
                    if abs(rect.x0 - col[0].x0) < tolerance:
                        col.append(rect);
                        placed = True;
                        break
                if not placed: columns.append([rect])
            if not final_rects_pixels:
                doc.close();
                return False, "未找到矩形。"
            avg_height = sum(r.height for r in final_rects_pixels) / len(final_rects_pixels)
            for col in columns:
                col.sort(key=lambda r: r.y0, reverse=True)
                for i, current_rect in enumerate(col):
                    if i < len(col) - 1:
                        next_rect_above = col[i + 1]
                        y_diff = current_rect.y0 - next_rect_above.y0
                        if y_diff >= 2 * avg_height: rect_ids_to_extend.add(id(current_rect))
        hotspots = []
        for rect in final_rects_pixels:
            offset_rect_px = fitz.Rect(rect)
            offset_rect_px.x0 += x_offset;
            offset_rect_px.y0 += y_offset
            offset_rect_px.x1 += x_offset;
            offset_rect_px.y1 += y_offset
            final_w_px = custom_width if custom_width is not None else offset_rect_px.width
            final_h_px = custom_height if custom_height is not None else offset_rect_px.height
            if pattern.lower() == "p. *" and id(rect) in rect_ids_to_extend:
                final_h_px += height_adjustment
            final_x_px = offset_rect_px.x1 - final_w_px
            final_y_px = offset_rect_px.y1 - final_h_px
            q_rect_px = QRect(int(final_x_px), int(final_y_px), int(final_w_px), int(final_h_px))
            pdf_rect_to_extract = fitz.Rect(
                final_x_px / scale_factor, final_y_px / scale_factor,
                (final_x_px + final_w_px) / scale_factor, (final_y_px + final_h_px) / scale_factor
            )
            extracted_text = page.get_textbox(pdf_rect_to_extract)
            clean_text = re.sub(r'\s+', ' ', extracted_text).strip()
            if pattern.lower() == "p. *":
                clean_text = re.sub(r'p\.\s*\d+\s*', '', clean_text, flags=re.IGNORECASE).strip()
            hotspot = {"rect": q_rect_px, "description": clean_text}
            hotspots.append(hotspot)
        if doc:
            doc.close()
        return True, hotspots