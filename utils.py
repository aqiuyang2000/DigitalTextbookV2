# FILE: D:\projects\singlepage\hotspot_editor\utils.py

def create_default_data():
    """创建一个新的热区时使用的默认数据结构。"""
    return {
        "id": None,
        "description": "",
        "hotspot_type": "file",
        "icon_type": "default",

        "url_data": {
            "url": "#",
            # --- *** 核心修改 1/2: 将URL的默认打开方式改为'embed' *** ---
            "target": "embed",
            # --- *** 修改结束 *** ---
            "popup_width": 800,
            "popup_height": 600,
            "aspect_ratio": "free"
        },
        "file_data": {
            "source_path": "",
            # --- *** 核心修改 2/2: 将文件的默认显示方式改为'embed' *** ---
            "display": "embed",
            # --- *** 修改结束 *** ---
            "popup_width": 800,
            "popup_height": 600,
            "aspect_ratio": "free"
        }
    }