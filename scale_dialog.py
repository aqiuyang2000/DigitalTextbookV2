# FILE: scale_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QGroupBox, QRadioButton, QFormLayout,
    QLabel, QDoubleSpinBox, QDialogButtonBox
)
from PySide6.QtCore import Qt


class ScaleDialog(QDialog):
    """
    一个用于获取批量缩放选项的对话框。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("批量缩放")
        self.setMinimumWidth(300)

        # --- UI 控件 ---
        # 缩放模式组
        mode_group = QGroupBox("缩放方式")
        mode_layout = QVBoxLayout(mode_group)
        self.radio_overall = QRadioButton("整体缩放 (保持宽高比)")
        self.radio_horizontal = QRadioButton("仅横向缩放")
        self.radio_vertical = QRadioButton("仅纵向缩放")
        mode_layout.addWidget(self.radio_overall)
        mode_layout.addWidget(self.radio_horizontal)
        mode_layout.addWidget(self.radio_vertical)
        self.radio_overall.setChecked(True)  # 默认选中

        # 缩放系数输入
        form_layout = QFormLayout()
        self.scale_spinbox = QDoubleSpinBox()
        self.scale_spinbox.setRange(0.1, 10.0)  # 允许缩小到10%，放大到10倍
        self.scale_spinbox.setSingleStep(0.1)
        self.scale_spinbox.setValue(1.0)
        self.scale_spinbox.setDecimals(2)
        form_layout.addRow(QLabel("缩放系数:"), self.scale_spinbox)

        # OK 和 Cancel 按钮
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # --- 布局 ---
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(mode_group)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.button_box)

        # --- 信号连接 ---
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_selected_options(self):
        """返回用户选择的模式和缩放系数。"""
        mode = 'overall'
        if self.radio_horizontal.isChecked():
            mode = 'horizontal'
        elif self.radio_vertical.isChecked():
            mode = 'vertical'

        factor = self.scale_spinbox.value()
        return factor, mode

    @staticmethod
    def get_scale_options(parent=None):
        """
        静态方法，用于创建、显示对话框并返回结果。
        这是与主窗口交互的推荐方式。
        """
        dialog = ScaleDialog(parent)
        result = dialog.exec()
        if result == QDialog.Accepted:
            return dialog.get_selected_options()
        return None, None  # 如果用户点击了Cancel