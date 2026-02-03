# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_load_image_path.py
#
# 功能: 提供 _load_image_path 方法，用于加载单个图像文件并创建新的编辑会话。

import os

# --- Qt Imports ---
from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QSizePolicy

# --- Project-specific Imports ---
from image_editing_session import ImageEditingSession
from photo_viewer import PhotoViewer
from graphics_items import ResizableRectItem, ResizableEllipseItem
from utils import create_default_data


class LoadImagePathMixin:
    """
    一个 Mixin 类，包含加载单个图片并创建完整编辑会话的核心方法。
    """

    def _load_image_path(self, file_path: str, hotspots_data: list = None,
                         next_hotspot_id_start: int = 0, insertion_index: int = -1,
                         source_pdf_path: str = None, original_multipage_pdf_path: str = None,
                         source_page_index: int = 0):
        """
        加载指定的图像文件，为其创建一个新的 ImageEditingSession 和 PhotoViewer，
        并将其添加到主窗口的布局和数据结构中。
        """
        if not file_path or not os.path.exists(file_path):
            print(f"警告: _load_image_path 接收到无效的文件路径: {file_path}，已跳过。")
            return

        session = ImageEditingSession(
            file_path, self, next_hotspot_id_start,
            source_pdf_path=source_pdf_path,
            original_multipage_pdf_path=original_multipage_pdf_path,
            source_page_index=source_page_index,
            parent=self
        )

        if not session.load_image():
            return

        viewer = PhotoViewer(session.scene, self)
        session.viewer = viewer
        # --- *** 核心修改 1/2: 调整 SizePolicy *** ---
        # 允许 viewer 在 QStackedWidget 中自由缩放
        viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # --- 连接信号 (这部分代码与上次修复后保持一致) ---
        session.undo_stack.cleanChanged.connect(
            lambda is_clean: self.set_dirty(not is_clean), self
        )
        session.undo_stack.canUndoChanged.connect(self.update_ui_for_active_session, self)
        session.undo_stack.canRedoChanged.connect(self.update_ui_for_active_session, self)
        viewer.deleteRequested.connect(self.delete_selected_hotspot)
        viewer.copyRequested.connect(self.copy_selected_hotspots)
        viewer.pasteRequested.connect(self.paste_hotspots)
        session.scene.selectionChanged.connect(self.update_hotspot_info)

        if hotspots_data:
            pen = self.get_hotspot_pen()
            brush = self.get_hotspot_brush()
            for hotspot in hotspots_data:
                shape_class = ResizableEllipseItem if hotspot['type'] == 'ellipse' else ResizableRectItem
                rect_data, pos_data = hotspot['rect'], hotspot['pos']
                item = shape_class(0, 0, rect_data['w'], rect_data['h'], bounds=session.scene.sceneRect(),
                                   viewer=viewer)
                item.setPos(QPointF(pos_data['x'], pos_data['y']))

                data = hotspot.get('data') or create_default_data()
                if not data.get('id'):
                    hotspot_id = session.get_next_hotspot_id()
                    temp_page_id = len(self.sessions)
                    data['id'] = f"{self.project_id}_p{temp_page_id}_h{hotspot_id}"

                item.setData(0, data)
                item.setPen(pen)
                item.setBrush(brush)
                session.scene.addItem(item)

        # --- *** 核心修改 2/2: 修改页面添加逻辑 *** ---
        # 将新创建的会话和视图插入到正确的位置
        if insertion_index != -1 and 0 <= insertion_index <= len(self.sessions):
            # 使用 QStackedWidget.insertWidget
            self.page_stack.insertWidget(insertion_index, viewer)
            self.sessions.insert(insertion_index, session)
            self.viewer_widgets.insert(insertion_index, viewer)
        else:
            # 使用 QStackedWidget.addWidget
            self.page_stack.addWidget(viewer)
            self.sessions.append(session)
            self.viewer_widgets.append(viewer)

        viewer.mousePressEvent = lambda event, v=viewer: self.handle_viewer_press(event, v)