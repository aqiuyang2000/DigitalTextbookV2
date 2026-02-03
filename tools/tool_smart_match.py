# FILE: tools/tool_smart_match.py (已修复自动加载)
import sys
import os
import csv
import shutil
from pathlib import Path
from difflib import SequenceMatcher
from collections import Counter

from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QHeaderView, QProgressBar, QLabel, QMessageBox, QComboBox
)
from PySide6.QtGui import QUndoStack
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QThread, Signal, Qt, QUrl

try:
    import whisper
except ImportError:
    whisper = None

from tools.base_tool import AbstractPdfTool
from commands import DataChangeCommand
from graphics_items import AbstractResizableItem


# --- 相似度匹配算法 (保持不变) ---
def word_similarity(s1, s2):
    # ... (此函数代码保持不变) ...
    s1_clean = str(s1).strip().lower()
    s2_clean = str(s2).strip().lower()
    if not s1_clean or not s2_clean: return 0.0
    w1 = s1_clean.split(); w2 = s2_clean.split()
    if s1_clean == s2_clean: return 1.0
    if Counter(w1) == Counter(w2): return 0.9
    common = set(w1) & set(w2)
    word_overlap = len(common) / max(len(set(w1)), len(set(w2))) if max(len(set(w1)), len(set(w2))) > 0 else 0
    seq_ratio = SequenceMatcher(None, s1_clean, s2_clean).ratio()
    return max(word_overlap, seq_ratio)


# --- Whisper 后台工作线程 (保持不变) ---
class WhisperWorker(QThread):
    # ... (此类代码保持不变) ...
    status_updated = Signal(str)
    progress_updated = Signal(int)
    result_ready = Signal(tuple)
    finished = Signal()
    def __init__(self, files_to_process, model_size="base"):
        super().__init__()
        self.mp3_files = files_to_process
        self.model_size = model_size
        self.model = None
    def run(self):
        if whisper is None:
            self.status_updated.emit("错误: openai-whisper 库未安装。")
            return
        try:
            self.status_updated.emit(f"正在加载 Whisper '{self.model_size}' 模型...")
            self.model = whisper.load_model(self.model_size)
            self.status_updated.emit("模型加载成功，准备开始转录。")
        except Exception as e:
            self.status_updated.emit(f"模型加载失败: {e}")
            return
        total_files = len(self.mp3_files)
        for index, file_path in enumerate(self.mp3_files):
            current_progress = int(((index + 1) / total_files) * 100)
            file_name = os.path.basename(file_path)
            self.status_updated.emit(f"正在处理 ({index + 1}/{total_files}): {file_name}")
            try:
                result = self.model.transcribe(os.path.abspath(file_path), fp16=False)
                content = result["text"].strip()
                self.result_ready.emit((index + 1, content, file_path))
            except Exception as e:
                self.result_ready.emit((index + 1, f"错误: {e}", file_path))
            self.progress_updated.emit(current_progress)
        self.status_updated.emit("所有文件处理完毕！")
        self.finished.emit()


# --- CSV 编辑与匹配的主对话框 ---
class CsvEditorDialog(QDialog):
    def __init__(self, main_window, media_dir_path):
        super().__init__(main_window)
        self.main_window = main_window
        self.media_dir = media_dir_path
        self.csv_path = os.path.join(self.media_dir, "content_index.csv")
        self.whisper_thread = None

        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._player.setAudioOutput(self._audio_output)

        self.setWindowTitle("智能语音匹配工具")
        self.setMinimumSize(900, 600)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)

        self.main_layout = QVBoxLayout(self)
        self.top_bar_layout = QHBoxLayout()
        self.btn_regenerate_csv = QPushButton("重新生成CSV")
        self.btn_direct_match = QPushButton("加载CSV并匹配")
        self.btn_export_csv = QPushButton("保存CSV修改")
        self.btn_smart_match = QPushButton("开始智能匹配")
        self.status_label = QLabel("请选择操作。")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.result_table = QTableWidget()
        self.setup_table()
        self.model_combo = QComboBox()
        self.model_combo.addItems(["base", "small", "medium", "large-v2"])
        self.model_combo.setCurrentText("large-v2")
        self.top_bar_layout.addWidget(QLabel("Whisper模型:"))
        self.top_bar_layout.addWidget(self.model_combo)
        self.top_bar_layout.addWidget(self.btn_regenerate_csv)
        self.top_bar_layout.addSpacing(20)
        self.top_bar_layout.addWidget(self.btn_direct_match)
        self.top_bar_layout.addStretch()
        self.top_bar_layout.addWidget(self.btn_export_csv)
        self.top_bar_layout.addWidget(self.btn_smart_match)
        self.main_layout.addLayout(self.top_bar_layout)
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.progress_bar)
        self.main_layout.addWidget(self.result_table)

        self.btn_regenerate_csv.clicked.connect(self.regenerate_csv)
        self.btn_direct_match.clicked.connect(self.load_csv_and_prepare_match)
        self.btn_export_csv.clicked.connect(self.export_to_csv)
        self.btn_smart_match.clicked.connect(self.run_smart_match)

        self.update_button_states()

        # --- *** 核心修复: 如果CSV文件已存在，则自动加载它 *** ---
        if os.path.exists(self.csv_path):
            self.load_csv_and_prepare_match()
        # --- *** 修复结束 *** ---

    # ... (所有其他方法，如 setup_table, add_table_row 等，都保持不变) ...
    def setup_table(self):
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["No", "Content", "File Path", "播放"])
        header = self.result_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
    def add_table_row(self, row_data):
        row_pos = self.result_table.rowCount()
        self.result_table.insertRow(row_pos)
        for col, data in enumerate(row_data):
            item = QTableWidgetItem(data)
            if col != 1:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.result_table.setItem(row_pos, col, item)
        file_path = row_data[2] if len(row_data) > 2 else None
        if file_path and os.path.exists(file_path):
            play_button = QPushButton("▶️ Play")
            play_button.setToolTip(f"播放: {os.path.basename(file_path)}")
            play_button.clicked.connect(lambda checked=False, path=file_path: self.play_audio(path))
            self.result_table.setCellWidget(row_pos, 3, play_button)
    def play_audio(self, file_path):
        if self._player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self._player.stop()
        url = QUrl.fromLocalFile(file_path)
        self._player.setSource(url)
        self._player.play()
        self.status_label.setText(f"正在播放: {os.path.basename(file_path)}")
    def closeEvent(self, event):
        self._player.stop()
        super().closeEvent(event)
    def add_whisper_result_row(self, result_data):
        self.add_table_row([str(d) for d in result_data])
    def update_button_states(self, is_running=False, data_loaded=False):
        has_csv = os.path.exists(self.csv_path)
        can_regenerate = not is_running and whisper is not None
        self.model_combo.setEnabled(can_regenerate)
        self.btn_regenerate_csv.setEnabled(can_regenerate)
        self.btn_direct_match.setEnabled(not is_running and has_csv)
        self.btn_export_csv.setEnabled(not is_running and data_loaded)
        self.btn_smart_match.setEnabled(not is_running and data_loaded)
        if whisper is None:
            self.status_label.setText("警告: 未安装 openai-whisper 库，无法生成CSV。")
    def load_csv_and_prepare_match(self):
        if not os.path.exists(self.csv_path):
            QMessageBox.warning(self, "文件不存在", "资源目录下未找到 content_index.csv 文件。")
            return
        try:
            self.result_table.setRowCount(0)
            with open(self.csv_path, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                header = next(reader)
                for row_data in reader:
                    self.add_table_row(row_data[:3])
            self.result_table.setEditTriggers(QTableWidget.DoubleClicked)
            self.status_label.setText(
                f"已加载 {self.result_table.rowCount()} 条记录。您可以编辑 'Content' 后保存，或直接开始匹配。")
            self.update_button_states(data_loaded=True)
        except Exception as e:
            QMessageBox.critical(self, "读取失败", f"无法读取或解析CSV文件: {e}")
    def export_to_csv(self):
        try:
            with open(self.csv_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                headers = [self.result_table.horizontalHeaderItem(i).text() for i in range(3)]
                writer.writerow(headers)
                for row in range(self.result_table.rowCount()):
                    row_data = [self.result_table.item(row, col).text() for col in range(3)]
                    writer.writerow(row_data)
            self.status_label.setText(f"CSV文件已成功保存到: {self.csv_path}")
        except Exception as e:
            QMessageBox.critical(self, "保存失败", f"无法写入CSV文件: {e}")
    def regenerate_csv(self):
        mp3_files = sorted([str(p) for p in Path(self.media_dir).rglob("*.mp3")])
        if not mp3_files:
            QMessageBox.information(self, "未找到文件", "在资源目录中未找到任何 .mp3 文件。")
            return
        selected_model = self.model_combo.currentText()
        self.update_button_states(is_running=True)
        self.result_table.setRowCount(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.whisper_thread = WhisperWorker(mp3_files, model_size=selected_model)
        self.whisper_thread.status_updated.connect(self.status_label.setText)
        self.whisper_thread.progress_updated.connect(self.progress_bar.setValue)
        self.whisper_thread.result_ready.connect(self.add_whisper_result_row)
        self.whisper_thread.finished.connect(self.on_transcription_finished)
        self.whisper_thread.start()
    def on_transcription_finished(self):
        self.progress_bar.setVisible(False)
        self.result_table.setEditTriggers(QTableWidget.DoubleClicked)
        self.status_label.setText("转录完成！现在可以编辑 'Content' 列，然后保存或开始匹配。")
        self.update_button_states(data_loaded=True)
        self.export_to_csv()
    def run_smart_match(self):
        active_session = self.main_window.active_session
        if not active_session:
            QMessageBox.warning(self, "无活动页面", "请先确保有一个活动的编辑页面。")
            return
        hotspots = [item for item in active_session.scene.items() if isinstance(item, AbstractResizableItem)]
        if not hotspots:
            QMessageBox.warning(self, "无热区", "当前页面没有任何热区可供匹配。")
            return
        csv_data = [{"content": self.result_table.item(row, 1).text(), "path": self.result_table.item(row, 2).text()}
                    for row in range(self.result_table.rowCount())]
        if not csv_data:
            QMessageBox.warning(self, "无CSV数据", "表格中没有数据可用于匹配。")
            return
        QApplication.setOverrideCursor(Qt.WaitCursor)
        commands_to_execute = []
        try:
            for hotspot in hotspots:
                hotspot_data = hotspot.data(0)
                if not hotspot_data: continue
                hotspot_desc = hotspot_data.get('description', '')
                if not hotspot_desc: continue
                best_match_record = None
                highest_score = -1.0
                for record in csv_data:
                    score = word_similarity(hotspot_desc, record['content'])
                    if score > highest_score:
                        highest_score = score
                        best_match_record = record
                if best_match_record and highest_score > 0.5:
                    try:
                        output_dir = self.main_window._get_output_directory()
                        media_target_dir = os.path.join(output_dir, "media")
                        os.makedirs(media_target_dir, exist_ok=True)
                        source_file_path = best_match_record['path']
                        filename = os.path.basename(source_file_path)
                        destination_path = os.path.join(media_target_dir, filename)
                        if not os.path.exists(destination_path):
                            shutil.copy(source_file_path, destination_path)
                        old_data = hotspot.data(0)
                        new_data = old_data.copy()
                        new_data['hotspot_type'] = 'file'
                        if 'file_data' not in new_data: new_data['file_data'] = {}
                        new_data['file_data']['source_path'] = destination_path
                        command = DataChangeCommand(hotspot, old_data, new_data)
                        commands_to_execute.append(command)
                    except Exception as e:
                        print(f"处理文件 '{source_file_path}' 时出错: {e}")
                        continue
        finally:
            QApplication.restoreOverrideCursor()
        match_count = len(commands_to_execute)
        if match_count > 0:
            main_undo_stack = active_session.undo_stack
            main_undo_stack.beginMacro(f"智能匹配 {match_count} 个热区")
            for command in commands_to_execute:
                main_undo_stack.push(command)
            main_undo_stack.endMacro()
            QMessageBox.information(self, "匹配完成", f"成功为 {match_count} 个热区找到了匹配的音频链接。")
        else:
            QMessageBox.information(self, "匹配完成", "没有找到足够相似的音频进行匹配。")
        self.accept()


# --- 工具的主入口类 (保持不变) ---
class SmartMatchTool(AbstractPdfTool):
    # ... (此类代码保持不变) ...
    name = "智能语音匹配"
    description = "打开一个包含MP3的目录，自动生成文本，然后将音频文件与当前页面的热区进行智能匹配。"
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dialog = None
    def run(self, main_window):
        if self.dialog and self.dialog.isVisible():
            self.dialog.activateWindow()
            self.dialog.raise_()
            return
        if not main_window.project_path:
            QMessageBox.warning(main_window, "需要保存项目", "请先保存项目，以便确定媒体文件的存放位置。")
            return
        media_dir = QFileDialog.getExistingDirectory(main_window, "请选择包含MP3文件的资源目录")
        if not media_dir:
            return
        self.dialog = CsvEditorDialog(main_window, media_dir)
        self.dialog.finished.connect(self.on_dialog_finished)
        self.dialog.show()
    def on_dialog_finished(self):
        print("智能匹配对话框已关闭，清除引用。")
        self.dialog = None