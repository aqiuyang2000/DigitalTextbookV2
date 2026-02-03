# FILE: D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_auto_icon_handler.py (NEW FILE)

class AutoIconHandlerMixin:
    """
    一个 Mixin 类，封装了根据热区类型自动匹配图标的逻辑。
    """

    def _on_hotspot_type_changed(self):
        """
        当“类型”下拉框 (type_combo) 的值改变时被调用的槽函数。
        """
        # 检查是否有单个热区被选中
        if not self.active_session or len(self.active_session.scene.selectedItems()) != 1:
            return

        current_type = self.type_combo.currentText()

        # 如果新选择的类型是“链接(URL)”
        if current_type == "链接 (URL)":
            # 获取当前图标下拉框的值
            current_icon_text = self.icon_type_combo.currentText()
            target_icon_text = "链接符号"

            # 只有当当前图标不是“链接符号”时，才进行程序化修改
            # 这可以防止不必要的重复信号触发和数据提交
            if current_icon_text != target_icon_text:
                print("热区类型变更为URL，自动设置图标为'链接符号'。")
                self.icon_type_combo.setCurrentText(target_icon_text)

        # 当类型从“链接”切换回“本地文件”时，我们暂时不自动改变图标，
        # 因为用户可能已经为这个热区设置了一个特定的文件图标（如视频、音频），
        # 我们应该保留用户的选择。自动匹配只在上传新文件时触发。