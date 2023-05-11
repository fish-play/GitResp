"""
-*- coding: utf-8 -*-
@Time : 2023/3/31 17:19
"""
import os
import fitz


pdf_dir = []


def get_file(pdf_file):
    docunames = os.listdir(pdf_file)
    for docuname in docunames:
        if os.path.splitext(docuname)[1] == '.pdf':  # 目录下包含.pdf的文件
            pdf_dir.append(os.path.join(pdf_file,docuname))


def conver_img():
    for pdf in pdf_dir:
        doc = fitz.open(pdf)
        for pg in range(doc.page_count):
            page = doc[pg]
            rotate = int(0)
            # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
            zoom_x = 3.0
            zoom_y = 3.0
            trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
            pm = page.get_pixmap(matrix=trans, alpha=False)
            pm.save(r'C:\Users\9000\Desktop\新建文件夹 (12)\1.jpeg')


if __name__ == '__main__':
    get_file(r'C:\Users\9000\Desktop\新建文件夹 (12)')
    conver_img()