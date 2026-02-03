# D:\projects\singlepage\hotspot_editor\exporter_parts\_mixin_export_as_dynamic_page.py
import os
import shutil
from template_manager import template_manager


class ExportAsDynamicPageMixin:
    @classmethod
    def export_as_dynamic_page(cls, parent_window, project_path: str):
        if not parent_window.sessions: return None

        # --- 路径定义 ---
        current_dir = os.path.dirname(__file__)
        hotspot_editor_root = os.path.abspath(os.path.join(current_dir, '..'))
        templates_root_dir = os.path.join(hotspot_editor_root, 'templates')

        media_dir = os.path.join(project_path, "media")
        scroll_view_pages_dir = os.path.join(project_path, "pages_scroll")
        scroll_view_images_dir = os.path.join(project_path, "images_scroll")

        # --- 目录清理和创建 ---
        if os.path.exists(scroll_view_pages_dir): shutil.rmtree(scroll_view_pages_dir)
        if os.path.exists(scroll_view_images_dir): shutil.rmtree(scroll_view_images_dir)
        os.makedirs(scroll_view_pages_dir, exist_ok=True)
        os.makedirs(scroll_view_images_dir, exist_ok=True)
        os.makedirs(media_dir, exist_ok=True)  # 确保 media 目录存在

        # --- 渲染页面片段 ---
        page_filenames = []
        for i, session in enumerate(parent_window.sessions):
            page_num = i + 1
            _, ext = os.path.splitext(session.image_path)
            unique_image_filename = f"page-img-{page_num}{ext}"
            shutil.copy(session.image_path, os.path.join(scroll_view_images_dir, unique_image_filename))

            # 注意 path_prefix，因为 fragment.html 在 pages_scroll/ 目录下
            hotspots, _ = cls._collect_hotspots_for_session(session, media_dir, path_prefix="../")

            fragment_context = {
                "page_num": page_num,
                "image_filename": f"images_scroll/{unique_image_filename}",
                "hotspots": hotspots
            }
            fragment_content = template_manager.render('dynamic_page/scroll_view/fragment.html.j2', **fragment_context)
            page_filename = f"page_{page_num}.html"
            with open(os.path.join(scroll_view_pages_dir, page_filename), "w", encoding="utf-8") as f: f.write(
                fragment_content)
            page_filenames.append(f"pages_scroll/{page_filename}")

        # --- 渲染主入口文件 ---
        nav_html = cls._generate_outline_html(parent_window.outline_data, "#page-")

        index_context = {
            "project_title": "动态加载页面", "nav_html": nav_html,
            "page_filenames": page_filenames,
            "hotspot_style": cls._get_hotspot_style_context()
        }
        index_content = template_manager.render('dynamic_page/scroll_view/index.html.j2', **index_context)

        with open(os.path.join(project_path, "index_scroll.html"), "w", encoding="utf--8") as f:
            f.write(index_content)

        try:
            # --- 复制专属静态资源 ---
            source_static_dir = os.path.join(templates_root_dir, "dynamic_page", "static")
            dest_static_dir = os.path.join(project_path, "static_scroll")
            if os.path.exists(dest_static_dir): shutil.rmtree(dest_static_dir)
            shutil.copytree(source_static_dir, dest_static_dir)

            # --- *** 核心修复: 复制共享资源和 JS 库 *** ---
            # 1. 复制 shared_assets
            source_shared_assets_dir = os.path.join(templates_root_dir, "shared_assets")
            dest_shared_assets_dir = os.path.join(project_path, "shared_assets")
            if os.path.exists(dest_shared_assets_dir): shutil.rmtree(dest_shared_assets_dir)
            shutil.copytree(source_shared_assets_dir, dest_shared_assets_dir)

            # 2. 复制 React 等 JS 库到项目根目录的 js 文件夹
            shared_js_dir = os.path.join(hotspot_editor_root, "js")
            dest_root_js_dir = os.path.join(project_path, "js")
            os.makedirs(dest_root_js_dir, exist_ok=True)
            shutil.copy(os.path.join(shared_js_dir, "react.development.js"), dest_root_js_dir)
            shutil.copy(os.path.join(shared_js_dir, "react-dom.development.js"), dest_root_js_dir)
            shutil.copy(os.path.join(shared_js_dir, "babel.min.js"), dest_root_js_dir)
            # --- *** 修复结束 *** ---

        except Exception as e:
            print(f"Warning: Could not copy static assets for dynamic_page. {e}")

        parent_window.statusBar().showMessage(f"动态网页（长滚动）导出成功！", 5000)
        return project_path