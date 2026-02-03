# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_perform_project_load.py
#
# 功能: 提供 _perform_project_load 方法，执行实际的项目加载工作。

import os
import traceback
import uuid

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QSettings

class PerformProjectLoadMixin:
    """
    一个 Mixin 类，包含执行项目加载的核心方法 _perform_project_load。
    """
    def _perform_project_load(self, path: str):
        """
        执行从指定路径加载项目的核心逻辑。

        此方法被 open_project 和 _load_last_project 调用。它不处理用户交互，
        只负责文件读取、数据解析和状态重建。

        流程包括：
        1. 清理当前工作区。
        2. 调用 project_manager 加载并预处理项目数据。
        3. 设置 project_id 和提纲。
        4. 遍历项目数据中的每个页面定义。
        5. 检查页面的缓存资源是否存在，如果存在则直接加载。
        6. 如果缓存不存在，则调用 _process_and_load_source_for_page 重新生成。
        7. 加载完成后，更新UI布局和状态，并将路径存入 QSettings。

        Args:
            path (str): 要加载的 `.json` 项目文件的绝对路径。
        """
        try:
            # 1. 设置项目路径并清空当前工作区
            self.project_path = path
            self.clear_project(keep_path=True)

            # 2. 调用 ProjectManager 加载数据
            project_data = self.project_manager.load_project(path)
            if not project_data:
                raise ValueError("项目文件为空或格式不正确。")

            # 3. 设置项目级属性
            self.project_id = project_data.get('project_id') or f"PROJ_{uuid.uuid4().hex[:8]}"
            self.outline_data = project_data.get('outline', [])
            self.outline_widget.populate_tree(self.outline_data)

            all_pages_data = project_data.get('pages', [])

            # 4. 遍历并加载每个页面
            for page_data in all_pages_data:
                # 获取工作区内资源的绝对路径 (由 project_manager.load_project 生成)
                workspace_assets_abs = page_data.get('workspace_assets_abs')
                page_index = page_data.get('page_index_in_source', 0)

                # 构建期望的图片和单页PDF的缓存路径
                expected_png_path = os.path.join(workspace_assets_abs, "images", f"page-{page_index + 1}.png")
                expected_spdf_path = os.path.join(workspace_assets_abs, "single_pdfs", f"page-{page_index + 1}.pdf")

                # 获取原始PDF的路径 (可能是工作区内的副本，也可能是旧版的绝对路径)
                original_pdf_path = page_data.get('workspace_source_abs') or page_data.get('source_pdf_path_abs')

                # 5. 检查缓存是否存在
                if os.path.exists(expected_png_path):
                    print(f"  [LOAD] 发现缓存素材，直接加载 page #{page_index + 1}")
                    # 直接加载缓存的PNG图片
                    self._load_image_path(
                        expected_png_path,
                        hotspots_data=page_data.get('hotspots', []),
                        next_hotspot_id_start=page_data.get('next_hotspot_id', 0),
                        source_pdf_path=expected_spdf_path,
                        original_multipage_pdf_path=original_pdf_path,
                        source_page_index=page_index
                    )
                else:
                    # 6. 如果缓存不存在，则需要重新从源PDF生成
                    print(f"  [LOAD] 未找到 page #{page_index + 1} 的缓存，将重新处理源: {original_pdf_path}")
                    self._process_and_load_source_for_page(page_data)

            # 7. 加载完成后的清理和UI更新
            self.statusBar().showMessage("项目加载完成！", 2000)
            self._ensure_output_directory()
            self.update_viewers_layout()
            
            if self.sessions:
                self.set_active_session(0)
            else:
                self.update_ui_for_active_session()
            
            # 将成功加载的路径保存到 QSettings
            settings = QSettings("MyCompany", "HotspotEditor")
            settings.setValue("last_project_path", path)
            self.set_dirty(False)

        except Exception as e:
            # 捕获任何加载过程中的错误
            QMessageBox.critical(self, "打开失败", f"无法加载项目文件：{e}\n{traceback.format_exc()}")
            self.clear_project() # 加载失败时，清空所有内容回到初始状态