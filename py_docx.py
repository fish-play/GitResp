"""
-*- coding: utf-8 -*-
@Time : 2023/3/9 9:15
"""
import docx
import os
import shutil
from docx import Document
py_dir = r"C:\Users\9000\Desktop\123\py"
txt_dir = r"C:\Users\9000\Desktop\123\txt"
docx_dir = r"C:\Users\9000\Desktop\123\docx"
py_lists = [i for i in os.listdir(py_dir) if ".py" in i]
for i in py_lists:
    shutil.copyfile(os.path.join(py_dir, i), os.path.join(txt_dir, i.replace('.py', '.txt')))
for i in os.listdir(txt_dir):
    with open(os.path.join(txt_dir, i), "r", encoding="utf-8") as f:
        reads = f.read()
    reads = reads.split("if __name__ == '__main__':")[0]
    document = Document()
    document.add_paragraph(reads)
    document.save(os.path.join(docx_dir, i.replace('.txt', '.docx')))
