# FILE: _command_batch_add_hotspots.py
#
# 功能: 定义 BatchAddHotspotsCommand，用于支持批量添加热区的撤销/重做。

from PySide6.QtGui import QUndoCommand
from PySide6.QtCore import QPointF

# 动态导入，避免循环依赖，并使模块更独立
# 这些类型仅用于类型提示，但在运行时需要
try:
    from graphics_items import ResizableRectItem, ResizableEllipseItem
except ImportError:
    # 在某些情况下（如单元测试），可能无法直接导入
    # 为了代码健壮性，我们允许它在没有这些类的情况下也能定义
    ResizableRectItem = type('ResizableRectItem', (object,), {})
    ResizableEllipseItem = type('ResizableEllipseItem', (object,), {})


class BatchAddHotspotsCommand(QUndoCommand):
    """
    用于撤销/重做批量添加热区操作的命令。
    """

    def __init__(self, scene, viewer, main_window, hotspots_data, parent=None):
        """
        初始化批量添加命令。

        Args:
            scene (QGraphicsScene): 目标场景。
            viewer (PhotoViewer): 关联的视图。
            main_window (HotspotEditor): 主窗口实例。
            hotspots_data (list): 包含要添加的热区信息的字典列表。
            parent (QUndoCommand, optional): 父命令。
        """
        super().__init__("批量导入热区", parent)
        self.scene = scene
        self.viewer = viewer
        self.main_window = main_window
        self.hotspots_data = hotspots_data
        self.added_items = []  # 用于存储此命令创建的图形项

    def undo(self):
        """
        撤销操作：从场景中移除所有由此命令添加的热区项。
        """
        for item in self.added_items:
            self.scene.removeItem(item)
        # 清空列表，以便在重做时能重新创建它们
        self.added_items.clear()

        # 撤销后可能需要更新UI，例如计数器，但这比较复杂，暂时简化处理。
        # 一个完整的实现可能会在这里发射一个信号。
        if self.scene:
            self.scene.selectionChanged.emit()

    def redo(self):
        """
        重做或首次执行操作：在场景中创建并添加所有热区项。
        """
        # 如果 self.added_items 不为空，说明是重做操作，
        # 之前撤销时只是移除了item但没有销毁它们（如果设计如此）。
        # 但我们目前的 undo() 设计是 clear()，所以这里总是重新创建。
        if self.added_items:
            for item in self.added_items:
                self.scene.addItem(item)
            if self.scene:
                self.scene.selectionChanged.emit()
            return

        # 如果是首次执行或撤销后重做
        bounds = self.scene.sceneRect()
        session = self.main_window.get_session_by_viewer(self.viewer)
        if not session:
            return

        for hotspot_info in self.hotspots_data:
            # 确定要创建的形状类型
            shape_class = ResizableEllipseItem if hotspot_info['type'] == 'ellipse' else ResizableRectItem

            # 从数据中提取位置和尺寸信息
            rect_data = hotspot_info['rect']
            pos_data = hotspot_info['pos']
            item_data = hotspot_info['data']

            # 创建热区项实例
            item = shape_class(0, 0, rect_data['w'], rect_data['h'], bounds=bounds, viewer=self.viewer)
            item.setPos(QPointF(pos_data['x'], pos_data['y']))

            # 生成并分配新的唯一ID
            new_id = self.main_window.generate_new_hotspot_id(session)
            item_data['id'] = new_id
            item.setData(0, item_data)

            # 设置外观
            item.setPen(self.main_window.get_hotspot_pen())
            item.setBrush(self.main_window.get_hotspot_brush())

            # 添加到场景和内部列表
            self.scene.addItem(item)
            self.added_items.append(item)

        if self.scene:
            self.scene.selectionChanged.emit()