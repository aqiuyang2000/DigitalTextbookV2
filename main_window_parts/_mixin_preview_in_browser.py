# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_preview_in_browser.py
#
# 功能: 提供 preview_in_browser 方法，用于启动本地服务器并在浏览器中预览导出的网页。

import os

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox

class PreviewInBrowserMixin:
    """
    一个 Mixin 类，包含用于在浏览器中预览项目的功能。
    """
    def preview_in_browser(self):
        """
        “在浏览器中预览...”按钮的槽函数。

        流程：
        1. 获取项目的输出目录。
        2. 根据 `chk_preview_dual`, `chk_preview_single`, `chk_preview_scroll` 
           复选框的勾选状态，构建一个需要预览的文件列表。
        3. 检查这些文件是否存在。如果用户勾选了某个格式但其文件不存在，
           则向用户显示警告。
        4. 如果有至少一个有效的文件可供预览，则调用 `self.preview_server` 
           来启动或重启一个本地HTTP服务器。
        5. `preview_server` 会负责在用户的默认浏览器中打开这些文件的URL。
        """
        output_dir = self._get_output_directory()
        if not output_dir:
            # 这个检查是双重保险，因为按钮通常在这种情况下是禁用的
            return

        files_to_open = []
        missing_formats = []

        # 检查双页画册 (index.html)
        if self.chk_preview_dual.isChecked():
            if os.path.exists(os.path.join(output_dir, "index.html")):
                files_to_open.append("index.html")
            else:
                missing_formats.append("双页画册")

        # 检查单页画册 (index_single.html)
        if self.chk_preview_single.isChecked():
            if os.path.exists(os.path.join(output_dir, "index_single.html")):
                files_to_open.append("index_single.html")
            else:
                missing_formats.append("单页画册")

        # 检查滚动网页 (index_scroll.html)
        if self.chk_preview_scroll.isChecked():
            if os.path.exists(os.path.join(output_dir, "index_scroll.html")):
                files_to_open.append("index_scroll.html")
            else:
                missing_formats.append("滚动网页")

        # 如果用户勾选了某个格式但其文件不存在，给予提示
        if missing_formats:
            QMessageBox.warning(self, "文件未找到", 
                                f"以下勾选的格式尚未导出，无法预览：\n{', '.join(missing_formats)}\n\n请先执行导出操作。")

        # 如果有可打开的文件，启动服务器并预览
        if files_to_open:
            self.preview_server.set_path(output_dir)
            base_url = self.preview_server.start(files_to_open)
            if base_url:
                self.statusBar().showMessage(f"预览服务器正在运行，已打开 {len(files_to_open)} 个标签页...", 5000)
        elif not missing_formats:
            # 如果既没有要打开的文件，也没有缺失的文件（说明用户一个都没勾选）
             QMessageBox.information(self, "提示", "请至少勾选一种需要预览的格式。")