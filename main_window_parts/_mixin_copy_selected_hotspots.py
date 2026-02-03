# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_copy_selected_hotspots.py
#
# 功能: 提供 copy_selected_hotspots 方法，用于复制选中的热区到内部剪贴板。

# --- Project-specific Imports ---
from graphics_items import AbstractResizableItem, ResizableRectItem

class CopySelectedHotspotsMixin:
    """
    一个 Mixin 类，包含用于复制选中热区数据的 copy_selected_hotspots 方法。
    """
    def copy_selected_hotspots(self):
        """
        将当前活动会话中所有选中的热区项的关键数据复制到内部剪贴板。

        此方法会遍历场景中的所有选中项，将它们的形状类型、矩形尺寸
        和自定义数据 (`item.data(0)`) 提取出来，打包成一个字典列表，
        并存储在 `self.clipboard` 中以备粘贴使用。
        """
        if not self.active_session:
            return

        # 1. 在每次复制前清空剪贴板
        self.clipboard.clear()
        
        # 2. 遍历当前场景中的所有选中项
        for item in self.active_session.scene.selectedItems():
            # 确保我们只处理自定义的热区项
            if isinstance(item, AbstractResizableItem):
                # 3. 序列化热区数据
                self.clipboard.append({
                    'type': 'rectangle' if isinstance(item, ResizableRectItem) else 'ellipse',
                    'rect': item.rect(),
                    'data': item.data(0)
                })