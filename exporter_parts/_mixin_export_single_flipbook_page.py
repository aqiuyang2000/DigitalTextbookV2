# _mixin_export_single_flipbook_page.py
import os
import shutil
from PySide6.QtWidgets import QMessageBox
from template_manager import template_manager

class ExportSingleFlipbookPageMixin:
    @classmethod
    def export_single_flipbook_page(cls, parent_window, output_dir: str):
        if not parent_window.active_session:
            QMessageBox.warning(parent_window, "错误", "没有选择任何页面可供导出。");
            return

        session = parent_window.active_session;
        page_num = parent_window.active_session_index + 1
        pages_dir_name, images_dir_name = "pages_single", "images_single"
        pages_dir, images_dir = os.path.join(output_dir, pages_dir_name), os.path.join(output_dir, images_dir_name)
        os.makedirs(pages_dir, exist_ok=True);
        os.makedirs(images_dir, exist_ok=True)
        save_path = os.path.join(pages_dir, f"page_{page_num}.html");
        media_dir = os.path.join(output_dir, "media")

        _, ext = os.path.splitext(session.image_path)
        unique_image_filename = f"page-img-{page_num}{ext}"
        shutil.copy(session.image_path, os.path.join(images_dir, unique_image_filename))

        # 关键：使用 cls 调用其他方法
        hotspots, js_popups = cls._collect_hotspots_for_session(session, media_dir, path_prefix="../")
        image_path_for_css = f"{images_dir_name}/{unique_image_filename}"

        context = {"page_num": page_num, "image_filename": image_path_for_css, "hotspots": hotspots,
                   "page_js_popups": '\n'.join(js_popups)}
        fragment_content = template_manager.render('flipbook_single/page.html.j2', **context)
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(fragment_content)
            parent_window.statusBar().showMessage(f"单页画册片段已成功更新。", 4000)
        except Exception as e:
            QMessageBox.critical(parent_window, "导出失败", f"写入HTML文件时发生错误: {e}")