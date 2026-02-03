# photo_viewer.py
from PySide6.QtWidgets import QGraphicsView, QGraphicsRectItem, QMenu, QSizePolicy
from PySide6.QtGui import QPen, QBrush, QMouseEvent, QCursor, QWheelEvent, QKeyEvent, QKeySequence, QPainter, QTransform
from PySide6.QtCore import Qt, QRectF, QPointF, Signal, QTimer
from graphics_items import ResizableRectItem, ResizableEllipseItem, AbstractResizableItem
from utils import create_default_data


class PhotoViewer(QGraphicsView):
    deleteRequested = Signal()
    copyRequested = Signal()
    pasteRequested = Signal(QPointF)

    def __init__(self, scene, main_window, parent=None):
        super().__init__(scene, parent)
        self.main_window = main_window
        self.start_pos = None
        self.current_rect_item = None
        self._zoom = 1.0

        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)
        self.setRenderHint(QPainter.Antialiasing)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.setStyleSheet("PhotoViewer { border: 2px solid transparent; }")

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def set_active(self, is_active):
        if is_active:
            self.setStyleSheet("PhotoViewer { border: 2px solid dodgerblue; }")
        else:
            self.setStyleSheet("PhotoViewer { border: 2px solid transparent; }")

    def fit_to_height(self):
        if self.scene() and not self.scene().sceneRect().isEmpty():
            scene_rect = self.scene().sceneRect()
            view_rect = self.viewport().rect()

            if scene_rect.height() == 0:
                return

            scale_factor = view_rect.height() / scene_rect.height()

            self.setTransform(QTransform())
            self.scale(scale_factor, scale_factor)
            self._zoom = scale_factor

            for item in self.scene().items():
                if isinstance(item, AbstractResizableItem):
                    item.updateForViewTransform()

    def fit_to_view(self):
        if self.scene() and not self.scene().sceneRect().isEmpty():
            self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)
            self._zoom = self.transform().m11()
            for item in self.scene().items():
                if isinstance(item, AbstractResizableItem):
                    item.updateForViewTransform()

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag);
            self.viewport().setCursor(Qt.ClosedHandCursor)
            fake_event = QMouseEvent(event.type(), event.position(), Qt.LeftButton, Qt.LeftButton, event.modifiers())
            super().mousePressEvent(fake_event);
            return

        items_at_pos = self.items(event.position().toPoint())
        can_draw = not any(isinstance(item, AbstractResizableItem) for item in items_at_pos)

        if event.button() == Qt.LeftButton and can_draw:
            self.start_pos = self.mapToScene(event.position().toPoint())
            self.current_rect_item = QGraphicsRectItem();
            self.current_rect_item.setPen(QPen(Qt.red, 2, Qt.DashLine));
            self.scene().addItem(self.current_rect_item)

    def wheelEvent(self, event: QWheelEvent):
        zoom_factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
        new_zoom = self._zoom * zoom_factor
        if new_zoom < 0.01 or new_zoom > 10: return
        old_pos = self.mapToScene(event.position().toPoint())
        self._zoom = new_zoom
        self.scale(zoom_factor, zoom_factor)
        new_pos = self.mapToScene(event.position().toPoint())
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())
        for item in self.scene().items():
            if isinstance(item, AbstractResizableItem):
                item.updateForViewTransform()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.start_pos:
            end_pos = self.mapToScene(event.position().toPoint())
            rect = QRectF(self.start_pos, end_pos).normalized()
            self.current_rect_item.setRect(rect)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.NoDrag)
            self.viewport().setCursor(Qt.ArrowCursor)
            fake_event = QMouseEvent(event.type(), event.position(), Qt.LeftButton, Qt.NoButton, event.modifiers())
            super().mouseReleaseEvent(fake_event)
            return

        if self.start_pos and self.current_rect_item:
            end_pos = self.mapToScene(event.position().toPoint())
            rect = QRectF(self.start_pos, end_pos).normalized()
            if rect.width() > 10 and rect.height() > 10:
                bounds = self.scene().sceneRect()
                shape_type = self.window().get_current_shape()
                shape_class = ResizableRectItem if shape_type == "Rectangle" else ResizableEllipseItem
                hotspot_item = shape_class(0, 0, rect.width(), rect.height(), bounds=bounds, viewer=self)
                hotspot_item.setPos(rect.topLeft())
                hotspot_item.setPen(self.main_window.get_hotspot_pen())
                hotspot_item.setBrush(self.main_window.get_hotspot_brush())
                main_win = self.window()
                session = main_win.get_session_by_viewer(self)
                if session:
                    new_id = main_win.generate_new_hotspot_id(session)
                    data = create_default_data()
                    data['id'] = new_id
                    hotspot_item.setData(0, data)
                else:
                    hotspot_item.setData(0, create_default_data())

                self.scene().addItem(hotspot_item)

            self.scene().removeItem(self.current_rect_item)
            self.current_rect_item = None
            self.start_pos = None
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if event.matches(QKeySequence.Delete):
            if self.scene().selectedItems(): self.deleteRequested.emit(); event.accept()
        elif event.matches(QKeySequence.Copy):
            if self.scene().selectedItems(): self.copyRequested.emit(); event.accept()
        elif event.matches(QKeySequence.Paste):
            paste_pos = self.mapToScene(self.mapFromGlobal(QCursor.pos()))
            self.pasteRequested.emit(paste_pos);
            event.accept()
        # --- *** 核心修改：添加对 Ctrl+A (SelectAll) 的处理 *** ---
        elif event.matches(QKeySequence.SelectAll):
            if self.scene():
                for item in self.scene().items():
                    # 确保只选中我们自定义的热区项
                    if isinstance(item, AbstractResizableItem):
                        item.setSelected(True)
                event.accept()  # 告诉系统我们已经处理了这个事件
        # ---
        elif event.key() == Qt.Key_PageDown:
            self.main_window.next_page()
            event.accept()
        elif event.key() == Qt.Key_PageUp:
            self.main_window.previous_page()
            event.accept()
        else:
            super().keyPressEvent(event)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        main_window = self.window()
        copy_action = menu.addAction("复制");
        paste_action = menu.addAction("粘贴");
        delete_action = menu.addAction("删除")
        has_selection = bool(self.scene().selectedItems());
        has_clipboard_data = bool(main_window.clipboard)
        copy_action.setEnabled(has_selection);
        delete_action.setEnabled(has_selection);
        paste_action.setEnabled(has_clipboard_data)
        copy_action.triggered.connect(self.copyRequested.emit)
        delete_action.triggered.connect(self.deleteRequested.emit)
        paste_action.triggered.connect(lambda: self.pasteRequested.emit(self.mapToScene(event.pos())))
        menu.exec(event.globalPos())