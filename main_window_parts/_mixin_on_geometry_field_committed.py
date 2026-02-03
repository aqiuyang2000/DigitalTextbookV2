# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_on_geometry_field_committed.py
#
# 功能: 提供 on_geometry_field_committed 槽函数，作为几何属性修改的统一入口。

class OnGeometryFieldCommittedMixin:
    """
    一个 Mixin 类，包含 on_geometry_field_committed 槽函数。
    """
    def on_geometry_field_committed(self):
        """
        当任一几何属性输入框（X, Y, 宽, 高）被提交（通常是按回车）时调用的槽函数。

        此方法会检查当前场景中的选中项数量：
        - 如果选中项多于一个，它会调用 `commit_batch_geometry_change` 
          来处理批量修改。
        - 如果只选中一个项，它会调用 `commit_geometry_change` 来处理
          单个修改。
        """
        if not self.active_session:
            return

        selected_items = self.active_session.scene.selectedItems()
        
        if len(selected_items) > 1:
            # 多选状态 -> 调用批量处理方法
            self.commit_batch_geometry_change()
        else:
            # 单选或无选状态 -> 调用单体处理方法
            # (commit_geometry_change 内部会处理无选中的情况)
            self.commit_geometry_change()