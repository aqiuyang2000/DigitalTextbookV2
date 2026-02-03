# D:\projects\singlepage\hotspot_editor\tools\tool_extract_all_words.py (已修复签名)
import fitz
import re

from PySide6.QtCore import Qt, QRect
from PySide6.QtWidgets import (
    QApplication, QMessageBox, QWidget, QFormLayout,
    QComboBox, QCheckBox, QLabel
)

from tools.base_tool import AbstractPdfTool
from commands import BatchAddHotspotsCommand
from utils import create_default_data


class AllWordsOptionsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.link_type_combo = QComboBox()
        self.link_type_combo.addItems(["本地文件", "链接 (URL)"])
        self.link_type_map = {"本地文件": "file", "链接 (URL)": "url"}
        self.link_type_combo.setCurrentIndex(0)
        self.exclude_chinese_check = QCheckBox("排除所有中文字、词")
        self.exclude_chinese_check.setChecked(True)
        self.exclude_english_check = QCheckBox("排除所有英文字母单词")
        self.exclude_english_check.setChecked(False)
        layout.addRow(QLabel("热区默认类型:"), self.link_type_combo)
        layout.addRow(self.exclude_chinese_check)
        layout.addRow(self.exclude_english_check)

    def get_values(self) -> dict:
        selected_text = self.link_type_combo.currentText()
        return {
            'link_type': self.link_type_map[selected_text],
            'exclude_chinese': self.exclude_chinese_check.isChecked(),
            'exclude_english': self.exclude_english_check.isChecked(),
        }


class ExtractAllWordsTool(AbstractPdfTool):
    name = "从所有单词创建热区"
    description = (
        "自动扫描当前 PDF 页面中的所有独立单词，并为每一个单词创建一个热区。\n\n"
        "可自定义排除中文或英文，并指定生成热区的默认类型。"
    )

    # --- *** 核心修复: 添加 main_window 参数以匹配基类签名 *** ---
    def get_options_widget(self, main_window) -> QWidget:
        """返回自定义的选项UI控件实例。"""
        # (即使当前未使用 main_window，也要保持签名一致)
        return AllWordsOptionsWidget()

    def run(self, main_window):
        session = main_window.active_session
        if not session or not session.source_pdf_path:
            QMessageBox.warning(main_window, "操作无效", "此工具仅适用于从PDF文件导入的页面。")
            return

        link_type = self.options.get('link_type', 'file')
        exclude_chinese = self.options.get('exclude_chinese', True)
        exclude_english = self.options.get('exclude_english', False)

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
        success, result = self._get_word_hotspots(
            session.source_pdf_path,
            page_index,
            scale_factor=scale_factor,
            exclude_chinese=exclude_chinese,
            exclude_english=exclude_english
        )
        QApplication.restoreOverrideCursor()

        if not success:
            QMessageBox.critical(main_window, "提取失败", result)
            return

        word_count = len(result)
        if word_count == 0:
            QMessageBox.information(main_window, "提示", "根据您的排除选项，没有找到符合条件的单词。")
            return

        reply = QMessageBox.question(main_window, "确认创建",
                                     f"成功识别到 {word_count} 个符合条件的单词。\n是否为它们创建热区？",
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
        QMessageBox.information(main_window, "操作成功", f"已成功为 {word_count} 个单词创建了热区。")

    def _get_word_hotspots(self, pdf_path: str, page_num: int, scale_factor: float,
                           exclude_chinese: bool, exclude_english: bool):
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            return False, f"无法打开PDF文件: {e}"
        if not (0 <= page_num < len(doc)):
            doc.close()
            return False, f"页码 {page_num + 1} 超出范围"
        page = doc[page_num]
        words = page.get_text("words")
        doc.close()
        if not words:
            return False, "在当前页面上未检测到任何单词。"
        RE_CHINESE = re.compile(r'[\u4e00-\u9fa5]')
        RE_ENGLISH_LIKE = re.compile(r"^[a-zA-Z0-9'.-]+$")
        hotspots = []
        for w in words:
            x0, y0, x1, y1, text = w[:5]
            text = text.strip()
            if not text: continue
            is_chinese = bool(RE_CHINESE.search(text))
            is_english = bool(RE_ENGLISH_LIKE.match(text))
            if exclude_chinese and is_chinese: continue
            if exclude_english and is_english: continue
            pixel_rect = QRect(
                int(x0 * scale_factor),
                int(y0 * scale_factor),
                int((x1 - x0) * scale_factor),
                int((y1 - y0) * scale_factor)
            )
            if pixel_rect.width() < 1 or pixel_rect.height() < 1: continue
            hotspot_info = { "rect": pixel_rect, "description": text }
            hotspots.append(hotspot_info)
        return True, hotspots