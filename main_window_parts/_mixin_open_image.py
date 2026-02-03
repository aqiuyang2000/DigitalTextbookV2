# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_open_image.py
#
# 功能: 提供 open_image 方法，用于向当前项目添加新的页面（图片或PDF）。

import os
import shutil

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtCore import QSettings


class OpenImageMixin:
    """
    一个 Mixin 类，包含向当前项目添加新页面的 open_image 方法。
    """

    def open_image(self):
        """
        处理“添加页面到项目...”的完整流程。
        """
        # 1. 前置检查：必须有已保存的项目
        if not self.project_path:
            QMessageBox.warning(self, "无打开的项目", "请先新建或打开一个项目，再添加图片。")
            return

        # --- *** 关键修复：恢复被错误省略的代码 *** ---
        # 2. 弹出文件选择对话框，并在这里定义 file_paths
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "添加图片或PDF到项目",
            "",
            "所有支持的文件 (*.png *.jpg *.jpeg *.bmp *.pdf);;PDF 文件 (*.pdf)"
        )
        if not file_paths:
            return
        # --- *** 修复结束 *** ---

        # 3. 确定新页面的插入位置
        base_insertion_index = -1
        if self.sessions:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("选择插入位置")
            msg_box.setText(f"您想将新页面插入到当前页面 (第 {self.active_session_index + 1} 页) 的前面还是后面？")
            before_btn = msg_box.addButton("在前面插入", QMessageBox.ActionRole)
            after_btn = msg_box.addButton("在后面插入", QMessageBox.ActionRole)
            cancel_btn = msg_box.addButton("取消", QMessageBox.RejectRole)
            msg_box.setDefaultButton(after_btn)
            msg_box.exec()

            if msg_box.clickedButton() == cancel_btn:
                return
            elif msg_box.clickedButton() == before_btn:
                base_insertion_index = self.active_session_index
            else:  # after_btn
                base_insertion_index = self.active_session_index + 1

        target_session_index_after_add = base_insertion_index if base_insertion_index != -1 else 0

        initial_count = len(self.sessions)
        added_count = 0

        # 4. 遍历并处理所有选中的文件
        try:
            for path in file_paths:
                current_insertion_index = base_insertion_index + added_count if base_insertion_index != -1 else -1

                if os.path.splitext(path)[1].lower() == '.pdf':
                    # --- 处理 PDF 文件 ---
                    workspace_path = self._get_workspace_path()
                    sources_dir = os.path.join(workspace_path, "sources")
                    os.makedirs(sources_dir, exist_ok=True)

                    source_filename = os.path.basename(path)
                    source_copy_path = os.path.join(sources_dir, source_filename)
                    if not os.path.exists(source_copy_path):
                        shutil.copy2(path, source_copy_path)

                    asset_dir = self._get_project_asset_dir_path(source_copy_path)

                    settings = QSettings("MyCompany", "HotspotEditor")
                    dpi = settings.value("pdf/resolution_dpi", 150, type=int)

                    processed_result = self.pdf_processor.process(source_copy_path, asset_dir, resolution_dpi=dpi)

                    if processed_result:
                        png_paths, single_pdf_paths = processed_result

                        for page_index, (img_path, pdf_path) in enumerate(zip(png_paths, single_pdf_paths)):
                            current_insertion_index_for_page = base_insertion_index + added_count if base_insertion_index != -1 else -1
                            self._load_image_path(
                                img_path,
                                insertion_index=current_insertion_index_for_page,
                                source_pdf_path=pdf_path,
                                original_multipage_pdf_path=source_copy_path,
                                source_page_index=page_index
                            )
                            added_count += 1

                else:
                    # --- 处理单个图片文件 ---
                    self._load_image_path(
                        path,
                        insertion_index=current_insertion_index,
                        source_page_index=0
                    )
                    added_count += 1

        finally:
            self.statusBar().showMessage("文件添加完成！", 2000)

        # 5. 如果成功添加了任何页面，则更新UI
        if len(self.sessions) > initial_count:
            self.update_viewers_layout()
            self.set_active_session(target_session_index_after_add)
            self.set_dirty(True)