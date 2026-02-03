# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_get_project_asset_dir_path.py
#
# 功能: 提供 _get_project_asset_dir_path 辅助方法，用于获取特定源文件的资产目录路径。

import os
import hashlib

class GetProjectAssetDirPathMixin:
    """
    一个 Mixin 类，包含用于获取特定源文件资产目录路径的辅助方法。
    """
    def _get_project_asset_dir_path(self, source_pdf_path: str) -> str | None:
        """
        根据给定的源PDF文件路径，为其生成一个唯一的资产目录路径。

        这个资产目录位于工作区的 `assets` 文件夹下。目录名是根据
        源PDF的文件名计算出的 MD5 哈希值，这确保了：
        1. 目录名是唯一的，不会与其他PDF的资产冲突。
        2. 目录名是确定的，每次为同一个PDF生成时，都会得到相同的路径。

        Args:
            source_pdf_path (str): 源PDF文件的绝对路径。

        Returns:
            str | None: 如果成功，返回该PDF对应的资产目录的绝对路径；
                        否则返回 None。
        """
        # 1. 获取工作区的根路径
        workspace_path = self._get_workspace_path()
        if not workspace_path:
            return None

        # 2. 从源路径中提取文件名
        filename = os.path.basename(source_pdf_path)
        
        # 3. 计算文件名的 MD5 哈希值作为目录名
        dir_name = hashlib.md5(filename.encode()).hexdigest()
        
        # 4. 构建最终的资产目录路径
        #    路径结构: .../_out/workspace/assets/<md5_hash>/
        return os.path.join(workspace_path, "assets", dir_name)