# FILE: commands.py (New Assembler File)
#
# 功能: 这是 commands 模块的公共接口。
#       它从 'commands_parts' 目录中导入所有独立的命令类，
#       并将它们作为模块的公共 API 暴露出来。
#       这种方式确保了对项目其他部分的调用完全透明且不受影响。

from commands_parts._command_batch_add_hotspots import BatchAddHotspotsCommand
from commands_parts._command_geometry_change import GeometryChangeCommand
from commands_parts._command_data_change import DataChangeCommand
from commands_parts._command_paste import PasteCommand
from commands_parts._command_delete import DeleteCommand
from commands_parts._command_batch_items_geometry import BatchItemsGeometryCommand
from commands_parts._command_batch_scale import BatchScaleCommand
from commands_parts._command_delete_page import DeletePageCommand