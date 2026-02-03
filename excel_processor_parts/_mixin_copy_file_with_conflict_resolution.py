# FILE: _mixin_copy_file_with_conflict_resolution.py
#
# 功能: 为 ExcelProcessor 添加文件冲突解决方法

import os
import shutil


class ExcelProcessorCopyFileMixin:
    """
    为 ExcelProcessor 添加文件复制和冲突解决功能。
    """

    @staticmethod
    def _copy_file_with_conflict_resolution(source_path: str, destination_dir: str) -> str:
        """
        复制文件到目标目录，如果文件名冲突，则自动重命名。
        返回最终复制后文件的绝对路径，如果源文件不存在则返回 None。

        Args:
            source_path (str): 源文件路径
            destination_dir (str): 目标目录

        Returns:
            str: 复制后的文件路径，如果失败则返回 None
        """
        if not source_path or not os.path.exists(source_path):
            return None

        filename = os.path.basename(source_path)
        basename, extension = os.path.splitext(filename)

        destination_path = os.path.join(destination_dir, filename)

        counter = 1
        while os.path.exists(destination_path):
            new_filename = f"{basename}_{counter}{extension}"
            destination_path = os.path.join(destination_dir, new_filename)
            counter += 1

        try:
            shutil.copy2(source_path, destination_path)
            return destination_path
        except Exception as e:
            print(f"错误：复制文件时失败 '{source_path}' -> '{destination_path}'. 原因: {e}")
            return None