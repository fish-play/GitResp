"""
-*- coding: utf-8 -*-

@Author : zp
@Time : 2022/7/13 15:39
@File : lesson1.py
"""

import uiautomation as auto

def GetFirstChild(control):
    return control.GetFirstChildControl()


def GetNextSibling(control):
    return control.GetNextSiblingControl()

desktop = auto.GetRootControl()
for control, depth in auto.WalkTree(desktop, getFirstChild=GetFirstChild, getNextSibling=GetNextSibling,
                                    includeTop=True, maxDepth=4):
    print(control)

# win =  uiautomation.PaneControl(Name="步步高USB办公电话")
#
# win.SetTopmost(True)
#
# win.TextControl(Name='通话记录').Click()

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