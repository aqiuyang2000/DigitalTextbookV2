# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_go_to_page_from_input.py
#
# 功能: 提供 go_to_page_from_input 方法，用于处理从文本框输入的页码跳转。

class GoToPageFromInputMixin:
    """
    一个 Mixin 类，包含 go_to_page_from_input 槽函数，用于响应页码输入框的回车事件。
    """
    def go_to_page_from_input(self):
        """
        当用户在页码输入框中按下回车键时调用的槽函数。

        它会读取输入框中的文本，尝试将其转换为整数，并验证该页码是否在
        有效范围内。如果一切正常，则调用 `set_active_session` 跳转到该页面。
        如果输入无效或超出范围，则会在状态栏显示错误信息，并将输入框的
        内容恢复为当前页码。
        """
        if not self.sessions:
            return

        text = self.txt_page_input.text()
        
        try:
            # 尝试将输入框的文本转换为整数
            page_num = int(text)
            
            # 检查页码是否在有效范围内 (1 到总页数)
            if 1 <= page_num <= len(self.sessions):
                # 如果有效，则转换为 0-based 索引并跳转
                self.set_active_session(page_num - 1)
            else:
                # 如果超出范围，显示错误信息并恢复输入框文本
                self.statusBar().showMessage(f"页码超出范围，请输入 1 到 {len(self.sessions)} 之间的数字。", 3000)
                self.txt_page_input.setText(str(self.active_session_index + 1))
                
        except ValueError:
            # 如果文本无法转换为整数 (例如，是空字符串或非数字字符)，
            # 显示错误信息并恢复输入框文本。
            self.statusBar().showMessage("请输入一个有效的页码数字。", 3000)
            self.txt_page_input.setText(str(self.active_session_index + 1))

        # 不论成功与否，都清除输入框的焦点，这是一个好的UI实践
        self.txt_page_input.clearFocus()