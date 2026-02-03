# D:\projects-singlepage\hotspot_editor\main_window_parts\_mixin_get_hotspot_pen.py
#
# 功能: 提供 get_hotspot_pen 辅助方法，用于根据设置创建热区边框的 QPen。

# --- Qt Imports ---
from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import QSettings

class GetHotspotPenMixin:
    """
    一个 Mixin 类，包含一个辅助方法，用于根据用户设置创建热区边框的 QPen。
    """
    def get_hotspot_pen(self) -> QPen:
        """
        从 QSettings 中读取编辑器热区的边框颜色设置，并返回一个配置好的 QPen 对象。

        这个方法封装了从设置中读取值的逻辑，并提供了默认值以防设置不存在。
        它被用于在创建新热区或在应用新设置后刷新现有热区时，获取正确的边框样式。

        Returns:
            QPen: 根据用户设置（或默认值）创建的画笔对象。
        """
        # 1. 创建 QSettings 实例
        settings = QSettings("MyCompany", "HotspotEditor")
        
        # 2. 从设置中读取 "editor/border_color" 的值。
        #    如果该设置不存在，则使用 QColor(Qt.blue) 作为默认颜色。
        color = settings.value("editor/border_color", QColor("blue"))
        
        # 3. 创建并返回一个 QPen 对象，颜色为读取到的颜色，宽度固定为 2
        return QPen(color, 2)