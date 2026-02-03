# D:\projects-singlepage\hotspot_editor\main_window_parts\_mixin_generate_new_hotspot_id.py
#
# 功能: 提供 generate_new_hotspot_id 辅助方法，用于为新热区生成唯一的ID。

# --- Project-specific Imports ---
# 导入 ImageEditingSession 用于类型提示
from image_editing_session import ImageEditingSession

class GenerateNewHotspotIdMixin:
    """
    一个 Mixin 类，包含用于为新热区生成全局唯一 ID 的辅助方法。
    """
    def generate_new_hotspot_id(self, session: ImageEditingSession) -> str | None:
        """
        为一个新的热区生成一个全局唯一的、带语义的 ID 字符串。

        ID 的格式为: `<project_id>_p<page_index>_h<hotspot_index>`
        例如: `PROJ_a1b2c3d4_p3_h15`

        - `project_id`: 整个项目的唯一标识符。
        - `page_index`: 热区所在页面在项目中的索引 (从0开始)。
        - `hotspot_index`: 热区在该页面内的唯一自增ID，由对应页面的
                         `ImageEditingSession` 实例管理。

        Args:
            session (ImageEditingSession): 新热区将要被添加到的会话。

        Returns:
            str | None: 如果成功生成，则返回 ID 字符串；如果项目尚未
                        保存 (没有 project_id) 或 session 无效，则返回 None。
        """
        # 1. 前置检查
        if not self.project_id or not session:
            return None

        # 2. 获取页面索引
        #    通过 session 对象在 self.sessions 列表中的位置来确定页面索引
        try:
            page_id = self.sessions.index(session)
        except ValueError:
            # 如果 session 不在列表中，则无法确定页面ID，返回 None
            return None
        
        # 3. 从 session 获取页面内部的热区自增ID
        hotspot_id_counter = session.get_next_hotspot_id()
        
        # 4. 格式化并返回最终的 ID 字符串
        return f"{self.project_id}_p{page_id}_h{hotspot_id_counter}"