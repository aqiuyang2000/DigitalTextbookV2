# D:\projects\singlepage\hotspot_editor\pdf_toolbox_dialog.py (新版本 - 支持动态选项)
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QLabel,
    QSplitter, QListWidgetItem, QAbstractItemView,
    QDialogButtonBox, QWidget, QFrame
)
from PySide6.QtCore import Qt

from pdf_tools import load_tools
import os

class PdfToolboxDialog(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setWindowTitle("PDF 工具箱")
        self.setMinimumSize(600, 400)

        # ... (UI 布局代码保持不变) ...
        self.splitter = QSplitter(Qt.Horizontal)
        self.tool_list = QListWidget()
        self.tool_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tool_list.setFixedWidth(200)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        self.name_label = QLabel("请选择一个工具")
        self.name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.description_label = QLabel("...")
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignTop)
        self.tool_options_widget = QWidget()
        self.tool_options_layout = QVBoxLayout(self.tool_options_widget)
        self.tool_options_layout.setContentsMargins(0, 10, 0, 0)
        right_layout.addWidget(self.name_label)
        right_layout.addWidget(self.description_label)
        right_layout.addWidget(QFrame(frameShape=QFrame.HLine, frameShadow=QFrame.Sunken))
        right_layout.addWidget(self.tool_options_widget)
        right_layout.addStretch()
        self.splitter.addWidget(self.tool_list)
        self.splitter.addWidget(right_panel)
        self.splitter.setSizes([200, 400])
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setText("运行工具")
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        self.button_box.button(QDialogButtonBox.Cancel).setText("关闭")
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.splitter)
        main_layout.addWidget(self.button_box)

        self.tool_list.currentItemChanged.connect(self.on_tool_selected)
        self.button_box.accepted.connect(self.run_selected_tool)
        self.button_box.rejected.connect(self.reject)

        self.populate_tools()

    def populate_tools(self):
        # ... (此方法保持不变) ...
        tool_classes = load_tools()
        for tool_class in tool_classes:
            tool_instance = tool_class(parent=self)
            item = QListWidgetItem(tool_instance.name)
            item.setData(Qt.UserRole, tool_instance)
            self.tool_list.addItem(item)

    def on_tool_selected(self, current_item, previous_item):
        while self.tool_options_layout.count():
            child = self.tool_options_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not current_item:
            self.name_label.setText("请选择一个工具")
            self.description_label.setText("...")
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
            return

        tool = current_item.data(Qt.UserRole)
        if tool:
            self.name_label.setText(tool.name)
            self.description_label.setText(tool.description)

            # --- *** 核心修改: 将 main_window 传递给 get_options_widget *** ---
            if hasattr(tool, 'get_options_widget') and callable(tool.get_options_widget):
                # 在调用时，传入 self.main_window
                options_widget = tool.get_options_widget(self.main_window)
                if options_widget:
                    self.tool_options_layout.addWidget(options_widget)

            self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)

    def run_selected_tool(self, current_item=None):
        # ... (此方法保持不变) ...
        # (修正：run_selected_tool 并不需要 current_item 参数，它是从 self.tool_list.currentItem() 获取的)
        current_item = self.tool_list.currentItem()
        if not current_item:
            return
        tool = current_item.data(Qt.UserRole)
        if tool:
            if hasattr(tool, 'set_options') and callable(tool.set_options):
                layout = self.tool_options_widget.layout()
                if layout and layout.count() > 0:
                    item = layout.itemAt(0)
                    if item:
                        options_widget = item.widget()
                        if options_widget and hasattr(options_widget, 'get_values'):
                            tool.set_options(options_widget.get_values())
            tool.run(self.main_window)
            self.accept()