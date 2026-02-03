# FILE: _mixin_export_double_page_fragment.py (FIXED)

import os
import shutil
import json
from jinja2 import Environment, FileSystemLoader
from PySide6.QtWidgets import QMessageBox

# 导入与完整导出相同的依赖
from graphics_items import AbstractResizableItem, ResizableEllipseItem


class ExportDoublePageFragmentMixin:
    """
    一个 Mixin 类，为 ExporterFlip 提供导出单个双页画册页面片段的功能。
    (已更新以支持松耦合模板)
    """

    @classmethod
    def export_double_page_fragment(cls, parent_window, output_dir):
        """
        仅导出或更新当前活动页面的、自包含的HTML片段。
        """
        if not parent_window.active_session:
            QMessageBox.warning(parent_window, "错误", "没有选择任何页面可供导出。")
            return

        session = parent_window.active_session
        page_num = parent_window.active_session_index + 1

        try:
            # --- 路径与模板设置 (与完整导出逻辑一致) ---
            current_dir = os.path.dirname(__file__)
            hotspot_editor_root = os.path.abspath(os.path.join(current_dir, '..'))
            templates_root_dir = os.path.join(hotspot_editor_root, 'templates')
            env = Environment(loader=FileSystemLoader(templates_root_dir))
            page_template = env.get_template('flipbook_modular/page.html.j2')

            # --- 目录创建 (保持不变) ---
            pages_dir = os.path.join(output_dir, "pages");
            images_dir = os.path.join(output_dir, "images")
            os.makedirs(pages_dir, exist_ok=True);
            os.makedirs(images_dir, exist_ok=True)

            # --- 复制图片 (保持不变) ---
            _, ext = os.path.splitext(session.image_path)
            unique_image_filename = f"page-img-{page_num}{ext}"
            shutil.copy(session.image_path, os.path.join(images_dir, unique_image_filename))

            page_hotspots = []
            js_popups_to_inject = []

            # --- *** 核心修复 1/2: 获取图片尺寸 *** ---
            image_width, image_height = session.image_width, session.image_height
            if image_width > 0 and image_height > 0:

                for item_index, item in enumerate(session.scene.items()):
                    if not isinstance(item, AbstractResizableItem) or not item.data(0): continue
                    data, scene_rect = item.data(0), item.sceneBoundingRect()

                    # --- *** 核心修复 2/2: 计算并使用百分比值 *** ---
                    hotspot_info = {
                        "shape": "ellipse" if isinstance(item, ResizableEllipseItem) else "rectangle",
                        "rect": {
                            "x_rel": (scene_rect.left() / image_width) * 100,
                            "y_rel": (scene_rect.top() / image_height) * 100,
                            "w_rel": (scene_rect.width() / image_width) * 100,
                            "h_rel": (scene_rect.height() / image_height) * 100
                        },
                        "href": "#", "target": "", "onclick": ""
                    }
                    # --- *** 修复结束 *** ---

                    htype = data.get("hotspot_type", "url")
                    if htype == "url":
                        udata = data.get("url_data", {});
                        hotspot_info["href"] = udata.get("url", "#");
                        hotspot_info["target"] = udata.get("target", "_blank")
                    elif htype == "file":
                        fdata = data.get("file_data", {});
                        source_path = fdata.get("source_path")
                        if not source_path or not os.path.exists(source_path): continue

                        media_filename = os.path.basename(source_path);
                        destination_path = os.path.join(output_dir, 'media', media_filename)
                        media_relative_path = f"media/{media_filename}"

                        os.makedirs(os.path.join(output_dir, 'media'), exist_ok=True)

                        if not os.path.exists(destination_path) or not os.path.samefile(source_path, destination_path):
                            shutil.copy(source_path, destination_path)

                        tag = cls._generate_media_tag_for_flipbook(media_relative_path)
                        js_body = f'<html><head><title>{media_filename}</title><style>body{{margin:0;display:flex;justify-content:center;align-items:center;background:#333;}}</style></head><body>{tag}</body></html>'
                        js_body_safe = json.dumps(js_body)
                        func_name = f"openMediaPopup_p{page_num}_{item_index}"
                        popup_w, popup_h = fdata.get('popup_width', 800), fdata.get('popup_height', 600)

                        js_popups_to_inject.append(
                            f"function {func_name}(){{var w=window.open('','{func_name}','width={popup_w},height={popup_h},resizable=yes,scrollbars=yes');w.document.write({js_body_safe});w.document.close();return false;}}")
                        hotspot_info['onclick'] = f"return {func_name}();"
                    page_hotspots.append(hotspot_info)

            page_context = {
                "image_path": f"images/{unique_image_filename}",
                "hotspots": page_hotspots
            }
            page_content = page_template.render(**page_context)
            save_path = os.path.join(pages_dir, f"page-{page_num}.html")

            with open(save_path, "w", encoding="utf-8") as f:
                f.write(page_content)

            parent_window.statusBar().showMessage(f"双页画册片段已成功更新。", 4000)

        except Exception as e:
            import traceback
            QMessageBox.critical(parent_window, "片段导出失败",
                                 f"写入HTML文件时发生错误: {e}\n{traceback.format_exc()}")