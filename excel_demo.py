"""
-*- coding: utf-8 -*-
@Time : 2023/2/16 9:21
"""
import pandas as pd
from openpyxl import Workbook


lists = []
excel_path = r"C:\Users\9000\Desktop\测试.xlsx"
df = pd.read_excel(excel_path)
g = df.drop_duplicates(subset="案号全")
for name in g.index:
    data = df.loc[name].to_dict()
    lists.append(data)
# print(lists)

for i in lists:
    bg_name = i.get("被告姓名").split('，')
    # a = [e for e in bg_name if "宁波银行" not in e]
    a = [e for e in bg_name if (e := e) not in "宁波银行"]
    print(a)
