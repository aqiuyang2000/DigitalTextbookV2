# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_commit_batch_geometry_change.py
#
# 功能: 提供 commit_batch_geometry_change 方法，用于提交对多个热区几何属性的批量修改。

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox

# --- Project-specific Imports ---
from commands import BatchItemsGeometryCommand

class CommitBatchGeometryChangeMixin:
    """
    一个 Mixin 类，包含用于提交多个热区几何属性批量更改的方法。
    """
    def commit_batch_geometry_change(self):
        """
        将在属性面板中对多个热区几何属性的批量修改提交到撤销栈。

        此方法被 `on_geometry_field_committed` 在多选模式下调用。

        流程：
        1. 检查是否有多个选中的热区项。
        2. 创建一个 `geo_changes` 字典，只包含用户实际填写了新值的字段。
           (X, Y, W, H 输入框中任何一个为空都表示用户不想修改该属性)。
        3. 验证所有输入值是否为有效的数字。
        4. 如果 `geo_changes` 字典不为空（即用户至少修改了一个属性），
           则创建一个 `BatchItemsGeometryCommand` 命令。
        5. 将命令推送到当前页面的撤销栈。
        """
        # 1. 检查前提条件
        if not self.active_session:
            return
        selected_items = self.active_session.scene.selectedItems()
        if len(selected_items) <= 1:
            return

        # 2. 构造一个只包含已修改属性的字典
        geo_changes = {}
        try:
            # 检查每个输入框，如果用户输入了值，则添加到变更字典中
            if self.txt_x.text():
                geo_changes['x'] = float(self.txt_x.text())
                
            if self.txt_y.text():
                geo_changes['y'] = float(self.txt_y.text())

            if self.txt_width.text():
                w = float(self.txt_width.text())
                if w <= 0:
                    raise ValueError("宽度必须为正数")
                geo_changes['w'] = w

            if self.txt_height.text():
                h = float(self.txt_height.text())
                if h <= 0:
                    raise ValueError("高度必须为正数")
                geo_changes['h'] = h

        except ValueError as e:
            # 3. 验证失败处理
            QMessageBox.warning(self, "输入错误", f"请输入有效的数字。\n错误: {e}")
            self.update_hotspot_info()  # 恢复显示（例如，清空无效输入并显示 <多值>）
            return

        # 4. 如果用户没有输入任何有效值，则不执行任何操作
        if not geo_changes:
            return

        # 5. 创建并执行批量修改命令
        command = BatchItemsGeometryCommand(selected_items, geo_changes)
        self.active_session.undo_stack.push(command)