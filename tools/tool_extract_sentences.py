# D:\projects\singlepage\hotspot_editor\tools\tool_extract_sentences.py (已修复签名)
import fitz
import nltk
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMessageBox, QWidget, QFormLayout,
    QComboBox, QLabel
)

from tools.base_tool import AbstractPdfTool
from commands import BatchAddHotspotsCommand
from utils import create_default_data


class SentenceOptionsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.link_type_combo = QComboBox()
        self.link_type_combo.addItems(["本地文件", "链接 (URL)"])
        self.link_type_map = {"本地文件": "file", "链接 (URL)": "url"}
        self.link_type_combo.setCurrentIndex(0)
        layout.addRow(QLabel("热区默认类型:"), self.link_type_combo)

    def get_values(self) -> dict:
        selected_text = self.link_type_combo.currentText()
        return {
            'link_type': self.link_type_map[selected_text],
        }


class AutoHotspotFromSentencesTool(AbstractPdfTool):
    name = "从英文句子创建热区"
    description = "自动扫描当前 PDF 页面中的所有英文文本，使用NLTK库进行句子分割，并为每个句子（或其跨行部分）创建一个热区。\n\n注意：对非标准文本布局或图文混排页面，效果可能不佳。"

    # --- *** 核心修复: 添加 main_window 参数以匹配基类签名 *** ---
    def get_options_widget(self, main_window) -> QWidget:
        """返回自定义的选项UI控件实例。"""
        return SentenceOptionsWidget()

    def run(self, main_window):
        session = main_window.active_session
        if not session or not session.source_pdf_path:
            QMessageBox.warning(main_window, "操作无效", "此工具仅适用于从PDF文件导入的页面。")
            return

        link_type = self.options.get('link_type', 'file')

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
        success, result = self._extract_sentences_with_coords(session.source_pdf_path, 0)
        QApplication.restoreOverrideCursor()

        if not success:
            QMessageBox.critical(main_window, "提取失败", result)
            return

        sentence_parts_count = len(result)
        unique_sentences = len(set(item['sentence_id'] for item in result))
        reply = QMessageBox.question(main_window, "确认创建",
                                     f"成功识别到 {unique_sentences} 个句子，共计 {sentence_parts_count} 个文本片段（行）。\n是否为所有片段创建热区？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        hotspots_to_add = []
        for sentence_info in result:
            pos = {'x': sentence_info['x'] * scale_factor, 'y': sentence_info['y'] * scale_factor}
            rect = {'w': sentence_info['width'] * scale_factor, 'h': sentence_info['height'] * scale_factor}
            data = create_default_data()
            data['description'] = sentence_info.get('full_text', '')
            data['hotspot_type'] = link_type
            hotspots_to_add.append({'pos': pos, 'rect': rect, 'type': 'rectangle', 'data': data})

        command = BatchAddHotspotsCommand(session.scene, session.viewer, main_window, hotspots_to_add)
        main_window.active_session.undo_stack.push(command)
        QMessageBox.information(main_window, "操作成功", f"已成功创建 {len(hotspots_to_add)} 个热区。")

    def _extract_sentences_with_coords(self, pdf_path, page_num):
        try:
            doc = fitz.open(pdf_path)
            if not 0 <= page_num < len(doc):
                doc.close()
                return False, f"错误: 页面索引 {page_num} 超出范围。"
            page = doc[page_num]
            words = page.get_text("words")
            if not words:
                doc.close()
                return False, f"在页面 {page_num + 1} 上未找到任何文本。"
            words.sort(key=lambda w: (w[3], w[0]))
            full_text = " ".join(w[4] for w in words)
            sentences = nltk.sent_tokenize(full_text)
            all_sentence_parts_info = []
            word_idx = 0
            for sent_idx, sentence_text in enumerate(sentences):
                target_word_combo = "".join(sentence_text.replace(" ", ""))
                current_sentence_words = []
                buffer_word_combo = ""
                start_word_idx = word_idx
                while word_idx < len(words):
                    word_info = words[word_idx]
                    current_sentence_words.append(word_info)
                    buffer_word_combo += word_info[4]
                    word_idx += 1
                    if "".join(buffer_word_combo.split()) == target_word_combo:
                        break
                else:
                    word_idx = start_word_idx
                    print(f"警告：无法精确匹配句子 '{sentence_text}'，可能已被跳过。")
                    continue
                lines = {}
                for word_info in current_sentence_words:
                    line_key = round(word_info[1])
                    if line_key not in lines:
                        lines[line_key] = []
                    lines[line_key].append(fitz.Rect(word_info[:4]))
                part_num = 1
                for line_key in sorted(lines.keys()):
                    line_rects = lines[line_key]
                    if not line_rects: continue
                    final_rect = fitz.Rect(line_rects[0])
                    for r in line_rects[1:]:
                        final_rect.include_rect(r)
                    if final_rect.is_empty: continue
                    info = {
                        "sentence_id": sent_idx + 1, "part_num": part_num,
                        "x": final_rect.x0, "y": final_rect.y0,
                        "width": final_rect.width, "height": final_rect.height,
                        "full_text": sentence_text.strip()
                    }
                    all_sentence_parts_info.append(info)
                    part_num += 1
            doc.close()
            if not all_sentence_parts_info:
                return False, f"在页面 {page_num + 1} 上未能成功提取和映射句子。"
            return True, all_sentence_parts_info
        except Exception as e:
            return False, f"处理PDF时发生错误: {e}"