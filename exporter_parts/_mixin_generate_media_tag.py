# _mixin_generate_media_tag.py
import mimetypes

class GenerateMediaTagMixin:
    @classmethod
    def _generate_media_tag(cls, media_relative_path: str) -> str:
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
        if not tag: tag = f'<p style="color:white;">无法预览文件: <a href="{media_relative_path}" style="color:lightblue;">点击下载</a></p>'
        return tag