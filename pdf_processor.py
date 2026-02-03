# FILE: pdf_processor.py (已优化)
import os
import shutil
import fitz  # PyMuPDF
from typing import List, Optional, Tuple
from PySide6.QtCore import QObject, Signal


class PdfProcessor(QObject):
    progress_updated = Signal(int, int)

    def __init__(self, base_temp_dir: str = None):
        super().__init__()
        self.base_temp_dir = base_temp_dir

    # --- *** 核心修改 1/2: 更新 process 方法的签名 *** ---
    def process(self, pdf_path: str, target_asset_dir: str, resolution_dpi: int = 150) -> Optional[
        Tuple[List[str], List[str]]]:
        """
        将指定的PDF文件转换为PNG和单页PDF，并保存到指定的资产目录中。

        :param pdf_path: 输入的PDF文件路径。
        :param target_asset_dir: 保存处理后素材的目标目录。
        :param resolution_dpi: 用于生成PNG图片的分辨率 (DPI)。
        :return: 一个元组，包含(PNG图片绝对路径列表, 单页PDF绝对路径列表)，如果失败则返回 None。
        """
        try:
            image_storage_path = os.path.join(target_asset_dir, "images")
            pdf_storage_path = os.path.join(target_asset_dir, "single_pdfs")

            if os.path.exists(target_asset_dir):
                shutil.rmtree(target_asset_dir)
            os.makedirs(image_storage_path)
            os.makedirs(pdf_storage_path)

            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            png_paths_list = []
            single_pdf_paths_list = []

            for page_num in range(total_pages):
                self.progress_updated.emit(page_num + 1, total_pages)
                page = doc.load_page(page_num)

                # --- *** 核心修改 2/2: 使用传入的DPI计算缩放因子 *** ---
                # 1. 计算缩放因子。PyMuPDF的默认DPI是72。
                #    例如，如果期望150 DPI，缩放因子 zoom = 150 / 72 ≈ 2.08
                zoom = resolution_dpi / 72.0

                # 2. 使用动态计算的缩放因子创建变换矩阵
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                image_filename = f"page-{page_num + 1}.png"
                image_filepath = os.path.join(image_storage_path, image_filename)
                pix.save(image_filepath)
                png_paths_list.append(os.path.abspath(image_filepath))

                # 保存为单页PDF (这部分不受分辨率影响)
                single_pdf_doc = fitz.open()
                single_pdf_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                pdf_filename_out = f"page-{page_num + 1}.pdf"
                pdf_filepath = os.path.join(pdf_storage_path, pdf_filename_out)
                single_pdf_doc.save(pdf_filepath)
                single_pdf_doc.close()
                single_pdf_paths_list.append(os.path.abspath(pdf_filepath))

            doc.close()
            return png_paths_list, single_pdf_paths_list

        except Exception as e:
            print(f"处理 PDF 时出错: {e}")
            import traceback
            traceback.print_exc()
            return None