# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_get_common_output_dir.py
#
# 功能: 提供 _get_common_output_dir 辅助方法，用于安全地获取项目输出目录。

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox

class GetCommonOutputDirectoryMixin:
    """
    一个 Mixin 类，包含用于获取通用输出目录并处理错误的辅助方法。
    """
    def _get_common_output_dir(self) -> str | None:
        """
        一个安全地获取项目输出目录的辅助方法，主要被“片段更新”功能使用。

        它会检查项目是否已保存。
        - 如果未保存，它会弹出一个警告消息框，并返回 `None`。
        - 如果已保存，它会调用 `_get_output_directory` 来获取并返回路径。

        这与 `_get_output_directory` 的区别在于，此方法包含了用户交互
        （弹窗警告），而 `_get_output_directory` 纯粹是进行路径计算。

        Returns:
            str | None: 如果项目已保存，则返回输出目录的绝对路径；
                        否则返回 None。
        """
        # 1. 检查项目路径是否存在
        if not self.project_path:
            # 如果不存在，则向用户显示一个警告对话框
            QMessageBox.warning(self, "无项目", "请先打开或保存一个项目。")
            return None
        
        # 2. 如果路径存在，则调用基础的路径获取方法
        return self._get_output_directory()