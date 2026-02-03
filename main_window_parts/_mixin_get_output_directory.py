# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_get_output_directory.py
#
# 功能: 提供 _get_output_directory 辅助方法，用于获取项目的输出目录路径。

import os

class GetOutputDirectoryMixin:
    """
    一个 Mixin 类，包含用于获取项目主输出目录路径的辅助方法。
    """
    def _get_output_directory(self) -> str | None:
        """
        获取当前项目的根输出目录（`_out` 文件夹）的绝对路径。

        输出目录的命名规则是：与 `.json` 项目文件同名，但去掉 `.json`
        扩展名，并追加 `_out` 后缀。它与 `.json` 文件位于同一目录下。

        例如:
        - 项目文件: `D:/MyProjects/AwesomeProject.json`
        - 输出目录: `D:/MyProjects/AwesomeProject_out`

        Returns:
            str | None: 如果项目路径已设置，则返回输出目录的绝对路径；
                        否则返回 None。
        """

        # 1. 检查项目是否已保存
        if not self.project_path:
            return None
        
        # 2. 获取项目文件所在的目录
        project_dir = os.path.dirname(self.project_path)
        
        # 3. 获取项目文件的基本名称（不含扩展名）
        project_basename = os.path.splitext(os.path.basename(self.project_path))[0]
        
        # 4. 构建输出目录名并返回完整路径
        output_dir_name = f"{project_basename}_out"
        return os.path.join(project_dir, output_dir_name)