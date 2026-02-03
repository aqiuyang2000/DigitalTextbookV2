# FILE: _mixin_export_as_modular_flipbook.py (FIXED & ENHANCED)

import os
import json
import shutil
import mimetypes
from jinja2 import Environment, FileSystemLoader
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor

from graphics_items import AbstractResizableItem, ResizableEllipseItem
from utils import create_default_data  # 导入 create_default_data


class ExportAsModularFlipbookMixin:
    """
    一个 Mixin 类，为 ExporterFlip 提供导出双页翻书画册的核心功能。
    """

    @classmethod
    def export_as_modular_flipbook(cls, parent_window, project_path: str):
        if not parent_window.sessions:
            return

        try:
            # --- 路径设置 ---
            current_dir = os.path.dirname(__file__)
            hotspot_editor_root = os.path.abspath(os.path.join(current_dir, '..'))
            templates_root_dir = os.path.join(hotspot_editor_root, 'templates')
            env = Environment(loader=FileSystemLoader(templates_root_dir))
            source_modular_assets_dir = os.path.join(templates_root_dir, "flipbook_modular_assets")
            dest_static_dir = os.path.join(project_path, "static_flip")
            source_shared_assets_dir = os.path.join(templates_root_dir, "shared_assets")
            dest_shared_assets_dir = os.path.join(project_path, "shared_assets")

            # --- 目录创建与资源复制 ---
            pages_dir = os.path.join(project_path, "pages")
            images_dir = os.path.join(project_path, "images")
            js_dir = os.path.join(project_path, "js")
            media_dir = os.path.join(project_path, "media")
            if os.path.exists(pages_dir): shutil.rmtree(pages_dir)
            if os.path.exists(dest_static_dir): shutil.rmtree(dest_static_dir)
            if os.path.exists(dest_shared_assets_dir): shutil.rmtree(dest_shared_assets_dir)
            shutil.copytree(source_shared_assets_dir, dest_shared_assets_dir)
            for d in [pages_dir, images_dir, js_dir, media_dir]: os.makedirs(d, exist_ok=True)
            shutil.copytree(source_modular_assets_dir, dest_static_dir)

            total_pages = len(parent_window.sessions)

            for i, session in enumerate(parent_window.sessions):
                page_num = i + 1
                _, ext = os.path.splitext(session.image_path)
                unique_image_filename = f"page-img-{page_num}{ext}"
                shutil.copy(session.image_path, os.path.join(images_dir, unique_image_filename))

                page_hotspots = []
                image_width, image_height = session.image_width, session.image_height
                if image_width == 0 or image_height == 0: continue

                for item_index, item in enumerate(session.scene.items()):
                    if not isinstance(item, AbstractResizableItem) or not item.data(0): continue
                    data, scene_rect = item.data(0), item.sceneBoundingRect()

                    hotspot_info = {
                        "shape": "ellipse" if isinstance(item, ResizableEllipseItem) else "rectangle",
                        "rect": {"x_rel": (scene_rect.left() / image_width) * 100,
                                 "y_rel": (scene_rect.top() / image_height) * 100,
                                 "w_rel": (scene_rect.width() / image_width) * 100,
                                 "h_rel": (scene_rect.height() / image_height) * 100},
                        'href': '#', 'target': '', 'onclick': '', 'description': data.get("description", ""),
                        'icon_type': data.get("icon_type", "default"), 'media_type': 'link',
                        'popup_width': 800, 'popup_height': 600,
                        'aspect_ratio': 'free',
                    }

                    htype = data.get("hotspot_type", "url")
                    if htype == "url":
                        udata = data.get("url_data", create_default_data()["url_data"])
                        hotspot_info["href"] = udata.get("url", "#")
                        hotspot_info["target"] = udata.get("target", "_blank")
                        hotspot_info["popup_width"] = udata.get('popup_width', 800)
                        hotspot_info["popup_height"] = udata.get('popup_height', 600)
                        hotspot_info['aspect_ratio'] = udata.get('aspect_ratio', 'free')

                        if hotspot_info["href"].lower().endswith(('.mp4', '.mov', '.webm')):
                            hotspot_info['media_type'] = 'video_url'

                    elif htype == "file":
                        fdata = data.get("file_data", create_default_data()["file_data"])
                        source_path = fdata.get("source_path")
                        if not source_path or not os.path.exists(source_path): continue

                        media_filename = os.path.basename(source_path)
                        destination_path = os.path.join(project_path, 'media', media_filename)
                        media_relative_path = f"media/{media_filename}"
                        os.makedirs(os.path.join(project_path, 'media'), exist_ok=True)
                        if not os.path.exists(destination_path) or not os.path.samefile(source_path, destination_path):
                            shutil.copy(source_path, destination_path)

                        hotspot_info['href'] = media_relative_path
                        hotspot_info['target'] = fdata.get("display", "popup")
                        hotspot_info['popup_width'] = fdata.get('popup_width', 800)
                        hotspot_info['popup_height'] = fdata.get('popup_height', 600)
                        hotspot_info['aspect_ratio'] = fdata.get('aspect_ratio', 'free')

                        mime_type, _ = mimetypes.guess_type(media_relative_path)
                        if mime_type:
                            if mime_type.startswith("audio/"):
                                hotspot_info['media_type'] = 'audio'
                            elif mime_type.startswith("video/"):
                                hotspot_info['media_type'] = 'video'
                            elif mime_type.startswith("image/"):
                                hotspot_info['media_type'] = 'image'
                            elif mime_type == "application/pdf":
                                hotspot_info['media_type'] = 'pdf'

                    page_hotspots.append(hotspot_info)

                page_template = env.get_template('flipbook_modular/page.html.j2')
                page_context = {"image_path": f"images/{unique_image_filename}", "hotspots": page_hotspots}
                page_content = page_template.render(**page_context)
                with open(os.path.join(pages_dir, f"page-{page_num}.html"), "w", encoding="utf-8") as f:
                    f.write(page_content)

            # --- 渲染主入口文件 ---
            outline_html = cls._generate_recursive_outline_for_flipbook(parent_window.outline_data)

            # --- *** 核心修复: 完整读取所有样式设置，包括 outline *** ---
            settings = QSettings("MyCompany", "HotspotEditor")
            fill_color = settings.value("export/fill_color", QColor(255, 165, 0))
            opacity = settings.value("export/opacity_percent", 40, type=int) / 100.0

            # 读取提纲设置
            outline_pos = settings.value("outline/position", "bottom-left")
            outline_behavior = settings.value("outline/behavior", "auto_hide")
            outline_font_size = settings.value("outline/font_size", 16, type=int)
            outline_indent = settings.value("outline/indent", 1.0, type=float)
            icon_size = settings.value("export/control_icon_size", 24, type=int)

            hotspot_style_context = {
                "fill_color_rgba": f"rgba({fill_color.red()}, {fill_color.green()}, {fill_color.blue()}, {opacity})",
                "hover_fill_color_rgba": f"rgba({fill_color.red()}, {fill_color.green()}, {fill_color.blue()}, {opacity + 0.2})",
                "has_border": settings.value("export/has_border", True, type=bool),
                "border_color_hex": settings.value("export/border_color", QColor(255, 165, 0)).name(),
                "border_width_px": settings.value("export/border_width", 2, type=int),
                "control_icon_size_px": icon_size,

                # 这里的键名必须是 outline，以匹配模板中的 hotspot_style.outline
                "outline": {
                    "position": outline_pos,
                    "behavior": outline_behavior,
                    "font_size_px": outline_font_size,
                    "indent_em": outline_indent
                }
            }
            # --- *** 修复结束 *** ---

            context = {"project_title": "翻书画册", "nav_html": outline_html, "total_pages": total_pages,
                       "hotspot_style": hotspot_style_context}
            index_template = env.get_template('flipbook_modular/index.html.j2')
            index_content = index_template.render(**context)
            with open(os.path.join(project_path, "index.html"), "w", encoding="utf-8") as f:
                f.write(index_content)

            # --- 复制JS库 ---
            shared_js_dir = os.path.join(hotspot_editor_root, "js")
            dest_root_js_dir = os.path.join(project_path, "js")
            shutil.copy(os.path.join(shared_js_dir, "jquery.min.js"), js_dir)
            shutil.copy(os.path.join(shared_js_dir, "turn.min.js"), js_dir)
            shutil.copy(os.path.join(shared_js_dir, "modernizr.min.js"), js_dir)
            shutil.copy(os.path.join(shared_js_dir, "react.development.js"), dest_root_js_dir)
            shutil.copy(os.path.join(shared_js_dir, "react-dom.development.js"), dest_root_js_dir)
            shutil.copy(os.path.join(shared_js_dir, "babel.min.js"), dest_root_js_dir)

            parent_window.statusBar().showMessage(f"双页画册导出成功！", 5000)
        except Exception as e:
            import traceback
            # 打印完整的堆栈跟踪，以便调试
            print(traceback.format_exc())
            QMessageBox.critical(parent_window, "导出失败", f"发生严重错误: {e}\n{traceback.format_exc()}")