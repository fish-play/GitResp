"""
-*- coding: utf-8 -*-
@Author : zp
"""
import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
import os


class PDFMerge():
    def __init__(self):
        self.pdf_path = os.getcwd()
        self.save_path = f"{self.pdf_path}\\新建文件夹"
        self.lists = []

    def read_pdf_name(self):

        dict_data = {}
        for name in os.listdir(self.pdf_path):
            if name.endswith('pdf'):
                value = name.split("-")[0]
                if dict_data.get(value,None) is None:
                    dict_data[value] = [name]
                else:
                    dict_data[value].append(name)
        for k, v in dict_data.items():
            # 定义生成文件
            pdfWriter = PdfFileWriter()
            # 开始循环
            for fname in v:
                fname = os.path.join(self.pdf_path, fname)
                content = open(fname, 'rb')
                pdfReader = PyPDF2.PdfFileReader(fname)
                for pageNum in range(1):  # 只要首页
                    firstPage = pdfReader.pages[pageNum]
                    pdfWriter.addPage(firstPage)

            bg_name = v[0].split(".pdf")[0]
            print(bg_name)
            q = 0
            for i in os.listdir(self.save_path):
                if bg_name in i:
                    q += 1
                    bg_name = bg_name + f"-{q}"

            pdf_name = os.path.join(self.save_path, bg_name+'.pdf')
            pdfOutput = open(pdf_name, 'wb')
            pdfWriter.write(pdfOutput)
            pdfOutput.close()

    def run(self):
        new_folder_path = self.save_path
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        self.read_pdf_name()


PDFMerge().run()
