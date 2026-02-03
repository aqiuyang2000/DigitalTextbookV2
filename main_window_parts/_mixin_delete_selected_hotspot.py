# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_delete_selected_hotspot.py
#
# 功能: 提供 delete_selected_hotspot 方法，用于删除选中的热区。

# --- Project-specific Imports ---
from commands import DeleteCommand
from graphics_items import AbstractResizableItem

class DeleteSelectedHotspotMixin:
    """
    一个 Mixin 类，包含用于删除选中热区的 delete_selected_hotspot 方法。
    """
    def delete_selected_hotspot(self):
        """
        删除当前活动会话中所有被选中的热区项。

        此方法会收集所有选中的热区项，创建一个 `DeleteCommand` 命令，
        然后将该命令推送到当前页面的撤销栈中。

        这个方法是“删除”菜单项、`Delete` 快捷键以及 `PhotoViewer` 
        上下文菜单发出的 `deleteRequested` 信号的最终槽函数。
        """
        if not self.active_session:
            return

        # 1. 收集所有需要被删除的项
        #    使用列表推导式筛选出所有选中的、且是我们自定义的热区项
        items_to_delete = [
            item for item in self.active_session.scene.selectedItems() 
            if isinstance(item, AbstractResizableItem)
        ]

        # 如果没有选中任何热区项，则不执行任何操作
        if not items_to_delete:
            return
            
        # 2. 创建一个 DeleteCommand
        command = DeleteCommand(self.active_session.scene, items_to_delete)
        
        # 3. 将命令推送到当前页面的撤销栈
        #    命令的 redo() 方法会立即被执行，从场景中移除这些项。
        self.active_session.undo_stack.push(command)