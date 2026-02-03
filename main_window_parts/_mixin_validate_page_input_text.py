# D:\projects\singlepage\hotspot_editor\main_window_parts\_mixin_validate_page_input_text.py
#
# 功能: 提供 validate_page_input_text 方法，用于验证页面跳转输入框的内容。

class ValidatePageInputTextMixin:
    """
    一个 Mixin 类，包含用于实时验证页面输入框文本的槽函数。
    """
    def validate_page_input_text(self, text: str):
        """
        当页面跳转输入框的文本改变时被调用的槽函数。

        它会检查新输入的文本是否为纯数字。如果不是，它会阻止非数字字符
        的输入，并通过状态栏向用户显示一条短暂的提示信息。

        Args:
            text (str): 输入框当前的完整文本。
        """
        # 如果输入框不为空且内容不全是数字
        if text and not text.isdigit():
            # 在状态栏显示提示信息，持续2秒
            self.statusBar().showMessage("请输入有效的页码数字。", 2000)
            
            # 阻止非数字字符的输入：将文本设置回之前有效的状态（即去掉最后一个字符）
            self.txt_page_input.setText(text[:-1])