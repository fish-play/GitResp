"""
-*- coding: utf-8 -*-
@Time : 2023/3/31 17:07
"""

import os
import fitz
seg_num = 1
pdf_path = rf"C:\Users\9000\Desktop\新建文件夹 (6)\动手学OCR.pdf"
output_dir = rf'C:\Users\9000\Desktop\新建文件夹 (11)'
pdf_doc = fitz.open(pdf_path)
num_page = pdf_doc.page_count
pages = [i for i in range(0, num_page, seg_num)]
print(pages)
for i, pages_start in enumerate(pages):
    pages_end = pages_start + seg_num - 1
    dist_pdf = fitz.open()
    dist_pdf.insert_pdf(pdf_doc, from_page=pages_start, to_page=pages_end)
    pdf_name = os.path.basename(pdf_path)
    savepdf = os.path.join(output_dir, f'{i}.pdf')
    dist_pdf.save(savepdf)
