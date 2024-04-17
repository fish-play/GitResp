"""
-*- coding: utf-8 -*-
@Time : 2024/2/27 8:36
"""
x = "张三里斯万事达卡就很少看到就还是三个地块边界"
b = x.count("三")
print(b)
import os
file = r"D:\测试文件\保函"
xxx = os.walk(file)
print(xxx)
for v in os.walk(file):
    print( v)