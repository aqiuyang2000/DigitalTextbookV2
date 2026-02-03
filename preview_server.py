# FILE: preview_server.py (已支持多文件预览)

import sys
import subprocess
import webbrowser
import time
from PySide6.QtWidgets import QMessageBox


class PreviewServer:
    """管理本地HTTP服务器的生命周期，支持同时预览多个页面。"""

    def __init__(self):
        self.server_process = None
        self.export_path = None
        self.port = 8000

    def set_path(self, path):
        """设置服务器的工作目录。"""
        self.export_path = path

    def stop(self):
        """如果服务器正在运行，则终止它。"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None

    def start(self, files_to_open=None):
        """
        启动HTTP服务器并在浏览器中打开指定的文件列表。
        :param files_to_open: 要打开的文件名列表，例如 ["index.html", "index_scroll.html"]
        """
        if files_to_open is None:
            files_to_open = ["index.html"]

        if not self.export_path:
            QMessageBox.warning(None, "错误", "预览路径未设置。")
            return None

        # 1. 先停止可能存在的旧服务器
        self.stop()

        # 2. 尝试启动新服务器
        base_url = ""
        for i in range(10):
            current_port = self.port + i
            try:
                si = None
                if sys.platform == "win32":
                    si = subprocess.STARTUPINFO()
                    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                # 启动 http.server 子进程
                self.server_process = subprocess.Popen(
                    [sys.executable, "-m", "http.server", str(current_port)],
                    cwd=self.export_path,
                    startupinfo=si
                )

                base_url = f"http://localhost:{current_port}/"
                break
            except Exception:
                continue
        else:
            QMessageBox.critical(None, "启动服务器失败", "无法在8000-8009端口找到可用的端口。")
            return None

        # 3. 服务器启动成功后，依次打开所有请求的文件
        # 稍微等待一下确保服务器就绪（通常不需要，但为了保险）
        time.sleep(0.5)

        for file_name in files_to_open:
            full_url = base_url + file_name
            webbrowser.open(full_url)

        return base_url