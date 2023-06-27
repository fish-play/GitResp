# import os
# from PyPDF2 import PdfFileWriter, PdfFileReader
#
#
# def split_pdf():
#     firename = os.getcwd()
#     chunk_size = 1
#     new_folder_path = f"{firename}\\NewFolder"
#     if not os.path.exists(new_folder_path):
#         os.makedirs(new_folder_path)
#     for _ in os.listdir(firename):
#         if '.pdf' not in _:
#             continue
#         file_name = os.path.join(firename, _)
#         input_pdf = PdfFileReader(open(file_name, "rb"))
#         if input_pdf.numPages <= chunk_size:
#             print("PDF文件页数少于分割大小")
#             return
#         for i in range(0, input_pdf.numPages, chunk_size):
#             output = PdfFileWriter()
#             for j in range(i, i + chunk_size):
#                 if j >= input_pdf.numPages:
#                     break
#                 output.addPage(input_pdf.getPage(j))
#             output_filename = os.path.join(f'{new_folder_path}', f"{_}" + str(i + 1) + "-" + ".pdf")
#             with open(output_filename, "wb") as out:
#                 output.write(out)
#             print("分割完成: ", output_filename)
#
#
# split_pdf()
a = ["1", "2", "3", "4"]
b = ["a", "b", "c", "d"]
c = zip(a, b)
print(dict(c))

import pandas as pd

# 读取数据文件，不指定表头
df = pd.read_excel('data.csv', header=None)

# 判断表头是否存在
if df.iloc[0].isnull().any():
    print('表头不存在')
else:
    print('表头存在')
