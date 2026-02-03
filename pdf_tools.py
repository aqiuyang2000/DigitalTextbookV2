# D:\projects\singlepage\hotspot_editor\pdf_tools.py (新版本 - 工具加载器)
import os
import importlib
import inspect
from tools.base_tool import AbstractPdfTool


def load_tools():
    """
    动态扫描 'tools' 文件夹，加载所有工具模块，并返回一个工具类的列表。
    """
    tools = []
    tools_dir = os.path.join(os.path.dirname(__file__), 'tools')

    # 遍历 'tools' 文件夹中的所有 .py 文件
    for filename in os.listdir(tools_dir):
        if filename.endswith('.py') and not filename.startswith('__') and filename != 'base_tool.py':
            module_name = f"tools.{filename[:-3]}"
            try:
                # 动态导入模块
                module = importlib.import_module(module_name)

                # 在模块中查找 AbstractPdfTool 的子类
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, AbstractPdfTool) and obj is not AbstractPdfTool:
                        tools.append(obj)
                        print(f"成功加载工具: {obj.name}")
            except Exception as e:
                print(f"错误：加载工具模块 '{module_name}' 失败: {e}")

    return tools