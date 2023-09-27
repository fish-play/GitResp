# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # import time
# #
# ''' selenium 基础用法'''
# # driver = webdriver.Chrome('chromedriver.exe')
# # driver.maximize_window()
# # driver.get('https://www.baidu.com')
# # driver.find_element(By.XPATH, '//*[@id="kw"]').send_keys('下厨房')
# # driver.find_element(By.XPATH, '//*[@id="su"]').click()
# #
# # time.sleep(6)
# # driver.find_element(By.XPATH, '//*[@id="2"]/div/div[1]/a/span').click()
# #
# # driver.switch_to.window(driver.window_handles[1])
# # time.sleep(3)
# # driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div[1]/form/span/input[2]').send_keys('宫保鸡丁')
# # time.sleep(3)
# # driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div[1]/form/input[2]').click()
# # dc = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[1]/div[1]/div/div[2]/div[1]/ul/li/div/div/p[2]').text
# # for i in dc:
# # # dc.get_attribute("textContent"
# #     print(dc)
#
#
# ''' airtest'''
# # # -*- encoding=utf8 -*-
# # __author__ = "9000"
# #
# # from airtest.core.api import *
# #
# # from selenium import webdriver
# # from selenium.webdriver.common.keys import Keys
# # from airtest_selenium.proxy import WebChrome
# # driver = WebChrome()
# # driver.implicitly_wait(20)
# # driver.maximize_window()
# # driver.get("https://www.hao123.com/")
# # driver.airtest_touch(Template(r'微信图片_20220316162018.png'))
# # auto_setup(__file__)
#
#
# ''' 读取excel表中的内容'''
# # import openpyxl
# # wb = openpyxl.load_workbook(r'C:\Users\9000\Desktop\工作簿.xlsx')
# # sheers = wb.sheetnames    # 拿到所有excel文件头
# # sheets = sheers[0]        # 确定要的excel第几个文件
# # ws = wb[sheets]           # 获取特定对的excel
# # rows = ws.rows            # 获取表格所有的行(可遍历)
# # columns = ws.columns      # 获取表格所有的列(可遍历)
#     # for row in rows:
#     #     line = [col.value for col in row]
#     #     print(line)
#     # print("-"*50)
#     # for colum in columns:
# #     line1 = [col.value for col in colum]
# #     print(line1)
# # print("-"*50)
# # print(ws['A1'].value, ws['B1'].value, ws['C1'].value)           # 通过定位打印特定的位置字段
#
#
# ''' 写excel文件'''
# # from openpyxl import Workbook
# # from openpyxl.utils import get_column_letter
# #
# # wb = Workbook()
# # ws = wb.active
# # ws.cell(row=1, column=1).value = '张三'   # 通过行和列的绝对位置添加字段
# # ws['B1'].value = '李四'                   # 通过列的相对位置添加字段
# # for row in range(2, 11):                 # 循环插入字段
# #     for col in range(1, 11):
# #         ws.cell(row=row, column=col).value = get_column_letter(col)
# #
# # wb.save(r'C:\Users\9000\Desktop\工作簿1.xlsx')
# # print('ok')
# #
# # class Demo:
# #     def __init__(self, name, age, sex, hobby):
# #         self.name = name
# #         self.age = age
# #         self.sex = sex
# #         self.hobby = hobby
# #
# #     def cls(self):
# #         return self.name
# #
# #     def logs(self):
# #         self.name = 'kine' + self.name
# #         print(self.age, self.name, self.hobby, self.sex)
# #
# #
# # s = Demo(name='张三', age=19, sex='男', hobby='篮球')
# # s.logs()
# #
# #
# # def a():
# #     a = 88888888
# #     return a
# # def n():
# #     x = a() + 11111111
# #     return x
# # c = n()
# # print(n())
# # import os
# # cmd = 'date'
# # os.system(cmd)
#
#
# #
# #
# # import os
# #
# # from pdf2img import pdf2img
# # class cs(object):
# #     def __init__(self, main_path):
# #         self.main_path = main_path
# #
# #     ''' 调用pdf2img生成jpg文件 '''
# #     def cc(self):
# #         pdf2img(self.main_path).run()
# #
# #     ''' 删除所有后缀为jpg的文件 '''
# #     def delec(self):
# #         for i in os.listdir(self.main_path):
# #             if i.find("jpg") != -1:
# #                 os.remove(os.path.join(self.main_path, i))
# #
# #
# # if __name__ == '__main__':
# #     cs(r'C:\Users\9000\Desktop\pdf').cc()
# # pdf2img(r"C:\Users\9000\Desktop\pdf").run()
# # a = [0, 1, 2, 3, 4, 5]
# # for i in enumerate(a):
# #     print(i)
# #
# #
# # !python3
# # 自动打印.py - 自动打印，使用PDF
# # -*- coding: utf-8 -*-
# import os, time
# import win32api
# import win32print
#
# # 重要提示：因为我的PDF默认使用Adobe Acrobat DC打开，但这里有一个问题是必须关闭Acrobat.exe才能知道默认打印机的更改，故每次打印前为保险起见需要关闭所有Acrobat.exe
# try:
#     os.system("taskkill /F /IM Acrobat.exe")
# except:
#     pass  # 如没有找到Acrobat.exe进程，则跳过
#
# # 获取所有打印机信息
# printers = win32print.EnumPrinters(3)
#
# # 获取默认打印机
# default_printers = win32print.GetDefaultPrinter()
# print(default_printers)
# # 指定另一个打印机名作为默认打印机
# win32print.SetDefaultPrinter('HP Color MFP E87640-50-60 PCL-6 (V4) (网络)')  # 这里可以换成其他打印机名称
# default_printers = win32print.GetDefaultPrinter()
# print(default_printers)
#
# # 设置权限作为获得句柄语句的参数，有时也可不用
# printaccess = {"DesiredAccess": win32print.PRINTER_ACCESS_USE}  # 较低的权限
# print_DEFAULTS = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}  # 较高的权限
# # 获取指定打印机句柄
# pHandle = win32print.OpenPrinter(default_printers, print_DEFAULTS)  # 这里使用默认打印机，第2个权限参数是可选选项，但如果不设置足够高的权限可能无法成功更改打印参数设置
# # 根据指定打印机句柄获取指定打印机信息
# properties = win32print.GetPrinter(pHandle, 2)  # 传入1返回1个元祖，传入2返回1个字典
# # 获取打印机打印参数设置——pDevMode类
# devmode = properties['pDevMode']
#
# ##查看devmode各类属性
# for n in dir(devmode):
#     print(n, getattr(devmode, n))
#
#
# # 设置打印函数
# def printFile(filename, Copies, FormName='A4', PaperSize=9, Orientation=1, Duplex=2, Color=1):
#     # 设置各类参数
#     devmode.Copies = Copies  # 打印份数设置
#     devmode.FormName = FormName  # 纸张尺寸设置：默认A4
#     devmode.PaperSize = PaperSize  # 只设置FormName不能更改纸张尺寸，设定PaperSize可以。另外指定PaperSize大小（A3为8，A4为9，A5为11，B4为12，B5为13等等）后，则PaperLength和PaperWidth不生效，
#     devmode.Orientation = Orientation  # 方向设置：1为纵向，2为横向。这里默认为1.
#     devmode.Duplex = Duplex  # 双面打印设置：1代表单面；2代表是，翻转；3代表是，向上翻。默认为2。
#     devmode.Color = Color  # 灰度打印设置：1代表仅限黑白，2代表关（即彩色）
#     # 可以对一些一般不更改的打印参数进行默认设置
#     devmode.MediaType = 291  # 纸张类型设置：292是未指定，291是普通纸，290是HP EcoFFICIENT，以此往下类推。这里默认291——普通纸
#     devmode.DefaultSource = 264  # 纸张来源设置：这里默认为1——打印机自动选择
#
#     # 保存更改后的设置
#     properties['pDevMode'] = devmode
#     win32print.SetPrinter(pHandle, 2, properties, 0)
#
#     # 使用ShellExecute打印
#     win32api.ShellExecute(
#         0,
#         "print",
#         filename,
#         None,  # 设置为None即可，也可用下面一行的语句
#         # '/d:"%s"' % win32print.GetDefaultPrinter(),
#         ".",
#         0
#     )
#     time.sleep(10)
#
#
# files = os.listdir('C:\\test')
#
# for file in files:
#     if '横向打印测试' in file:
#         printFile(filename=filepath, Copies=1, Orientation=2, Duplex=3)  # 各种不同打印参数设置下传入不同参数
#     elif '纵向打印测试' in file:
#         printFile(filename=filepath, Copies=1, Duplex=2)  #
#
# # 恢复自己用的默认打印机
# try:
#     os.system("taskkill /F /IM Acrobat.exe")
# except:
#     pass
# win32print.SetDefaultPrinter('SHARP DX-2508NC')
# # 退出窗口
# exit()
#
#
dic = [{"金额": 300, "姓名": "张三", "账户": "321313213213"}, {"金额": 600, "姓名": "李四", "账户": "321313213213"},
       {"金额": 800, "姓名": "王五", "账户": "321313213213"},
       {"金额": 5000, "姓名": "赵六", "账户": "321313213213"}, {"金额": 49000, "姓名": "小明", "账户": "321313213213"},
       {"金额": 49000, "姓名": "小红", "账户": "321313213213"}]

all_bd = 98500
a = [300, 600, 800, 5000, 49000, 49000]
a.sort(reverse=True)
# print(a)
money_num = 0
acc = []
for i in a:
    acc.append(i)
    money_num += int(i)
    if money_num >= all_bd:
        break

l = []
for x in dic:
    if x["金额"] in acc:
        l.append(x)
print(l)
sorted_data = sorted(l, key=lambda x: x['金额'], reverse=True)
print(sorted_data)



