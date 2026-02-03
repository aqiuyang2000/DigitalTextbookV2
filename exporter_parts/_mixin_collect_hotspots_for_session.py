# FILE: D:\projects\singlepage\hotspot_editor\exporter_parts\_mixin_collect_hotspots_for_session.py

import os
import shutil
import json
import mimetypes
from graphics_items import AbstractResizableItem, ResizableEllipseItem
from utils import create_default_data  # 导入 create_default_data


class CollectHotspotsForSessionMixin:
    @classmethod
    def _collect_hotspots_for_session(cls, session, media_dir: str, path_prefix=""):
        hotspots_data, js_popups = [], []
        image_width, image_height = session.image_width, session.image_height
        if image_width == 0 or image_height == 0: return [], []

        page_num = session.main_window.sessions.index(session) + 1

        for item_index, item in enumerate(session.scene.items()):
            if not isinstance(item, AbstractResizableItem) or not item.data(0): continue
            data = item.data(0)
            scene_rect = item.sceneBoundingRect()
            is_ellipse = isinstance(item, ResizableEllipseItem)

            hotspot_info = {
                'rel_x': (scene_rect.left() / image_width) * 100,
                'rel_y': (scene_rect.top() / image_height) * 100,
                'rel_w': (scene_rect.width() / image_width) * 100,
                'rel_h': (scene_rect.height() / image_height) * 100,
                'is_circle': is_ellipse, 'href': '#', 'target': '', 'onclick': '',
                'description': data.get("description", ""),
                'icon_type': data.get("icon_type", "default"),
                'media_type': 'link',
                'popup_width': 800,
                'popup_height': 600,
                # --- *** 核心修改 1/3: 添加 aspect_ratio 字段 *** ---
                'aspect_ratio': 'free',
            }

            htype = data.get("hotspot_type", "url")
            if htype == "url":
                udata = data.get("url_data", create_default_data()["url_data"])
                url, target = udata.get("url", "#"), udata.get("target", "_blank")

                hotspot_info['href'] = url
                hotspot_info['target'] = target
                hotspot_info['popup_width'] = udata.get('popup_width', 800)
                hotspot_info['popup_height'] = udata.get('popup_height', 600)
                # --- *** 核心修改 2/3: 传递 URL 宽高比 *** ---
                hotspot_info['aspect_ratio'] = udata.get('aspect_ratio', 'free')

                if url.lower().endswith(('.mp4', '.mov', '.webm')):
                    hotspot_info['media_type'] = 'video_url'

                if target == "popup":
                    hotspot_info[
                        'onclick'] = f"window.open('{url}', '_blank', 'width={hotspot_info['popup_width']},height={hotspot_info['popup_height']},resizable=yes,scrollbars=yes'); return false;"

            elif htype == "file":
                fdata = data.get("file_data", create_default_data()["file_data"])
                source_path = fdata.get("source_path")
                if not source_path or not os.path.exists(source_path): continue

                media_filename = os.path.basename(source_path)
                destination_path = os.path.join(media_dir, media_filename)

                if not os.path.exists(destination_path) or not os.path.samefile(source_path, destination_path):
                    os.makedirs(media_dir, exist_ok=True)
                    shutil.copy(source_path, destination_path)

                media_relative_path = f"{path_prefix}media/{media_filename}"
                hotspot_info['href'] = media_relative_path
                hotspot_info['target'] = fdata.get("display", "popup")
                hotspot_info['popup_width'] = fdata.get('popup_width', 800)
                hotspot_info['popup_height'] = fdata.get('popup_height', 600)
                # --- *** 核心修改 3/3: 传递文件宽高比 *** ---
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

            hotspots_data.append(hotspot_info)

        return hotspots_data, []