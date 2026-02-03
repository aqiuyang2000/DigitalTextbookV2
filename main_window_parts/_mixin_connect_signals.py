# FILE: D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_connect_signals.py

from PySide6.QtWidgets import QTextEdit


class ConnectSignalsMixin:
    """
    一个 Mixin 类，包含连接所有UI信号和槽的 connect_signals 方法。
    """

    def connect_signals(self):
        """
        连接UI控件的信号到相应的处理方法（槽）。
        """
        self.page_scrollbar.valueChanged.connect(self.on_scroll)
        self.btn_prev.clicked.connect(self.previous_page)
        self.btn_next.clicked.connect(self.next_page)
        self.txt_page_input.returnPressed.connect(self.go_to_page_from_input)
        self.txt_page_input.textChanged.connect(self.validate_page_input_text)
        self.btn_delete_page.clicked.connect(self.delete_current_page)
        self.btn_export_all.clicked.connect(self.export_all_formats)
        self.btn_update_all_fragments.clicked.connect(self.update_all_fragments)
        self.btn_preview.clicked.connect(self.preview_in_browser)
        self.btn_batch_import.clicked.connect(self.batch_import_hotspots)
        self.btn_export_hotspot_data.clicked.connect(self.export_hotspot_data)
        self.btn_export_current_page_data.clicked.connect(self.export_current_page_data)
        self.btn_pdf_toolbox.clicked.connect(self.open_pdf_toolbox)
        self.btn_batch_scale.clicked.connect(self.open_batch_scale_dialog)
        self.outline_widget.item_clicked.connect(self.go_to_page)
        self.outline_widget.outline_changed.connect(self._on_outline_changed)
        self.pdf_processor.progress_updated.connect(self._update_pdf_conversion_progress)

        # --- 属性面板 ---
        for editor in [self.txt_x, self.txt_y, self.txt_width, self.txt_height]:
            editor.returnPressed.connect(self.on_geometry_field_committed)

        # 数据提交信号
        self.txt_url.editingFinished.connect(self.commit_data_change)
        for combo in [self.combo_target, self.combo_file_display, self.icon_type_combo]:
            combo.currentIndexChanged.connect(self.commit_data_change)

        # --- *** 核心修改: 为 type_combo 添加新的连接 *** ---
        self.type_combo.currentIndexChanged.connect(self._on_hotspot_type_changed)  # 1. 自动匹配图标
        self.type_combo.currentIndexChanged.connect(self.commit_data_change)  # 2. 保存数据
        self.type_combo.currentIndexChanged.connect(self.stacked_widget.setCurrentIndex)  # 3. 切换面板
        # --- *** 修改结束 *** ---

        self.txt_description.focusOutEvent = lambda event: (
            self.commit_data_change(),
            QTextEdit.focusOutEvent(self.txt_description, event)
        )
        self.btn_upload.clicked.connect(self.select_hotspot_file)

        # 弹窗可见性信号
        self.combo_file_display.currentIndexChanged.connect(self.update_popup_size_visibility)
        self.combo_target.currentIndexChanged.connect(self.update_url_popup_size_visibility)

        # 宽高比处理信号
        self.url_aspect_ratio_combo.currentIndexChanged.connect(self._handle_aspect_ratio_change)
        self.file_aspect_ratio_combo.currentIndexChanged.connect(self._handle_aspect_ratio_change)
        self.txt_url_popup_width.editingFinished.connect(self._handle_width_change)
        self.txt_url_popup_height.editingFinished.connect(self._handle_height_change)
        self.txt_popup_width.editingFinished.connect(self._handle_width_change)
        self.txt_popup_height.editingFinished.connect(self._handle_height_change)