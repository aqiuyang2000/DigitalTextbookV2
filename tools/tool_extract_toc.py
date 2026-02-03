# D:\projects\singlepage\hotspot_editor\tools\tool_extract_toc.py (已修复签名)
import re
import fitz
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMessageBox, QApplication, QWidget, QFormLayout,
                               QLineEdit, QLabel)

from tools.base_tool import AbstractPdfTool


class TocOptionsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.page_range_edit = QLineEdit("1")
        self.page_range_edit.setPlaceholderText("例如: 1 或 3-5")
        layout.addRow(QLabel("输入目录页码范围:"), self.page_range_edit)

    def get_values(self):
        return {'page_range': self.page_range_edit.text()}


class ExtractTocTool(AbstractPdfTool):
    name = "从当前页提取目录"
    description = (
        "智能分析指定PDF页面范围的文本布局，提取目录结构，并追加到提纲面板。\n\n"
        "本工具会按顺序尝试多种策略（关键词、布局等）以获得最佳结果。"
    )

    # --- *** 核心修复: 添加 main_window 参数以匹配基类签名 *** ---
    def get_options_widget(self, main_window) -> QWidget:
        return TocOptionsWidget()

    def run(self, main_window):
        session = main_window.active_session
        if not session:
            QMessageBox.warning(main_window, "操作无效", "没有活动的页面。")
            return

        self.main_window = main_window
        original_pdf_path = session.original_multipage_pdf_path

        if not original_pdf_path:
            print("警告: 未找到精确的原始PDF路径，尝试备用猜测逻辑...")
            if session.source_pdf_path:
                original_pdf_path = self._find_original_pdf_fallback(session.source_pdf_path)
            else:
                QMessageBox.warning(main_window, "操作无效", "此页面不是从PDF生成的，无法使用此工具。")
                return

        if not original_pdf_path or not os.path.exists(original_pdf_path):
            QMessageBox.critical(main_window, "错误",
                                 f"无法找到用于分析的原始多页PDF文件。\n检查路径: {original_pdf_path or '无'}")
            return

        page_range_str = self.options.get('page_range', '1').strip()
        try:
            pages_to_process = self._parse_page_range(page_range_str)
            if not pages_to_process: raise ValueError("页码范围无效")
        except ValueError as e:
            QMessageBox.warning(main_window, "输入错误", f"页码范围格式不正确: {e}")
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        lines = self._process_pdf_pages_to_lines(original_pdf_path, pages_to_process)

        if "错误：" in str(lines):
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(main_window, "文本提取失败", str(lines))
            return

        strategies = [self._strategy_keywords, self._strategy_layout]
        toc_tree = []
        for strategy in strategies:
            print(f"--- 尝试策略: {strategy.__name__} ---")
            toc_tree = strategy(lines)
            if toc_tree:
                print(f"--- 策略 {strategy.__name__} 成功！---")
                break
            else:
                print(f"--- 策略 {strategy.__name__} 失败。---")

        QApplication.restoreOverrideCursor()

        if not toc_tree:
            main_window.statusBar().showMessage("所有策略都未能识别出有效的目录结构。", 4000)
            return

        current_outline = main_window.outline_data
        current_outline.extend(toc_tree)
        main_window.outline_widget.populate_tree(current_outline)
        main_window._on_outline_changed(current_outline)
        if not main_window.outline_widget.isVisible():
            main_window.toggle_outline_action.setChecked(True)
            main_window.toggle_outline_panel(True)

        QMessageBox.information(main_window, "提取成功", f"成功提取并追加了 {len(toc_tree)} 个一级目录项到提纲。")

    def _parse_page_range(self, range_str: str) -> list[int]:
        pages = []
        # --- 修正: 更健壮的页码范围解析 ---
        parts = range_str.replace(" ", "").split(',')
        for part in parts:
            if not part: continue
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    if start <= end:
                        pages.extend(range(start - 1, end))
                except (ValueError, IndexError):
                    pass
            else:
                try:
                    pages.append(int(part) - 1)
                except ValueError:
                    pass
        return sorted(list(set(p for p in pages if p >= 0)))

    def _find_original_pdf_fallback(self, single_page_pdf_path: str) -> str | None:
        try:
            if not hasattr(self, 'main_window') or not self.main_window.project_path: return None
            # 改进了路径猜测逻辑，使其更健壮
            workspace_dir = os.path.dirname(os.path.dirname(os.path.dirname(single_page_pdf_path)))
            sources_dir = os.path.join(workspace_dir, "sources")
            if not os.path.isdir(sources_dir): return None

            # 尝试从 session 中获取原始文件名信息
            session_filename_base = None
            for s in self.main_window.sessions:
                if s.source_pdf_path == single_page_pdf_path:
                    if s.original_multipage_pdf_path:
                        session_filename_base = os.path.splitext(os.path.basename(s.original_multipage_pdf_path))[0]
                    break

            if not session_filename_base: return None

            for file in os.listdir(sources_dir):
                if file.lower().endswith('.pdf'):
                    if os.path.splitext(file)[0] == session_filename_base:
                        return os.path.join(sources_dir, file)
            return None
        except Exception:
            return None

    def _process_pdf_pages_to_lines(self, pdf_path, page_indices):
        all_lines_data = []
        try:
            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()
            doc = fitz.open(stream=pdf_data, filetype="pdf")

            for page_num in page_indices:
                if not (0 <= page_num < len(doc)): continue
                page = doc[page_num]
                blocks = page.get_text("dict")["blocks"]
                for b in blocks:
                    if b['type'] == 0:
                        for l in b["lines"]:
                            spans = l['spans']
                            if not spans: continue
                            text = "".join(s['text'] for s in spans).strip()
                            if not text or "目录" in text or "contents" in text.lower(): continue
                            text = re.sub(r'\s+', ' ', text).strip()
                            text = re.sub(r'[\. ]{3,}', ' ', text).strip()
                            all_lines_data.append({
                                'text': text, 'x': l['bbox'][0], 'y': l['bbox'][1], 'size': spans[0]['size']
                            })
            doc.close()
            return all_lines_data
        except Exception as e:
            return f"错误：处理PDF时发生未知异常: {e}"

    def _parse_line(self, line_text):
        line_text = line_text.strip()
        parts = re.split(r'\s+', line_text)
        page_num, title = None, line_text
        if len(parts) > 1 and parts[-1].isdigit():
            page_num = int(parts[-1])
            title = " ".join(parts[:-1]).strip()
        return title, page_num

    def _strategy_keywords(self, lines_data):
        toc_tree = []
        current_parent = None
        parent_keywords_re = re.compile(
            r'^\s*(Unit|Module|第.*[单元章课])', re.IGNORECASE
        )
        for line in lines_data:
            title, page_num = self._parse_line(line['text'])
            if parent_keywords_re.match(title):
                node = {'title': title, 'page': page_num, 'children': []}
                toc_tree.append(node)
                current_parent = node
            elif current_parent:
                if page_num is None: continue
                child_node = {'title': title, 'page': page_num, 'children': []}
                current_parent['children'].append(child_node)
        self._post_process_tree(toc_tree)
        return toc_tree

    def _strategy_layout(self, lines_data):
        if not lines_data: return []
        merged_lines = []
        i = 0
        while i < len(lines_data):
            current_line = lines_data[i]
            title, page_num = self._parse_line(current_line['text'])
            if page_num is None and i + 1 < len(lines_data):
                next_line = lines_data[i + 1]
                if next_line['text'].isdigit() and abs(next_line['y'] - current_line['y']) < 20:
                    current_line['title'] = title
                    current_line['page'] = int(next_line['text'])
                    merged_lines.append(current_line)
                    i += 2
                    continue
            current_line['title'] = title
            current_line['page'] = page_num
            merged_lines.append(current_line)
            i += 1
        toc_tree = []
        parent_stack = [({'children': toc_tree}, -1)]
        for line in merged_lines:
            if not line['title'] or line['page'] is None: continue
            node = {'title': line['title'], 'page': line['page'], 'children': []}
            indent = line['x']
            while indent <= parent_stack[-1][1]:
                parent_stack.pop()
            parent_stack[-1][0]['children'].append(node)
            if len(parent_stack) < 2:
                parent_stack.append((node, indent))
        self._post_process_tree(toc_tree)
        return toc_tree

    def _post_process_tree(self, nodes):
        for node in nodes:
            if node['page'] is None and node['children']:
                first_child_page = next((child['page'] for child in node['children'] if child['page'] is not None),
                                        None)
                if first_child_page:
                    node['page'] = first_child_page
            if node['children']:
                self._post_process_tree(node['children'])

    def _build_tree_fallback(self, pdf_path):
        return []