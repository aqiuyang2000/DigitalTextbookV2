# D:\projects\singlepage\hotspot_editor\test_toc_extractor.py
import os
import json
import sys
from unittest import TestCase, main as unittest_main

# --- 核心：确保脚本能找到 tools 目录下的模块 ---
# 将项目根目录添加到Python的模块搜索路径中
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 现在可以安全地导入我们想要测试的工具了
try:
    from tools.tool_extract_toc import ExtractTocTool
except ImportError as e:
    print(
        f"导入错误: 无法找到 'tools.tool_extract_toc'。请确保文件路径正确，并且 tools 文件夹下有 __init__.py 文件。\n{e}")
    sys.exit(1)

# --- 测试配置 ---
TEST_SUITE_DIR = os.path.join(project_root, 'toc_test_suite')


class TestTocExtractor(TestCase):

    def run_test_on_file(self, txt_filepath):
        """
        对单个txt文件执行完整的测试流程。
        """
        # 构造期望结果文件的路径
        expected_json_path = txt_filepath.replace('.txt', '.expected.json')

        # 1. 检查期望结果文件是否存在
        self.assertTrue(os.path.exists(expected_json_path),
                        f"测试失败: 找不到期望结果文件 -> {expected_json_path}")

        # 2. 读取测试文件和期望结果
        with open(txt_filepath, 'r', encoding='utf-8') as f:
            test_content_lines = f.read().splitlines()

        with open(expected_json_path, 'r', encoding='utf-8') as f:
            expected_toc = json.load(f)

        # 3. 创建工具实例并执行提取逻辑
        # 我们需要一个模拟的父对象，但在这里传入 None 即可，因为它不影响算法
        tool_instance = ExtractTocTool(parent=None)

        # --- 调用您想要测试的策略 ---
        # 首先尝试关键词策略
        actual_toc = tool_instance._strategy_keywords(test_content_lines)
        # 如果关键词策略失败，则尝试布局策略
        if not actual_toc:
            actual_toc = tool_instance._strategy_layout(test_content_lines)

        # 4. 比较结果
        # assertEqual 会自动为我们提供详细的差异报告
        self.assertEqual(expected_toc, actual_toc,
                         f"文件 '{os.path.basename(txt_filepath)}' 的目录提取结果与期望不符。")

    def test_all_toc_files(self):
        """
        自动发现并运行 toc_test_suite 文件夹下的所有测试用例。
        """
        self.assertTrue(os.path.isdir(TEST_SUITE_DIR),
                        f"测试套件目录不存在: {TEST_SUITE_DIR}")

        found_tests = False
        # 遍历测试套件目录
        for root, _, files in os.walk(TEST_SUITE_DIR):
            for filename in files:
                if filename.endswith('.txt'):
                    found_tests = True
                    txt_filepath = os.path.join(root, filename)

                    # 使用 subtest，这样即使一个文件失败，测试也不会停止
                    with self.subTest(msg=f"Testing file: {filename}"):
                        print(f"\n--- Running test for: {filename} ---")
                        self.run_test_on_file(txt_filepath)

        if not found_tests:
            self.fail("在测试套件目录中没有找到任何 .txt 测试文件。")


# --- 运行测试 ---
if __name__ == '__main__':
    print("=" * 60)
    print("开始执行目录提取器自动化测试...")
    print("=" * 60)
    unittest_main(verbosity=2)