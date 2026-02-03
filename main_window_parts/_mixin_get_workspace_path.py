# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_get_workspace_path.py
#
# 功能: 提供 _get_workspace_path 辅助方法，用于获取项目的工作区路径。

import os

class GetWorkspacePathMixin:
    """
    一个 Mixin 类，包含用于获取项目工作区目录路径的辅助方法。
    """
    def _get_workspace_path(self) -> str | None:
        """
        获取当前项目的工作区 (`workspace`) 目录的绝对路径。

        工作区目录位于项目输出目录 (`_out`) 下，用于存放项目的
        中间产物和源文件副本，如处理后的图片、PDF，以及源PDF的备份。

        Returns:
            str | None: 如果项目路径已设置，则返回工作区目录的绝对路径；
                        否则返回 None。
        """
        if not self.project_path:
            return None
        
        # 调用另一个辅助方法来获取项目输出目录的根路径
        output_dir = self._get_output_directory()
        if not output_dir:
            return None
            
        # 在输出目录下拼接 "workspace"
        return os.path.join(output_dir, "workspace")