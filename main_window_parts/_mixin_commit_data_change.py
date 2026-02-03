# FILE: D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_commit_data_change.py

# --- Project-specific Imports ---
from commands import DataChangeCommand
from utils import create_default_data


class CommitDataChangeMixin:
    """
    一个 Mixin 类，包含用于提交热区非几何数据更改的方法。
    """

    def commit_data_change(self):
        """
        将在属性面板中对热区数据属性的修改提交到撤销栈。
        """
        if not self.active_session or not self.active_session.scene.selectedItems():
            return

        selected_items = self.active_session.scene.selectedItems()
        if len(selected_items) != 1:
            return

        item = selected_items[0]

        try:
            pw = int(self.txt_popup_width.text())
            ph = int(self.txt_popup_height.text())
            url_pw = int(self.txt_url_popup_width.text())
            url_ph = int(self.txt_url_popup_height.text())
        except ValueError:
            self.update_hotspot_info()
            return

        old_data = item.data(0) or create_default_data()
        new_data = old_data.copy()

        # --- 构建新数据字典 ---
        new_data["description"] = self.txt_description.toPlainText()
        new_data["hotspot_type"] = "file" if self.type_combo.currentIndex() == 1 else "url"

        selected_icon_text = self.icon_type_combo.currentText()
        if selected_icon_text:
            new_data["icon_type"] = self.icon_type_map[selected_icon_text]

        # URL 数据 (确保深拷贝)
        new_data["url_data"] = old_data.get("url_data", create_default_data()["url_data"]).copy()
        # --- *** 核心修改 1/2: 读取并保存URL宽高比 *** ---
        selected_url_aspect_text = self.url_aspect_ratio_combo.currentText()
        new_data["url_data"].update({
            "url": self.txt_url.text(),
            "target": self.target_map[self.combo_target.currentText()],
            "popup_width": url_pw,
            "popup_height": url_ph,
            "aspect_ratio": self.aspect_ratio_map.get(selected_url_aspect_text, "free")
        })
        # --- *** 修改结束 *** ---

        # 文件数据 (确保深拷贝)
        new_data["file_data"] = old_data.get("file_data", create_default_data()["file_data"]).copy()
        # --- *** 核心修改 2/2: 读取并保存文件宽高比 *** ---
        selected_file_aspect_text = self.file_aspect_ratio_combo.currentText()
        new_data["file_data"].update({
            "display": "embed" if self.combo_file_display.currentIndex() == 1 else "popup",
            "popup_width": pw,
            "popup_height": ph,
            "aspect_ratio": self.aspect_ratio_map.get(selected_file_aspect_text, "free")
        })
        # --- *** 修改结束 *** ---

        if old_data == new_data:
            return

        command = DataChangeCommand(item, old_data, new_data)
        self.active_session.undo_stack.push(command)