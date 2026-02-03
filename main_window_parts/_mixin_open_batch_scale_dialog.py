# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_open_batch_scale_dialog.py
#
# 功能: 提供 open_batch_scale_dialog 方法，用于打开批量缩放对话框并执行操作。

# --- Qt Imports ---
from PySide6.QtWidgets import QMessageBox

# --- Project-specific Imports ---
from scale_dialog import ScaleDialog
from commands import BatchScaleCommand

class OpenBatchScaleDialogMixin:
    """
    一个 Mixin 类，包含用于打开批量缩放对话框并处理其结果的功能。
    """
    def open_batch_scale_dialog(self):
        """
        “缩放选中项...”按钮的槽函数。

        流程：
        1. 检查当前是否有活动会话以及是否选中了多个热区项。
        2. 使用 `ScaleDialog.get_scale_options` 静态方法来显示对话框并获取
           用户输入的缩放系数 (factor) 和缩放模式 (mode)。
        3. 如果用户确认了对话框（而不是取消），并且缩放系数有效，
           则创建一个 `BatchScaleCommand` 命令。
        4. 将命令推送到当前页面的撤销栈以执行批量缩放。
        """
        # 1. 前置检查
        if not self.active_session:
            return
            
        selected_items = self.active_session.scene.selectedItems()
        if len(selected_items) <= 1:
            QMessageBox.information(self, "提示", "请先选择至少两个热区再使用此功能。")
            return

        # 2. 显示对话框并获取用户输入
        #    ScaleDialog.get_scale_options 是一个静态方法，它封装了
        #    对话框的创建、执行和结果返回，使调用代码非常简洁。
        factor, mode = ScaleDialog.get_scale_options(self)

        # 3. 检查返回结果
        #    如果用户点击 "Cancel"，factor 将为 None。
        #    如果用户没有改变默认的缩放系数 1.0，也不执行任何操作。
        if factor is not None and factor != 1.0:
            # 4. 创建并推送命令
            command = BatchScaleCommand(selected_items, factor, mode)
            self.active_session.undo_stack.push(command)