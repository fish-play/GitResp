# """
# -*- coding: utf-8 -*-
# @Time : 2023/3/3 15:36
# """
# import os
# file = r"C:\Users\9000\Desktop\新建文件夹 (6)"
# x = []
# for i in os.listdir(file):
#     a = i.replace('-', ".").split(".")[1]
#     try:
#        b = a.split("之")[0]
#     except:
#         ...
#
#     x.append(b)
# print(x)
# _ = ["4000", "4001", "4002", "4003"]
# for i in _:
#     if x.count(i)<5:
#         print(i)
#         o = f"案号:{i}"
#         Note = open(r'C:\Users\9000\Desktop\新建文件夹 (6)\x.txt', mode='a+')
#         Note.write(f"{o}\n")
