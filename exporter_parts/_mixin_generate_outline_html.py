# _mixin_generate_outline_html.py

class GenerateOutlineHtmlMixin:
    @classmethod
    def _generate_outline_html(cls, outline_data, page_prefix_url="#page"):
        if not outline_data: return ""
        html = "<ul>";
        for item in outline_data:
            html += f"<li><a href='{page_prefix_url}{item['page']}'>{item['title']}</a>"
            # 关键：使用 cls 调用自身以实现递归
            if item.get('children'): html += cls._generate_outline_html(item['children'], page_prefix_url)
            html += "</li>"
        html += "</ul>";
        return html