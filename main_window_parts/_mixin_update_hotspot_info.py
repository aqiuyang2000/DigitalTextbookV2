# FILE: D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_update_hotspot_info.py

import os

# --- Qt Imports ---
from PySide6.QtWidgets import QWidget

# --- Project-specific Imports ---
from graphics_items import AbstractResizableItem
from utils import create_default_data


class UpdateHotspotInfoMixin:
    """
    一个 Mixin 类，包含根据场景选择状态更新属性面板的 update_hotspot_info 方法。
    """

    def update_hotspot_info(self):
        """
        当场景中的选中项改变时，更新右侧属性面板的显示内容。
        """
        if not self.active_session:
            self.set_properties_enabled(False)
            self.btn_batch_scale.setEnabled(False)
            for editor in [self.txt_id, self.txt_description, self.txt_x, self.txt_y, self.txt_width, self.txt_height,
                           self.txt_url]:
                editor.clear()
            self.icon_type_combo.setCurrentIndex(0)
            self.url_aspect_ratio_combo.setCurrentIndex(0)  # 新增
            self.file_aspect_ratio_combo.setCurrentIndex(0)  # 新增
            self.lbl_filename.setText("<i>未选择文件</i>")
            return

        selected_items = self.active_session.scene.selectedItems()

        # --- 情况 1: 选中单个热区 ---
        if len(selected_items) == 1 and isinstance(selected_items[0], AbstractResizableItem):
            self.set_properties_enabled(True)
            self.btn_batch_scale.setEnabled(False)
            item = selected_items[0]
            data = item.data(0) or create_default_data()

            [w.blockSignals(True) for w in self.central_widget.findChildren(QWidget)]

            # ID, 几何属性等...
            hotspot_id = data.get("id")
            if not hotspot_id and self.project_id:
                hotspot_id = self.generate_new_hotspot_id(self.active_session)
                data['id'] = hotspot_id
                item.setData(0, data)
            self.txt_id.setText(hotspot_id or "N/A")
            scene_pos = item.pos();
            rect = item.rect()
            self.txt_description.setText(data.get("description", ""))
            self.txt_x.setText(f"{scene_pos.x():.1f}")
            self.txt_y.setText(f"{scene_pos.y():.1f}")
            self.txt_width.setText(f"{rect.width():.1f}")
            self.txt_height.setText(f"{rect.height():.1f}")

            # 数据属性
            htype = data.get("hotspot_type", "url")
            self.type_combo.setCurrentIndex(1 if htype == "file" else 0)
            self.stacked_widget.setCurrentIndex(1 if htype == "file" else 0)
            icon_type = data.get("icon_type", "default")
            self.icon_type_combo.setCurrentText(self.icon_type_map_reverse.get(icon_type, "默认图标"))

            # URL 数据
            udata = data.get("url_data", create_default_data()["url_data"])
            self.txt_url.setText(udata.get("url", "#"))
            self.combo_target.setCurrentText(self.target_map_reverse.get(udata.get("target"), "在新标签页中打开"))
            self.txt_url_popup_width.setText(str(udata.get("popup_width", 800)))
            self.txt_url_popup_height.setText(str(udata.get("popup_height", 600)))
            # --- *** 核心修改 1/2: 更新URL宽高比下拉框 *** ---
            url_aspect = udata.get("aspect_ratio", "free")
            self.url_aspect_ratio_combo.setCurrentText(self.aspect_ratio_map_reverse.get(url_aspect, "自由调整"))

            # 文件数据
            fdata = data.get("file_data", create_default_data()["file_data"])
            source_path = fdata.get("source_path", "")
            self.lbl_filename.setText(f"<i>{os.path.basename(source_path)}</i>" if source_path else "<i>未选择文件</i>")
            self.combo_file_display.setCurrentIndex(1 if fdata.get("display") == "embed" else 0)
            self.txt_popup_width.setText(str(fdata.get("popup_width", 800)))
            self.txt_popup_height.setText(str(fdata.get("popup_height", 600)))
            # --- *** 核心修改 2/2: 更新文件宽高比下拉框 *** ---
            file_aspect = fdata.get("aspect_ratio", "free")
            self.file_aspect_ratio_combo.setCurrentText(self.aspect_ratio_map_reverse.get(file_aspect, "自由调整"))

            self.update_popup_size_visibility()
            self.update_url_popup_size_visibility()

            [w.blockSignals(False) for w in self.central_widget.findChildren(QWidget)]

        # --- 情况 2: 选中多个热区 ---
        elif len(selected_items) > 1:
            self.set_properties_enabled(True)
            self.btn_batch_scale.setEnabled(True)

            self.txt_id.setText("");
            self.txt_description.setText("")
            self.txt_id.setEnabled(False);
            self.txt_description.setEnabled(False)
            self.type_combo.setEnabled(False);
            self.stacked_widget.setEnabled(False)

            # 多选时禁用宽高比设置，以简化逻辑
            self.url_aspect_ratio_combo.setEnabled(False)
            self.file_aspect_ratio_combo.setEnabled(False)

            all_icons = {item.data(0).get("icon_type", "default") for item in selected_items if item.data(0)}
            if len(all_icons) == 1:
                self.icon_type_combo.setCurrentText(self.icon_type_map_reverse.get(all_icons.pop(), "默认图标"))
            else:
                self.icon_type_combo.setCurrentIndex(-1)

            all_x = {round(item.pos().x(), 1) for item in selected_items};
            all_y = {round(item.pos().y(), 1) for item in selected_items}
            all_w = {round(item.rect().width(), 1) for item in selected_items};
            all_h = {round(item.rect().height(), 1) for item in selected_items}
            self.txt_x.setText(str(all_x.pop()) if len(all_x) == 1 else "");
            self.txt_x.setPlaceholderText("<多值>" if len(all_x) > 1 else "X")
            self.txt_y.setText(str(all_y.pop()) if len(all_y) == 1 else "");
            self.txt_y.setPlaceholderText("<多值>" if len(all_y) > 1 else "Y")
            self.txt_width.setText(str(all_w.pop()) if len(all_w) == 1 else "");
            self.txt_width.setPlaceholderText("<多值>" if len(all_w) > 1 else "宽")
            self.txt_height.setText(str(all_h.pop()) if len(all_h) == 1 else "");
            self.txt_height.setPlaceholderText("<多值>" if len(all_h) > 1 else "高")

        # --- 情况 3: 没有选中项 ---
        else:
            self.set_properties_enabled(False)
            self.btn_batch_scale.setEnabled(False)
            for editor in [self.txt_id, self.txt_description, self.txt_x, self.txt_y, self.txt_width, self.txt_height,
                           self.txt_url]:
                editor.clear()
            self.icon_type_combo.setCurrentIndex(0)
            self.url_aspect_ratio_combo.setCurrentIndex(0)
            self.file_aspect_ratio_combo.setCurrentIndex(0)
            self.lbl_filename.setText("<i>未选择文件</i>")