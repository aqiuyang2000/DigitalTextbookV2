# FILE: exporter_flip_parts/_mixin_generate_outline.py
#
# 功能: 提供 _generate_recursive_outline_for_flipbook 方法的实现。

class GenerateOutlineMixin:
    """
    一个 Mixin 类，为 ExporterFlip 提供递归生成HTML提纲的功能。
    """

    @classmethod
    def _generate_recursive_outline_for_flipbook(cls, outline_data: list) -> str:
        """
        根据嵌套的提纲数据列表，递归地生成一个HTML的无序列表 (<ul>)。

        Args:
            outline_data (list): 包含提纲项的列表。每个项是一个字典，
                                 可能包含 'children' 键来表示子项。

        Returns:
            str: 生成的HTML字符串。
        """
        if not outline_data:
            return ""

        html_parts = ["<ul>"]
        for item in outline_data:
            html_parts.append(f"<li><a href='#' data-page='{item['page']}'>{item['title']}</a>")
            # 关键点：通过 cls 调用自身以实现递归
            if item.get('children'):
                html_parts.append(cls._generate_recursive_outline_for_flipbook(item['children']))
            html_parts.append("</li>")

        html_parts.append("</ul>")
        return "".join(html_parts)