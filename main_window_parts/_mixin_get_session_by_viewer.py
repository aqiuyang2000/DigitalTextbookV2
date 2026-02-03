# D:\projects-singlepage\hotspot_editor\main_window_parts\_mixin_get_session_by_viewer.py
#
# 功能: 提供 get_session_by_viewer 辅助方法，用于通过 viewer 实例查找其对应的 session。

# --- Project-specific Imports ---
# 导入 PhotoViewer 和 ImageEditingSession 用于类型提示
from photo_viewer import PhotoViewer
from image_editing_session import ImageEditingSession

class GetSessionByViewerMixin:
    """
    一个 Mixin 类，包含一个辅助方法，用于通过 PhotoViewer 实例反向查找
    其对应的 ImageEditingSession 实例。
    """
    def get_session_by_viewer(self, viewer: PhotoViewer) -> ImageEditingSession | None:
        """
        根据给定的 PhotoViewer 控件实例，返回其管理的 ImageEditingSession。

        由于 `self.sessions` (数据模型列表) 和 `self.viewer_widgets` (视图列表)
        的索引是始终保持同步的，此方法可以通过查找 viewer 在其列表中的索引，
        来定位 session 在另一个列表中的对应项。

        Args:
            viewer (PhotoViewer): 需要查找其对应会话的 PhotoViewer 实例。

        Returns:
            ImageEditingSession | None: 如果找到，则返回对应的会话实例；
                                        否则返回 None。
        """
        # 1. 检查给定的 viewer 是否在我们管理的 viewer 列表中
        if viewer in self.viewer_widgets:
            # 2. 如果是，获取它在列表中的索引
            index = self.viewer_widgets.index(viewer)
            
            # 3. 使用相同的索引从 sessions 列表中返回对应的 session
            return self.sessions[index]
            
        # 4. 如果在列表中找不到该 viewer，则返回 None
        return None