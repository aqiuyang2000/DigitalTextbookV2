# FILE: image_editing_session.py (Corrected)
from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QMessageBox
from PySide6.QtGui import QPixmap, QUndoStack
from PySide6.QtCore import QObject


class ImageEditingSession(QObject):
    """
    管理单个页面（图片）的所有状态，包括场景、撤销栈和元数据。
    继承自 QObject 以便能参与Qt的父子对象生命周期管理。
    """

    def __init__(self, image_path, main_window, next_hotspot_id_start=0,
                 source_pdf_path=None, original_multipage_pdf_path=None, source_page_index=0, parent=None):

        # *** 核心修复: 明确调用 QObject 的构造函数并传递 parent ***
        QObject.__init__(self, parent)

        print(
            f"DEBUG: ImageEditingSession.__init__ - original_multipage_pdf_path received: {original_multipage_pdf_path}")

        # --- 属性初始化 (保持不变) ---
        self.image_path = image_path
        self.main_window = main_window

        self.source_pdf_path = source_pdf_path
        self.original_multipage_pdf_path = original_multipage_pdf_path
        self.source_page_index = source_page_index

        self.scene = QGraphicsScene()
        self.undo_stack = QUndoStack(self)  # 将 self 作为 QUndoStack 的父对象
        self.pixmap_item = None
        self.viewer = None
        self.image_width = 0
        self.image_height = 0
        self._next_hotspot_id = next_hotspot_id_start

    def get_next_hotspot_id(self) -> int:
        """
        获取此会话内下一个可用的热区ID计数器，并自增。
        """
        current_id = self._next_hotspot_id
        self._next_hotspot_id += 1
        return current_id

    def load_image(self) -> bool:
        """
        从 self.image_path 加载图片并将其添加到场景中。
        返回 True 表示成功，False 表示失败。
        """
        try:
            # 使用 with open 读取可以更好地处理文件句柄
            with open(self.image_path, 'rb') as f:
                image_data = f.read()
            pixmap = QPixmap()
            if not pixmap.loadFromData(image_data):
                # 如果 Qt 无法解析图片数据
                raise IOError("QPixmap.loadFromData() failed.")
        except (IOError, FileNotFoundError) as e:
            QMessageBox.critical(None, "错误", f"无法加载或读取图片文件:\n{self.image_path}\n\n错误: {e}")
            return False

        if pixmap.isNull():
            QMessageBox.critical(None, "错误", f"加载的图片数据无效:\n{self.image_path}")
            return False

        self.image_width = pixmap.width()
        self.image_height = pixmap.height()

        # 如果场景中已有旧图片，先移除
        if self.pixmap_item:
            self.scene.removeItem(self.pixmap_item)

        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.pixmap_item.setFlag(QGraphicsPixmapItem.ItemIsSelectable, False)  # 图片本身不可选中
        self.scene.addItem(self.pixmap_item)

        # 设置场景的边界矩形与图片大小一致
        self.scene.setSceneRect(self.pixmap_item.boundingRect())
        return True