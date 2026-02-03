# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_commit_geometry_change.py
#
# 功能: 提供 commit_geometry_change 方法，用于提交对单个热区几何属性的修改。

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QPointF, QSizeF

# --- Project-specific Imports ---
from commands import GeometryChangeCommand

class CommitGeometryChangeMixin:
    """
    一个 Mixin 类，包含用于提交单个热区几何属性更改的方法。
    """
    def commit_geometry_change(self):
        """
        将在属性面板中对单个热区几何属性的修改提交到撤销栈。

        此方法被 `on_geometry_field_committed` 在单选模式下调用。

        流程：
        1. 检查是否有单个选中的热区项。
        2. 从 `txt_x`, `txt_y`, `txt_width`, `txt_height` 输入框读取文本。
        3. 验证输入值是否为有效的正数。如果无效，则显示警告并中止。
        4. 获取热区项修改前的旧位置和尺寸。
        5. 比较新旧值，如果没有任何变化，则不执行任何操作。
        6. 创建一个 `GeometryChangeCommand` 命令，包含新旧几何数据。
        7. 将命令推送到当前页面的撤销栈。
        """
        # 1. 检查前提条件
        if not self.active_session or not self.active_session.scene.selectedItems():
            return
            
        selected_items = self.active_session.scene.selectedItems()
        if len(selected_items) != 1:
            return
            
        item = selected_items[0]
        
        # 2. 读取并验证输入
        try:
            x = float(self.txt_x.text())
            y = float(self.txt_y.text())
            w = float(self.txt_width.text())
            h = float(self.txt_height.text())
            # 宽度和高度必须是正数
            assert w > 0 and h > 0
        except (ValueError, AssertionError):
            QMessageBox.warning(self, "输入错误", "请输入有效的几何坐标，且宽高必须为正数。")
            self.update_hotspot_info() # 恢复输入框为项目的原始值
            return
            
        # 4. 获取旧值并构造新值
        old_pos = item.pos()
        old_size = item.rect().size()
        new_pos = QPointF(x, y)
        new_size = QSizeF(w, h)
        
        # 5. 检查是否有实际变化
        if old_pos == new_pos and old_size == new_size:
            return
            
        # 6. 创建命令
        command = GeometryChangeCommand(item, old_pos, old_size, new_pos, new_size)
        
        # 7. 推送命令到撤销栈
        self.active_session.undo_stack.push(command)