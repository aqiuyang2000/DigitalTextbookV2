# D:\projects\singlepage\hotspot_editor\exporter_parts\_mixin_export_to_html.py
import os
import shutil
from PySide6.QtWidgets import QMessageBox
from template_manager import template_manager


class ExportToHtmlMixin:
    @classmethod
    def export_to_html(cls, parent_window, output_dir: str):
        if not parent_window.active_session:
            QMessageBox.warning(parent_window, "错误", "没有选择任何页面可供导出。");
            return

        session = parent_window.active_session
        page_num = parent_window.active_session_index + 1

        # --- 核心修改 1/3: 目录路径与主导出逻辑保持一致 ---
        pages_dir_name, images_dir_name = "pages_scroll", "images_scroll"
        pages_dir = os.path.join(output_dir, pages_dir_name)
        images_dir = os.path.join(output_dir, images_dir_name)
        os.makedirs(pages_dir, exist_ok=True)
        os.makedirs(images_dir, exist_ok=True)

        save_path = os.path.join(pages_dir, f"page_{page_num}.html")
        media_dir = os.path.join(output_dir, "media")

        _, ext = os.path.splitext(session.image_path)
        unique_image_filename = f"page-img-{page_num}{ext}"
        shutil.copy(session.image_path, os.path.join(images_dir, unique_image_filename))

        hotspots, js_popups = cls._collect_hotspots_for_session(session, media_dir, path_prefix="../")

        # --- 核心修改 2/3: 图片路径与主导出逻辑保持一致 ---
        image_path_for_html = f"{images_dir_name}/{unique_image_filename}"

        # (注意：片段导出不需要 js_popups，因为主 index 文件会统一加载)
        context = {
            "page_num": page_num,
            "image_filename": image_path_for_html,
            "hotspots": hotspots
        }

        # --- 核心修改 3/3: 更新 fragment 模板的渲染路径 ---
        fragment_content = template_manager.render('dynamic_page/scroll_view/fragment.html.j2', **context)

        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(fragment_content)
            parent_window.statusBar().showMessage(f"长网页片段已成功更新。", 4000)
        except Exception as e:
            QMessageBox.critical(parent_window, "导出失败", f"写入HTML文件时发生错误: {e}")