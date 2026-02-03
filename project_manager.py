# FILE: project_manager.py (带有调试代码和修复)
import json
import os
import shutil
from graphics_items import AbstractResizableItem, ResizableEllipseItem


class ProjectManager:
    def _get_safe_relative_path(self, target_path: str, start_dir: str) -> str:
        if not target_path or not os.path.exists(target_path): return ""
        try:
            return os.path.relpath(target_path, start_dir)
        except ValueError:
            project_root = os.path.dirname(start_dir)
            assets_dir = os.path.join(project_root, "_project_assets")
            subfolder = "media"
            _, ext = os.path.splitext(target_path)
            if ext.lower() in ['.png', '.jpg', '.jpeg', '.bmp']:
                subfolder = "images"
            elif ext.lower() == '.pdf':
                subfolder = "pdfs"
            final_assets_dir = os.path.join(assets_dir, subfolder)
            os.makedirs(final_assets_dir, exist_ok=True)
            filename = os.path.basename(target_path)
            destination_path = os.path.join(final_assets_dir, filename)
            if not os.path.exists(destination_path) or not os.path.samefile(target_path, destination_path):
                shutil.copy2(target_path, destination_path)
            return os.path.relpath(destination_path, start_dir)

    def save_project(self, sessions: list, project_path: str, project_id: str, outline_data: list):
        print("\n--- DEBUG: Entering save_project ---")
        project_data = {'project_id': project_id, 'outline': outline_data, 'pages': []}
        project_dir = os.path.dirname(project_path)

        # --- 核心修复：不再使用 set 来去重，而是为每个 session 单独保存 ---
        # 之前的 set 逻辑在处理独立图片和来自不同PDF的页面时会产生问题

        for i, session in enumerate(sessions):
            print(f"  [SAVE] Processing session #{i}:")

            # --- 调试点 1: 打印每个 session 的核心路径信息 ---
            print(f"    - Session Image Path: {session.image_path}")
            print(f"    - Session Original PDF Path: {session.original_multipage_pdf_path}")

            # --- 逻辑主体：为每个 session 创建一个独立的 page_data 条目 ---
            # original_multipage_pdf_path 是关键，它标识了页面的来源
            source_pdf_path = session.original_multipage_pdf_path

            # 即使是单张图片（没有原始PDF），也应该有一个条目
            # 对于单张图片，它的 image_path 就是它的源
            source_path_for_assets = source_pdf_path if source_pdf_path else session.image_path

            import hashlib
            source_filename = os.path.basename(source_path_for_assets)

            # 复制源文件到工作区 (如果它是一个PDF且还不存在)
            workspace_source_rel = ""
            if source_pdf_path:
                workspace_sources_dir = os.path.join(self._get_workspace_dir(project_path), "sources")
                os.makedirs(workspace_sources_dir, exist_ok=True)
                dest_source_path = os.path.join(workspace_sources_dir, os.path.basename(source_pdf_path))
                if not os.path.exists(dest_source_path):
                    shutil.copy2(source_pdf_path, dest_source_path)
                workspace_source_rel = os.path.relpath(dest_source_path, project_dir)

            # 资产目录路径
            asset_dir_name = hashlib.md5(source_filename.encode()).hexdigest()
            asset_dir_rel_path = os.path.join(
                f"{os.path.splitext(os.path.basename(project_path))[0]}_out",
                "workspace", "assets", asset_dir_name
            )

            # --- 调试点 2: 打印将要保存的相对路径 ---
            print(f"    - Saving workspace_source_rel: {workspace_source_rel}")
            print(f"    - Saving workspace_assets_rel: {asset_dir_rel_path}")

            page_data = {
                'source_pdf_path_rel': self._get_safe_relative_path(source_pdf_path, project_dir),
                'workspace_source_rel': workspace_source_rel,
                'workspace_assets_rel': asset_dir_rel_path,
                # 关键：现在保存的是单个页面的信息
                'page_index_in_source': session.source_page_index if hasattr(session, 'source_page_index') else i,
                # 记录这是源的第几页
                'hotspots': [],
                'next_hotspot_id': session._next_hotspot_id
            }

            # 热区保存逻辑保持不变
            for item in session.scene.items():
                if isinstance(item, AbstractResizableItem):
                    item_custom_data = item.data(0).copy() if item.data(0) else {}
                    if item_custom_data.get('hotspot_type') == 'file':
                        file_data = item_custom_data.get('file_data', {}).copy()
                        source_path = file_data.get('source_path')
                        if source_path: file_data['source_path'] = self._get_safe_relative_path(source_path,
                                                                                                project_dir)
                        item_custom_data['file_data'] = file_data
                    hotspot_data = {
                        'pos': {'x': item.pos().x(), 'y': item.pos().y()},
                        'rect': {'w': item.rect().width(), 'h': item.rect().height()},
                        'type': 'ellipse' if isinstance(item, ResizableEllipseItem) else 'rectangle',
                        'data': item_custom_data
                    }
                    page_data['hotspots'].append(hotspot_data)

            project_data['pages'].append(page_data)

        print("--- DEBUG: Finished save_project ---\n")
        with open(project_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=4)

    # 新增一个辅助方法
    def _get_workspace_dir(self, project_path):
        return os.path.join(
            os.path.dirname(project_path),
            f"{os.path.splitext(os.path.basename(project_path))[0]}_out",
            "workspace"
        )

    def load_project(self, project_path: str) -> dict:
        # load_project 逻辑暂时保持不变，但之后可能需要根据新的保存结构调整
        with open(project_path, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        project_dir = os.path.dirname(project_path)
        for page_group in project_data.get('pages', []):
            for key in ['source_pdf_path_rel', 'workspace_source_rel', 'workspace_assets_rel']:
                if page_group.get(key):
                    abs_key = key.replace('_rel', '_abs')
                    page_group[abs_key] = os.path.abspath(os.path.join(project_dir, page_group[key]))
            # for page_details in page_group.get('pages_hotspots', []):
            for hotspot in page_group.get('hotspots', []):
                data = hotspot.get('data', {})
                if data.get('hotspot_type') == 'file':
                    file_data = data.get('file_data', {})
                    source_path_rel = file_data.get('source_path')
                    if source_path_rel:
                        file_data['source_path'] = os.path.abspath(os.path.join(project_dir, source_path_rel))
        return project_data