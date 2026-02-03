# _mixin_get_hotspot_style_context.py
from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor


class GetHotspotStyleContextMixin:
    @classmethod
    def _get_hotspot_style_context(cls) -> dict:
        """
        读取用户设置并返回一个字典，该字典将作为 'hotspot_style' 变量传递给 Jinja2 模板。
        """
        settings = QSettings("MyCompany", "HotspotEditor")

        # --- 1. 热区样式设置 ---
        fill_color = settings.value("export/fill_color", QColor(64, 158, 255))
        opacity = settings.value("export/opacity_percent", 30, type=int) / 100.0
        icon_size = settings.value("export/control_icon_size", 24, type=int)

        # --- *** 核心修改: 2. 读取提纲/目录设置 *** ---
        outline_pos = settings.value("outline/position", "bottom-left")
        outline_behavior = settings.value("outline/behavior", "auto_hide")
        outline_font_size = settings.value("outline/font_size", 16, type=int)
        outline_indent = settings.value("outline/indent", 1.0, type=float)
        # --- *** 修改结束 *** ---

        return {
            # 热区相关
            "fill_color_rgba": f"rgba({fill_color.red()}, {fill_color.green()}, {fill_color.blue()}, {opacity})",
            "hover_fill_color_rgba": f"rgba({fill_color.red()}, {fill_color.green()}, {fill_color.blue()}, {opacity + 0.2})",
            "has_border": settings.value("export/has_border", True, type=bool),
            "border_color_hex": settings.value("export/border_color", QColor(64, 158, 255)).name(),
            "border_width_px": settings.value("export/border_width", 1, type=int),
            "control_icon_size_px": icon_size,

            # 提纲相关 (新增加的字典)
            "outline": {
                "position": outline_pos,  # 'bottom-left', 'top-left', etc.
                "behavior": outline_behavior,  # 'auto_hide' or 'fixed'
                "font_size_px": outline_font_size,
                "indent_em": outline_indent
            }
        }