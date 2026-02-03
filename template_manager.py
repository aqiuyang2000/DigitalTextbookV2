# template_manager.py
# (最终修正版：自动初始化，路径查找更健壮)

import os
import sys
from jinja2 import Environment, FileSystemLoader


class TemplateManager:
    """
    一个单例类，用于管理和渲染 Jinja2 模板。
    它会在第一次被需要时（调用render时）自动初始化。
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TemplateManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # 防止重复初始化
        if hasattr(self, 'initialized') and self.initialized:
            return

        self.env = None
        self.initialized = False
        self._initialize()

    def _get_application_path(self):
        """确定应用程序的根目录，对源码运行和打包程序都有效。"""
        if getattr(sys, 'frozen', False):
            # 如果是打包后的程序 (e.g., PyInstaller)
            return os.path.dirname(sys.executable)
        else:
            # 如果是直接从源代码运行，__main__ 通常是启动脚本
            try:
                # sys.modules['__main__'] 是启动脚本的模块对象
                # 其 __file__ 属性就是启动脚本的路径 (e.g., main.py)
                main_script_path = sys.modules['__main__'].__file__
                return os.path.dirname(os.path.abspath(main_script_path))
            except (KeyError, AttributeError):
                # 如果上述方法失败（在某些特殊环境下），使用备用方法
                return os.path.dirname(os.path.abspath(__file__))

    def _initialize(self, template_dir_name='templates'):
        """
        私有的初始化方法。
        """
        if self.initialized:
            return

        app_root_path = self._get_application_path()
        template_path = os.path.join(app_root_path, template_dir_name)

        print(f"TemplateManager: Attempting to initialize with template directory: {template_path}")

        if not os.path.isdir(template_path):
            error_msg = f"FATAL: Template directory not found at '{template_path}'"
            print(error_msg)
            self.env = None
        else:
            print("TemplateManager: Template directory found. Initializing Jinja2 Environment.")
            self.env = Environment(
                loader=FileSystemLoader(template_path),
                autoescape=True
            )

        self.initialized = True

    def render(self, template_name: str, **context) -> str:
        """
        渲染指定的模板。
        """
        if not self.env:
            error_msg = f"Template engine could not be initialized. Check if the '{os.path.join(self._get_application_path(), 'templates')}' directory exists."
            print(error_msg)
            return f"<h1>Template Engine Error</h1><p>{error_msg}</p>"

        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            print(f"Error rendering template '{template_name}': {e}")
            return f"<h1>Template Rendering Error</h1><p>Template: {template_name}<br>Details: {e}</p>"


# 创建一个全局实例供其他模块使用
template_manager = TemplateManager()