# D:\projects\singlepage\hotspot_editor\main.py (最终版 - 保持原有运行方式)

import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from main_window import HotspotEditor
import nltk


def setup_nltk():
    """
    检查并下载NLTK句子分割模型。
    """
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("首次运行: NLTK 'punkt' 模型未找到，正在自动下载...")
        msg_box = QMessageBox()
        msg_box.setWindowTitle("首次运行设置")
        msg_box.setText("正在下载自然语言处理所需的模型文件 (punkt)，\n这只需要一次。请稍候...")
        msg_box.setStandardButtons(QMessageBox.NoButton)
        msg_box.show()
        QApplication.processEvents()

        nltk.download('punkt', quiet=True)

        msg_box.close()
        print("模型下载完成。")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        setup_nltk()
    except Exception as e:
        QMessageBox.warning(None, "NLTK 模型下载失败",
                            f"无法自动下载 'punkt' 模型，句子识别功能可能无法使用。\n"
                            f"请检查您的网络连接。\n错误: {e}")

    editor = HotspotEditor()
    editor.show()
    sys.exit(app.exec())