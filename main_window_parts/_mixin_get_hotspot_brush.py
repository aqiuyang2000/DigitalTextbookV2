# D:\projects-singlepage\hotspot_editor\main_window_parts\_mixin_get_hotspot_brush.py
#
# 功能: 提供 get_hotspot_brush 辅助方法，用于根据设置创建热区填充的 QBrush。

# --- Qt Imports ---
from PySide6.QtGui import QBrush, QColor
from PySide6.QtCore import QSettings, Qt

class GetHotspotBrushMixin:
    """
    一个 Mixin 类，包含一个辅助方法，用于根据用户设置创建热区填充的 QBrush。
    """
    def get_hotspot_brush(self) -> QBrush:
        """
        从 QSettings 中读取编辑器热区的填充颜色和不透明度设置，
        并返回一个配置好的 QBrush 对象。

        这个方法封装了读取和组合颜色与透明度的逻辑，并为每个设置
        提供了默认值。

        Returns:
            QBrush: 根据用户设置（或默认值）创建的画刷对象。
        """
        # 1. 创建 QSettings 实例
        settings = QSettings("MyCompany", "HotspotEditor")
        
        # 2. 读取填充颜色，默认值为蓝色
        color = settings.value("editor/fill_color", QColor(Qt.blue))
        
        # 3. 读取不透明度百分比 (0-100)，默认值为 15%
        #    type=int 确保了返回的是整数类型
        opacity_percent = settings.value("editor/opacity_percent", 15, type=int)
        
        # 4. 将百分比转换为浮点数 (0.0-1.0) 并设置到颜色对象的 alpha 通道
        color.setAlphaF(opacity_percent / 100.0)
        
        # 5. 创建并返回一个 QBrush 对象
        return QBrush(color)