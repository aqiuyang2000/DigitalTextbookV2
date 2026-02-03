# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_ensure_output_directory.py
#
# 功能: 提供 _ensure_output_directory 輔助方法，用於創建專案的完整輸出目錄結構。

import os

class EnsureOutputDirectoryMixin:
    """
    一個 Mixin 類，包含用於確保專案輸出目錄結構存在的輔助方法。
    """
    def _ensure_output_directory(self):
        """
        確保專案的根輸出目錄 (`_out`) 及其所有必需的子目錄都存在。

        如果目錄不存在，此方法會使用 `os.makedirs` 創建它們。
        `os.makedirs` 的 `exist_ok=True` 參數確保了即使目錄已經存在，
        也不會引發錯誤。

        這個方法通常在新建專案或另存為專案後被呼叫。
        """
        # 1. 獲取根輸出目錄的路徑
        out_dir = self._get_output_directory()
        
        # 如果無法獲取輸出目錄（例如專案尚未保存），則不執行任何操作
        if not out_dir:
            return

        # 2. 定義所有需要被創建的子目錄的相對路徑列表
        #    這個列表定義了專案輸出目錄的完整結構。
        dirs_to_create = [
            "", # 根輸出目錄本身
            "images", 
            "js", 
            "media", 
            "pages",
            # 單頁畫冊的資源目錄
            "pages_single", 
            "images_single",
            # 長網頁的資源目錄
            "pages_scroll", 
            "images_scroll",
            # 工作區目錄
            "workspace", 
            "workspace/sources", 
            "workspace/assets"
        ]
        
        # 3. 遍歷列表並創建每一個目錄
        for d in dirs_to_create:
            # 使用 os.path.join 拼接出絕對路徑
            full_path = os.path.join(out_dir, d)
            # 創建目錄，exist_ok=True 確保了如果目錄已存在也不會報錯
            os.makedirs(full_path, exist_ok=True)