# D:\projects\singlepage\hotspot_editor\main_window_parts\_base.py (已修复导入错误)
#
# 功能: 定义 HotspotEditor 的基类 HotspotEditorBase。
#       这个文件包含唯一的 __init__ 方法，负责初始化所有实例变量，
#       为所有后续的 Mixin 功能模块提供共享的上下文和状态。

import atexit
import hashlib
import uuid

# --- Qt Imports ---
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QSplitter
)
from PySide6.QtGui import QUndoStack
from PySide6.QtCore import Qt

# --- Project-specific Imports (核心修复：将相对导入改为绝对导入) ---
from preview_server import PreviewServer
from pdf_processor import PdfProcessor
from project_manager import ProjectManager
from outline_editor_widget import OutlineEditorWidget


class HotspotEditorBase(QMainWindow):
    """
    HotspotEditor 的基础类。

    这个类只包含 __init__ 方法，用于设置窗口、初始化所有核心组件和实例变量。
    它被设计为所有其他功能性 Mixin 类的基础，确保所有 Mixin 都能访问
    到一个统一的、初始状态正确的实例 (`self`)。
    """

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1600, 900)

        # --- 核心服务与管理器初始化 ---
        self.preview_server = PreviewServer()
        atexit.register(self.preview_server.stop)  # 确保程序退出时服务器能停止

        self.pdf_processor = PdfProcessor()
        self.project_manager = ProjectManager()

        # --- 主窗口布局初始化 ---
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_splitter = QSplitter(Qt.Horizontal, self)
        self.layout = QHBoxLayout(self.central_widget)
        self.layout.addWidget(self.main_splitter)

        # --- 状态与数据容器初始化 ---
        # (这部分内容与您提供的完全相同，无需修改)
        # 会话管理
        self.sessions = []
        self.viewer_widgets = []
        self.active_session_index = -1

        # 撤销/重做栈
        self.project_undo_stack = QUndoStack(self)

        self.project_undo_stack.canUndoChanged.connect(self.update_ui_for_active_session)
        self.project_undo_stack.canRedoChanged.connect(self.update_ui_for_active_session)

        # 项目属性
        self.project_path = None
        self.project_id = None
        self.clipboard = []
        self.is_dirty = False

        # 提纲/目录数据
        self.outline_widget = OutlineEditorWidget(self)
        self.outline_data = []

        # UI 内部状态
        self._is_scrolling_programmatically = False

        # UI 控件的占位符 (这些将在 setup_ui mixin 中被实际创建和赋值)
        self.scroll_area = None
        self.scroll_area_widget_contents = None
        self.pages_layout = None
        self.shape_combo = None
        self.info_label = None
        self.controls_layout = None
        self.btn_prev = None
        self.btn_next = None
        self.lbl_page_info = None
        self.txt_page_input = None
        self.btn_delete_page = None
        self.btn_export_all = None
        self.btn_preview = None
        self.chk_preview_dual = None
        self.chk_preview_single = None
        self.chk_preview_scroll = None
        self.btn_update_all_fragments = None
        self.btn_batch_import = None
        self.btn_export_hotspot_data = None
        self.btn_export_current_page_data = None
        self.btn_pdf_toolbox = None
        self.btn_batch_scale = None
        self.txt_id = None
        self.txt_description = None
        self.txt_x = None
        self.txt_y = None
        self.txt_width = None
        self.txt_height = None
        self.type_combo = None
        self.stacked_widget = None
        self.txt_url = None
        self.combo_target = None
        self.target_map = {}
        self.target_map_reverse = {}
        self.btn_upload = None
        self.lbl_filename = None
        self.combo_file_display = None
        self.txt_popup_width = None
        self.txt_popup_height = None
        self.lbl_popup_width = None
        self.lbl_popup_height = None
        self.edit_menu = None
        self.undo_action = None
        self.redo_action = None
        self.toggle_outline_action = None
        self.export_flipbook_action = None
        self.export_single_flipbook_action = None
        self.export_dynamic_page_action = None
        self.export_all_action = None
        self.update_flipbook_fragment_action = None
        self.update_single_flipbook_fragment_action = None
        self.update_dynamic_fragment_action = None

        # --- 初始化流程调用 ---
        # 注意: 这些方法将在最终组合的类中被 Mixin 提供
        self.setup_ui()
        self.create_menus()
        self.connect_signals()
        self.update_ui_for_active_session()
        self._load_last_project()