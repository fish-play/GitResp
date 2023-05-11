"""
-*- coding: utf-8 -*-

@Author : zp
@Time : 2022/7/13 15:39
@File : lesson1.py
"""
import subprocess
import time
# import win32gui
from log import logger

# import uiautomation as auto
# import uiautomation

# def GetFirstChild(control):
#     return control.GetFirstChildControl()
#
#
# def GetNextSibling(control):
#     return control.GetNextSiblingControl()

# '''
# 利用win32查找句柄部分
# '''
# desktop = auto.GetRootControl()
# for control, depth in auto.WalkTree(desktop, getFirstChild=GetFirstChild, getNextSibling=GetNextSibling,
#                                     includeTop=True, maxDepth=4):
#     print(control)
'''
控制软件部分
'''
# win =  uiautomation.PaneControl(Name="步步高USB办公电话(RecorderPhone)")
#
# win.SetTopmost(True)
# #
# time.sleep(3)
# win.EditControl(AutomationId='1235').SendKeys('017633602179')
# time.sleep(2)
#
# win.ButtonControl(Name='拨号').Click()
# win.EditControl(AutomationId='1235').SendKeys('{Ctrl}(A)')
# win.EditControl(AutomationId='1235').SendKeys('{Ctrl}(X)')


# win.PaneControl(Name='步步高USB办公电话').Click()


# jz = win.TextControl(Name='美食').GetParentControl().GetParentControl()
# win.TextControl(Name='导入导出').Click()
# win.ImageControl(AutomationId='1243').Click()

# time.sleep(3)
# win.TextControl(Name='奶茶果汁').Click()

#
# win.TextControl(Name='美食').Click()
#
# jz = win.TextControl(Name='美食').GetParentControl().GetParentControl()
# print(jz)
# for control, depth in auto.WalkTree(jz, getFirstChild=GetFirstChild, getNextSibling=GetNextSibling,
#                                     includeTop=True):
#     print(control)
# win.TextControl(Name="饺子馄饨").Click()
# for control, depth in auto.WalkTree(win, getFirstChild=GetFirstChild, getNextSibling=GetNextSibling,
#                                     includeTop=True):
#     print(control)
# win1 = uiautomation.PaneControl(Name="美食")
# for control, depth in auto.WalkTree(win1, getFirstChild=GetFirstChild, getNextSibling=GetNextSibling,
#                                     includeTop=True, maxDepth=1):
#     print(control)


# def x(i):
#     print(i["one"], i["tow"], i[None])
#
#
#
# if __name__ == '__main__':
#     i = {"one":"232", "tow":"tawtw", None:"sdaas"}
#     x(i)


n = int(input())
print('1 ')
if n > 1:
    print("1 1 ")
    add = 0
    i = 3
    lst = [1, 1]
    while (i < n + 1):
        lst1 = lst[:]
        lst = [1, 1]
        for j in range(1, i - 1):
            add = lst1[j - 1] + lst1[j]
            lst.insert(-1, add)
        i += 1
        for k in lst:
            print(k, end=' ')
        print()
