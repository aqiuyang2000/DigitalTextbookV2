# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_on_outline_changed.py
#
# 功能: 提供 _on_outline_changed 槽函数，用于在提纲数据变化时同步状态。

class OnOutlineChangedMixin:
    """
    一个 Mixin 类，包含 _on_outline_changed 槽函数，用于响应提纲编辑器的
    内容变更事件。
    """
    def _on_outline_changed(self, new_outline_data: list):
        """
        当 `OutlineEditorWidget` 中的提纲数据发生变化时被调用的槽函数。

        此方法接收从 `OutlineEditorWidget` 发送过来的、代表了当前最新
        树状结构的列表数据，并将其更新到主窗口的 `self.outline_data` 属性中。
        同时，它会调用 `set_dirty(True)` 来标记项目存在未保存的更改。

        Args:
            new_outline_data (list): 最新的提纲数据结构。
        """
        # 1. 更新主窗口持有的提纲数据副本
        self.outline_data = new_outline_data
        
        # 2. 标记项目为“已修改”状态
        self.set_dirty(True)