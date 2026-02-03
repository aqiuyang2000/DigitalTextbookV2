# FILE: D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_aspect_ratio_handler.py (NEW FILE)

from PySide6.QtWidgets import QLineEdit, QComboBox


class AspectRatioHandlerMixin:
    """
    一个 Mixin 类，封装了所有处理宽高比锁定和自动计算的逻辑。
    """

    def _get_active_aspect_ratio_widgets(self) -> tuple[QComboBox | None, QLineEdit | None, QLineEdit | None]:
        """辅助方法，根据当前激活的面板返回对应的UI控件。"""
        if self.stacked_widget.currentIndex() == 0:  # URL 面板
            return self.url_aspect_ratio_combo, self.txt_url_popup_width, self.txt_url_popup_height
        elif self.stacked_widget.currentIndex() == 1:  # 文件面板
            return self.file_aspect_ratio_combo, self.txt_popup_width, self.txt_popup_height
        return None, None, None

    def _handle_aspect_ratio_change(self):
        """当宽高比下拉框的值改变时调用。"""
        # 当切换到“自由调整”时，不执行任何计算
        self._calculate_size(source='aspect_ratio')

    def _handle_width_change(self):
        """当宽度输入框的值改变时调用。"""
        self._calculate_size(source='width')
        # 宽度变化后，手动触发一次数据提交
        self.commit_data_change()

    def _handle_height_change(self):
        """当高度输入框的值改变时调用。"""
        self._calculate_size(source='height')
        # 高度变化后，手动触发一次数据提交
        self.commit_data_change()

    def _calculate_size(self, source: str):
        """
        核心计算逻辑。

        Args:
            source (str): 触发计算的来源 ('width', 'height', or 'aspect_ratio')
        """
        combo, width_edit, height_edit = self._get_active_aspect_ratio_widgets()
        if not combo or not width_edit or not height_edit:
            return

        aspect_ratio_key = combo.currentText()
        aspect_ratio_str = self.aspect_ratio_map.get(aspect_ratio_key)

        if not aspect_ratio_str or aspect_ratio_str == 'free':
            return  # 如果是自由调整，则不进行任何计算

        try:
            ratio_w, ratio_h = map(int, aspect_ratio_str.split(':'))

            # 临时断开信号连接，防止无限循环
            width_edit.editingFinished.disconnect(self._handle_width_change)
            height_edit.editingFinished.disconnect(self._handle_height_change)

            if source == 'width' or source == 'aspect_ratio':
                # 以宽度为基准计算高度
                current_width = int(width_edit.text())
                new_height = int(current_width * ratio_h / ratio_w)
                height_edit.setText(str(new_height))
            elif source == 'height':
                # 以高度为基准计算宽度
                current_height = int(height_edit.text())
                new_width = int(current_height * ratio_w / ratio_h)
                width_edit.setText(str(new_width))

        except (ValueError, ZeroDivisionError):
            # 如果输入无效或比例错误，则不执行任何操作
            pass
        finally:
            # 重新连接信号
            width_edit.editingFinished.connect(self._handle_width_change)
            height_edit.editingFinished.connect(self._handle_height_change)