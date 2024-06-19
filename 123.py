# import os
# import time
# from openpyxl import load_workbook
# from win32com.client import DispatchEx
# excel_path = r"C:\Users\9000\Desktop\pdf\蔡州贤-431202199604020439-利随本清.xlsx"
# pdf_path = r"C:\Users\9000\Desktop\pdf\蔡州贤-431202199604020439-利随本清.pdf"             #这里是输出PDF的保存路径
# a = time.time()
# wb = load_workbook(excel_path)
# ws = wb.active
# ws.page_setup.scale = 57
# wb.save(excel_path)
#
# xlApp = DispatchEx("Excel.Application")
# xlApp.Visible = False
# xlApp.DisplayAlerts = 5
# books = xlApp.Workbooks.Open(excel_path, False)
# books.ExportAsFixedFormat(0, pdf_path)
# books.Close(False)
# xlApp.Quit()
# print(time.time() - a)
#
#
