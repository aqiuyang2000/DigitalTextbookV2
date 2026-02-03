# FILE: _mixin_export_as_single_page_flipbook.py (FINAL REFACTORED VERSION & PATH FIXED)
import os
import json
import shutil
from pathlib import Path
from PySide6.QtWidgets import QMessageBox
from template_manager import template_manager


class ExportAsSinglePageFlipbookMixin:
    """
    一个 Mixin 类，为 HtmlExporter 提供导出单页翻书画册的功能。
    (已更新以支持完全松耦合的模块化模板)
    """

    @classmethod
    def export_as_single_page_flipbook(cls, parent_window, project_path: str):
        if not parent_window.sessions: return None

        try:
            # --- 路径设置 ---
            current_dir = os.path.dirname(__file__)
            hotspot_editor_root = os.path.abspath(os.path.join(current_dir, '..'))
            templates_root_dir = os.path.join(hotspot_editor_root, 'templates')

            source_assets_dir = os.path.join(hotspot_editor_root, "templates", "flipbook_single_assets")
            dest_static_dir = os.path.join(project_path, "static_single")

            source_shared_assets_dir = os.path.join(templates_root_dir, "shared_assets")
            dest_shared_assets_dir = os.path.join(project_path, "shared_assets")

            # --- 目录创建与清理 ---
            media_dir = os.path.join(project_path, "media")
            flipbook_pages_dir = os.path.join(project_path, "pages_single")
            flipbook_images_dir = os.path.join(project_path, "images_single")

            if os.path.exists(flipbook_pages_dir): shutil.rmtree(flipbook_pages_dir)
            if os.path.exists(flipbook_images_dir): shutil.rmtree(flipbook_images_dir)
            if os.path.exists(dest_static_dir): shutil.rmtree(dest_static_dir)
            if os.path.exists(dest_shared_assets_dir): shutil.rmtree(dest_shared_assets_dir)

            os.makedirs(flipbook_pages_dir, exist_ok=True)
            os.makedirs(flipbook_images_dir, exist_ok=True)
            os.makedirs(media_dir, exist_ok=True)

            # --- 资源复制 ---
            shutil.copytree(source_assets_dir, dest_static_dir)
            shutil.copytree(source_shared_assets_dir, dest_shared_assets_dir)

            shared_js_dir = os.path.join(hotspot_editor_root, "js")

            # --- *** 核心修复: 将JS库复制到正确的位置 *** ---
            # 1. 复制 React 等库到项目根的 js/ 目录
            dest_root_js_dir = os.path.join(project_path, "js")
            os.makedirs(dest_root_js_dir, exist_ok=True)
            shutil.copy(os.path.join(shared_js_dir, "react.development.js"), dest_root_js_dir)
            shutil.copy(os.path.join(shared_js_dir, "react-dom.development.js"), dest_root_js_dir)
            shutil.copy(os.path.join(shared_js_dir, "babel.min.js"), dest_root_js_dir)

            # 2. 复制 turn.js 等库到 static_single/js/ 目录
            dest_single_js_dir = os.path.join(dest_static_dir, "js")
            os.makedirs(dest_single_js_dir, exist_ok=True)  # 确保 static_single/js 存在
            shutil.copy(os.path.join(shared_js_dir, "jquery.min.js"), dest_single_js_dir)
            shutil.copy(os.path.join(shared_js_dir, "modernizr.min.js"), dest_single_js_dir)
            shutil.copy(os.path.join(shared_js_dir, "turn.min.js"), dest_single_js_dir)
            # --- *** 修复结束 *** ---

            # --- 渲染逻辑 (保持不变) ---
            all_page_data = []
            for i, session in enumerate(parent_window.sessions):
                page_num = i + 1
                _, ext = os.path.splitext(session.image_path)
                unique_image_filename = f"page-img-{page_num}{ext}"
                shutil.copy(session.image_path, os.path.join(flipbook_images_dir, unique_image_filename))

                hotspots, _ = cls._collect_hotspots_for_session(session, media_dir, path_prefix="../")

                image_path_for_css = f"images_single/{unique_image_filename}"
                page_context = {
                    "page_num": page_num,
                    "image_filename": image_path_for_css,
                    "hotspots": hotspots
                }
                page_content = template_manager.render('flipbook_single/page.html.j2', **page_context)
                page_filename = f"page_{page_num}.html"
                with open(os.path.join(flipbook_pages_dir, page_filename), "w", encoding="utf-8") as f: f.write(
                    page_content)

                all_page_data.append({
                    "url": f"pages_single/{page_filename}",
                    "width": session.image_width,
                    "height": session.image_height
                })

            nav_html = cls._generate_outline_html(parent_window.outline_data, "#page/")

            index_context = {
                "project_title": "单页翻书画册", "nav_html": nav_html,
                "pages_data_json": json.dumps(all_page_data),
                "hotspot_style": cls._get_hotspot_style_context()
            }
            index_content = template_manager.render('flipbook_single/flipbook_view/index.html.j2', **index_context)

            with open(os.path.join(project_path, "index_single.html"), "w", encoding="utf-8") as f:
                f.write(index_content)

            parent_window.statusBar().showMessage(f"单页画册（左右翻）导出成功！", 5000)
            return project_path

        except Exception as e:
            import traceback
            QMessageBox.critical(parent_window, "导出失败",
                                 f"导出单页画册时发生严重错误: {e}\n{traceback.format_exc()}")
            return None