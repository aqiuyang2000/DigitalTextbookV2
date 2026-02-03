# D:\projects\singlepage\hotspot_editor\tools\base_tool.py (新版本 - 支持选项)
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget


class AbstractPdfTool(QObject):
    """
    所有PDF工具的抽象基类。
    子类必须定义 name 和 description 属性。
    """
    name = "未命名工具"
    description = "无详细描述。"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.options = {}

    def run(self, main_window):
        """工具的主要执行逻辑，必须由子类实现。"""
        raise NotImplementedError("run() method must be implemented by subclasses.")

    # --- *** 核心修改: 允许 get_options_widget 接收 main_window 参数 *** ---
    def get_options_widget(self, main_window) -> QWidget | None:
        """
        可选方法。如果工具需要自定义选项UI，则重写此方法。
        返回一个 QWidget 实例，该实例将被显示在工具箱对话框中。

        Args:
            main_window: 主窗口的引用，以便工具可以访问全局设置等上下文。

        Returns:
            QWidget or None: 选项控件，或在没有选项时返回 None。
        """
        return None

    def set_options(self, options: dict):
        """
        可选方法。工具箱在执行 run() 之前会调用此方法。
        """
        self.options = options