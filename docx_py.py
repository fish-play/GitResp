"""
-*- coding: utf-8 -*-
@Time : 2023/3/9 9:15
"""
import docx
import os
import shutil
from docx import Document

docx_dir_path = r'C:\Users\9000\Desktop\鄞州\docx'
py_dir_path = r'C:\Users\9000\Desktop\鄞州\py'
for i in os.listdir(docx_dir_path):
    docx_file_path = os.path.join(docx_dir_path, i)
    py_file_path = os.path.join(py_dir_path, i.replace(".docx", ".py"))
    document = Document(docx_file_path)
    for paragraph in document.paragraphs:
        with open(py_file_path, 'a+', encoding='utf-8') as f:
            f.write(paragraph.text)