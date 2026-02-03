# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_process_and_load_source_for_page.py
#
# 功能: 提供 _process_and_load_source_for_page 方法，用于在缓存丢失时重新生成并加载页面。

import os

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox
# --- *** 核心修改 1/2: 导入 QSettings *** ---
from PySide6.QtCore import QSettings


class ProcessAndLoadSourceForPageMixin:
    """
    一个 Mixin 类，包含在项目加载期间按需重新处理PDF源文件以恢复
    单个缺失页面的功能。
    """

    def _process_and_load_source_for_page(self, page_data: dict):
        """
        为一个在加载时发现缓存丢失的页面，重新处理其原始PDF源文件并加载它。

        这是一个恢复机制，确保即使项目的 `_out/workspace/assets` 目录
        不完整，项目仍然可以成功加载。

        Args:
            page_data (dict): 从项目文件中读取的、关于这单个页面的数据字典。
                              它必须包含源PDF的路径和页面在源中的索引。
        """
        # 1. 确定原始多页PDF的绝对路径
        source_pdf_abs = page_data.get('workspace_source_abs') or page_data.get('source_pdf_path_abs')
        if not source_pdf_abs or not os.path.exists(source_pdf_abs):
            QMessageBox.warning(
                self,
                "缺少文件",
                f"找不到用于重新生成页面的源PDF文件，已跳过：\n{source_pdf_abs or '无路径'}"
            )
            return

        # 2. 获取该PDF对应的资产目录 (将在其中存放新生成的图片和单页PDF)
        asset_dir = self._get_project_asset_dir_path(source_pdf_abs)
        if not asset_dir:
            QMessageBox.warning(self, "错误", "无法为源文件创建资产目录，已跳过。")
            return

        # --- *** 核心修改 2/2: 读取设置并传递给 process 方法 *** ---
        # 1. 从 QSettings 读取用户保存的分辨率，默认为 150
        settings = QSettings("MyCompany", "HotspotEditor")
        dpi = settings.value("pdf/resolution_dpi", 150, type=int)

        # 2. 调用 PdfProcessor 来处理整个PDF文件，并传入 dpi 参数
        processed_result = self.pdf_processor.process(source_pdf_abs, asset_dir, resolution_dpi=dpi)

        if not processed_result:
            QMessageBox.warning(self, "处理失败", f"无法处理源PDF文件:\n{source_pdf_abs}")
            return

        png_paths, single_pdf_paths = processed_result

        # 4. 从处理结果中，只挑选出我们当前需要的那个页面
        page_index = page_data.get('page_index_in_source', 0)

        if page_index < len(png_paths):
            # 5. 调用 _load_image_path 来加载新生成的页面资源
            self._load_image_path(
                png_paths[page_index],
                hotspots_data=page_data.get('hotspots', []),
                next_hotspot_id_start=page_data.get('next_hotspot_id', 0),
                source_pdf_path=single_pdf_paths[page_index],
                original_multipage_pdf_path=source_pdf_abs,
                source_page_index=page_index
            )
        else:
            QMessageBox.warning(
                self,
                "索引错误",
                f"尝试加载源PDF的第 {page_index + 1} 页时失败，因为处理后只得到 {len(png_paths)} 页。"
            )