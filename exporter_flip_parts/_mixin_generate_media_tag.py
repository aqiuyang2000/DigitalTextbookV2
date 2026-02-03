# FILE: exporter_flip_parts/_mixin_generate_media_tag.py
#
# 功能: 提供 _generate_media_tag_for_flipbook 方法的实现。

import mimetypes


class GenerateMediaTagMixin:
    """
    一个 Mixin 类，为 ExporterFlip 提供生成媒体HTML标签的功能。
    """

    @classmethod
    def _generate_media_tag_for_flipbook(cls, media_relative_path: str) -> str:
        """
        根据媒体文件的相对路径和MIME类型，为其生成一个合适的HTML标签
        以便在弹窗中预览。

        Args:
            media_relative_path (str): 媒体文件相对于网页的路径。

        Returns:
            str: 生成的HTML标签字符串。
        """
        tag = ""
        mime_type, _ = mimetypes.guess_type(media_relative_path)
        if mime_type:
            if mime_type.startswith("image/"):
                tag = f'<img src="{media_relative_path}" style="max-width:100%; max-height:100%;">'
            elif mime_type.startswith("video/"):
                tag = f'<video src="{media_relative_path}" controls autoplay style="width:100%; height:100%;"></video>'
            elif mime_type.startswith("audio/"):
                tag = f'<audio src="{media_relative_path}" controls autoplay></audio>'
            elif mime_type.startswith("text/"):
                tag = f'<iframe src="{media_relative_path}" style="width:100%; height:98%; border:none;"></iframe>'

        if not tag:
            tag = f'<p style="color:white;">无法预览文件: <a href="{media_relative_path}" style="color:lightblue;">点击下载</a></p>'

        return tag