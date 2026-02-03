# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_active_session_property.py
#
# 功能: 提供 active_session @property，用于便捷地访问当前活动会话。

class ActiveSessionPropertyMixin:
    """
    一个 Mixin 类，将 active_session 实现为一个只读属性。
    """
    @property
    def active_session(self):
        """
        一个只读属性，用于安全地获取当前活动的 ImageEditingSession 实例。

        它封装了检查索引有效性的逻辑。如果当前 `active_session_index`
        是一个有效的索引，则返回 `self.sessions` 列表中对应的会话对象；
        否则，返回 `None`。

        这使得在其他代码中可以简单地使用 `if self.active_session:` 来判断
        是否存在活动会话，而无需关心索引的具体值。

        Returns:
            ImageEditingSession or None: 当前活动的会话实例，或在没有
                                         活动会话时返回 None。
        """
        # 检查 active_session_index 是否在 sessions 列表的有效范围内
        if 0 <= self.active_session_index < len(self.sessions):
            return self.sessions[self.active_session_index]
        
        # 如果索引无效（例如，-1 或超出范围），则返回 None
        return None