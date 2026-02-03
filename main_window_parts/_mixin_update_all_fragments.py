# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_update_all_fragments.py
#
# 功能: 提供 update_all_fragments 方法，用于一键更新当前活动页面的所有格式片段。

import traceback

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox

# --- Project-specific Imports ---
from exporter import HtmlExporter
from exporter_flip import export_double_page_fragment

class UpdateAllFragmentsMixin:
    """
    一个 Mixin 类，包含一键更新当前页面所有格式片段的功能。
    """
    def update_all_fragments(self):
        """
        “一键更新所有格式片段”按钮的槽函数。

        此功能主要用于开发和调试，允许用户在修改了单个页面后，
        无需重新导出整个项目，只需快速更新该页面对应的 HTML 文件，
        即可在浏览器中刷新查看更改。

        它会依次调用三种不同格式的“片段导出”函数。
        """
        # 1. 前置检查
        if not self.project_path:
            QMessageBox.warning(self, "无项目", "请先保存或打开一个项目。")
            return
        if not self.active_session:
            QMessageBox.warning(self, "无活动页面", "没有选择任何页面可供更新。")
            return

        # 获取统一的输出目录
        output_dir = self._get_common_output_dir()
        if not output_dir:
            return

        try:
            # 2. 依次调用三种片段更新函数
            # a. 更新双页画册片段
            export_double_page_fragment(self, output_dir)
            
            # b. 更新单页画册片段
            HtmlExporter.export_single_flipbook_page(self, output_dir)
            
            # c. 更新长网页片段
            HtmlExporter.export_to_html(self, output_dir)
            
            # 3. 显示成功信息
            self.statusBar().showMessage("所有格式的页面片段已成功更新！", 5000)
            
        except Exception as e:
            # 4. 捕获任何异常
            QMessageBox.critical(self, "片段更新失败", f"更新过程中发生错误: {e}\n{traceback.format_exc()}")