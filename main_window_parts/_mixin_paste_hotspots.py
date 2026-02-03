# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_paste_hotspots.py
#
# 功能: 提供 paste_hotspots 方法，用于将剪贴板中的热区粘贴到场景中。

# --- Qt Imports ---
from PySide6.QtCore import QPointF

# --- Project-specific Imports ---
from commands import PasteCommand

class PasteHotspotsMixin:
    """
    一个 Mixin 类，包含用于粘贴热区的 paste_hotspots 方法。
    """
    def paste_hotspots(self, position: QPointF):
        """
        在指定位置粘贴内部剪贴板 (`self.clipboard`) 中的热区。

        此方法会检查剪贴板中是否有内容以及是否存在活动会话。如果满足条件，
        它会创建一个 `PasteCommand` 命令，并将剪贴板数据、目标位置等信息
        传递给该命令。

        将粘贴操作封装为命令，使得粘贴也可以被撤销。

        Args:
            position (QPointF): 鼠标光标在场景坐标系中的位置，
                                将作为粘贴的基准点。
        """
        # 1. 检查剪贴板是否为空或没有活动会话
        if not self.clipboard or not self.active_session:
            return
            
        # 2. 创建一个 PasteCommand
        command = PasteCommand(
            self.active_session.scene, 
            self.active_session.viewer, 
            self, 
            self.clipboard, 
            position
        )
        
        # 3. 将命令推送到当前页面的撤销栈
        #    命令的 redo() 方法会立即被执行，完成粘贴操作。
        self.active_session.undo_stack.push(command)