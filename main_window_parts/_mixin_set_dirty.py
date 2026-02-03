# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_set_dirty.py
#
# 功能: 提供 set_dirty 方法，用於設定專案的「已修改」狀態。

class SetDirtyMixin:
    """
    一個 Mixin 類，包含用於設定專案「已修改」(dirty) 狀態的 set_dirty 方法。
    """
    def set_dirty(self, dirty=True):
        """
        設定專案是否有未儲存的變更。

        這會更新內部的 is_dirty 旗標，並立即呼叫 update_window_title
        來在視窗標題上反映這個狀態（通常是透過顯示或隱藏一個星號 *）。

        為了避免不必要的重複刷新，只有當新的狀態與當前狀態不同時，
        才會執行更新。

        Args:
            dirty (bool): True 表示有未儲存的變更，False 表示已儲存。
        """
        # 如果新的狀態與目前狀態相同，則不執行任何操作以提高效率
        if self.is_dirty == dirty:
            return
        
        # 更新內部狀態旗標
        self.is_dirty = dirty
        
        # 呼叫另一個 Mixin 中的方法來更新視窗標題
        self.update_window_title(dirty=self.is_dirty)