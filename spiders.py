# """
# -*- coding: utf-8 -*-
#
# @Author : zp
# @Time : 2022/8/3 10:17
# @File : spiders.py
# """
# import re
# import time
#
# import requests
# from lxml import etree
#
# url = 'https://www.lawxp.com/court/?pg=0&rid=0&cid=0&q='
# headers = {
#     'Cookie': 'ASP.NET_SessionId=1qdivzan2hbttjko4fd5iotu; Hm_lvt_31b422713d7e15457030105c4f9a6d7a=1659492717; Hm_lpvt_31b422713d7e15457030105c4f9a6d7a=1659493012',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
#     'Referer': 'https://www.lawxp.com/court/?pg=0&rid=0&cid=0&q='
# }
#
# response = requests.get(url=url, headers=headers)
# htm = response.content.decode()
# # print(htm)
# # a = re.search('class="w-zx-sfcs4".*<a .*>(.*)</a>', htm).group(1)
# # a = re.findall('class="w-zx-sfcs4".*\n.*\n.*', htm)
# # for i in a:
# #     print(i)
# # """
# # a[].group().strip('class="w-zx-sfcs4">').replace(
# #     """<a href='/wl/Lawyer2Info/CourtShow.aspx?courtId=2119' class="w-zx-sfcs41">""", '').replace('</a>', '').replace(
# #     '\n', '').replace(' ', '')"""
# p_list = etree.HTML(htm)
# # print(p_list)
# #
# for i in p_list[1]:
#     img_src = i.xpath('//*[@id="w3-body"]/div/div[2]/div[1]/ul[1]/li/div[2]/div/a/text()')
#     date_ss = i.xpath('//*[@id="w3-body"]/div/div[2]/div[1]/ul/li/div[2]/div/p[2]/text()')
#     print(img_src)
#     print(date_ss)
#
#
# import pdfplumber
# '''for i in os.listdir(self.pdf_path):
#     errmsg = []
#     result = []
#     if i.endswith('.pdf'):
#         # logger.info(f'{i}租赁服务信息正在提取')
#         with pdfplumber.open(os.path.join(self.pdf_path, i)) as pdf:
#             texts = ""
#             result.append(i)
#             for page in pdf.pages:
#                 texts += page.extract_text()
#             # print(texts)'''
# import fitz
# '''
# _ = os.listdir(self.pdf_path)
#         for x in _:
#             print("*" * 100)
#             result = []
#             errmsg = []
#             if x.endswith(".pdf"):
#                 logger.info(f"开始执行{x}")
#                 doc = fitz.open(os.path.join(self.pdf_path, x))
#                 content = ""
#                 for i in doc:
#                     content += i.get_text()
#                     # print(content)'''
#
#
#
#
#
#
#
#
#
#
# import os
# from win32com.client import DispatchEx
# from openpyxl import load_workbook
# from flows.flow import ListDataFlow, ScriptDef, DirectoryItem
# from rpalib.log import logger
#
#
# class Format(ListDataFlow):
#     def __init__(self, file_path, save_path):
#         self.file_path = file_path
#         self.save_path = save_path
#
#     def run(self):
#         for excel_name in os.listdir(self.file_path):
#             if '.xlsx' in excel_name:
#                 excel_path = os.path.join(self.file_path, excel_name)
#                 pdf_path = os.path.join(self.save_path, excel_name.replace(".xlsx", ""))
#                 logger.info(f"开始执行-{excel_path}")
#                 wb = load_workbook(excel_path)
#                 ws = wb.active
#                 ws.page_setup.scale = 70   # 设置页面显示大小
#                 wb.save(excel_path)
#
#                 xlApp = DispatchEx("Excel.Application")
#                 xlApp.Visible = False
#                 xlApp.DisplayAlerts = 5     # 页面上下偏移
#                 books = xlApp.Workbooks.Open(excel_path, False)
#                 sheet = books.Worksheets("sheet1")
#                 sheet.PageSetup.Orientation = 2    # 1代表纵向，2代表横向
#                 sheet.PageSetup.CenterHorizontally = True
#                 books.ExportAsFixedFormat(0, pdf_path)
#                 books.Close(False)
#                 xlApp.Quit()
#
#
# export = ScriptDef(
#     cls=Format,
#     group="宁波",
#     title="excel转pdf",
#     description="excel转pdf",
#     arguments=[
#         DirectoryItem(title="excel所在目录", name="file_path"),
#         DirectoryItem(title="pdf生成目录", name="save_path"),
#     ]
# )
#
#
# if __name__ == '__main__':
#     Format(r'C:\Users\9000\Desktop\000', r'C:\Users\9000\Desktop\pdf').run()
#
import traceback


def run():
    # for e in range(5):
    #     print(11111)
    i = 0
    try:
        assert type(i) is str
        print(111)
    except Exception as e:
        print("出错了")
        traceback.print_exc()
    finally:
        print(121212)


run()
