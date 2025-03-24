import os
import shutil
from PyPDF2 import PdfWriter


def create_corrupt_pdf(save_path):
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(b"This is not valid PDF content")
        return True
    except Exception as e:
        return False

def create_pdf_file(save_path):
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        writer = PdfWriter()
        writer.add_blank_page(width=72 * 8.5, height=72 * 11)
        with open(save_path, "wb") as f:
            writer.write(f)
        return True
    except Exception as e:
        return False


def delete_folder(folder_path):
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        return True
    except Exception as e:
        return False
