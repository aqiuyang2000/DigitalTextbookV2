# FILE: _command_paste.py
#
# 功能: 定义 PasteCommand，用于支持粘贴热区操作的撤销/重做。

from PySide6.QtGui import QUndoCommand
from PySide6.QtCore import QPointF

# 动态导入，避免循环依赖
try:
    from graphics_items import ResizableRectItem, ResizableEllipseItem
except ImportError:
    ResizableRectItem = type('ResizableRectItem', (object,), {})
    ResizableEllipseItem = type('ResizableEllipseItem', (object,), {})


class PasteCommand(QUndoCommand):
    """
    用于撤销/重做粘贴一个或多个热区项操作的命令。
    """

    def __init__(self, scene, viewer, main_window, paste_data: list, position: QPointF, parent=None):
        """
        初始化粘贴命令。

        Args:
            scene (QGraphicsScene): 目标场景。
            viewer (PhotoViewer): 关联的视图。
            main_window (HotspotEditor): 主窗口实例。
            paste_data (list): 包含要粘贴的热区信息的字典列表。
            position (QPointF): 粘贴的基准位置。
        """
        super().__init__("粘贴热区", parent)
        self.scene = scene
        self.viewer = viewer
        self.main_window = main_window
        self.paste_data = paste_data
        self.position = position
        self.pasted_items = []  # 存储粘贴创建的项

    def undo(self):
        """
        撤销操作：从场景中移除所有粘贴的项。
        """
        for item in self.pasted_items:
            self.scene.removeItem(item)
        self.pasted_items.clear()

        # 发出信号以更新属性面板等UI
        if self.scene:
            self.scene.selectionChanged.emit()

    def redo(self):
        """
        重做或首次执行操作：在场景中创建并添加粘贴的项。
        """
        # 清除当前选择，并将新粘贴的项设置为选中
        self.scene.clearSelection()
        bounds = self.scene.sceneRect()
        session = self.main_window.get_session_by_viewer(self.viewer)

        # 如果 self.pasted_items 不为空，说明是重做操作，直接重新添加项
        if self.pasted_items:
            for item in self.pasted_items:
                self.scene.addItem(item)
                item.setSelected(True)
            if self.scene:
                self.scene.selectionChanged.emit()
            return

        # 首次执行：根据粘贴数据创建项
        for i, data in enumerate(self.paste_data):
            # 计算新项的位置（可以稍微偏移以避免完全重叠）
            new_pos = self.position + QPointF(i * 10, i * 10)

            # 确定形状类型
            shape_class = ResizableRectItem if data['type'] == 'rectangle' else ResizableEllipseItem

            # 创建热区项
            hotspot = shape_class(data['rect'], bounds=bounds, viewer=self.viewer)
            hotspot.setPos(new_pos)

            # 复制数据并生成新的ID
            new_item_data = data['data'].copy()
            if session:
                new_item_data['id'] = self.main_window.generate_new_hotspot_id(session)

            hotspot.setData(0, new_item_data)
            hotspot.setPen(self.main_window.get_hotspot_pen())
            hotspot.setBrush(self.main_window.get_hotspot_brush())

            # 添加到场景并设置为选中
            self.scene.addItem(hotspot)
            hotspot.setSelected(True)
            self.pasted_items.append(hotspot)

        # 发出信号以更新属性面板等UI
        if self.scene:
            self.scene.selectionChanged.emit()