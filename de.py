# import re
# import fitz
# from rpalib.log import logger
# from flows.flow import ScriptDef, DirectoryItem, ListDataFlow
# import os
# from openpyxl import Workbook
# import time

# x = [
#     re.compile(r'\n(.*?)\n'),
#     re.compile(r'合同编号：(.*?)\n'),
#     re.compile(r'甲方（借款人）：(.*?)\n'),
#     re.compile(r'身份证号: (\d+)'),
#     re.compile(r'年利率\n(.*?)\n'),
#     re.compile(r'小写）.*?(\d+.\d+)'),
#     re.compile(r'开户行：(.*?)\n'),
#     re.compile(r'户名：(.*?)\n'),
#     re.compile(r'账号：(\d+)'),
#     re.compile(r'甲方的送达地址：(.*?)\n'),
#     re.compile(r'（接收号码）：(\d+)'),
#     re.compile(r'签署日期\n(.*?)\n')
# ]
#
# title = ['借款合同名称', '合同编号', '借款人姓名', '借款人身份证号', '年利率', '贷款金额', '开户行', '户名', '银行账号', '送达地址', '送达联系电话',
#          '借款协议签署日期', '报错']
#
#
# class WxPDFGet(ListDataFlow):
#
#     def __init__(self, dir_path, save_excel):
#         super().__init__()
#         self.dir_path = dir_path
#         now = time.strftime("%Y_%m_%d_%H_%M_%S")
#         self.save_excel = os.path.join(save_excel, '借款协议信息' + now + '.xlsx')
#         self.data = []
#
#     def write_excel(self):
#         wb = Workbook()
#         sh = wb.worksheets[0]
#         sh.append(["提取文件名称"] + title)
#         for i in self.data:
#             sh.append(i)
#         print(sh)
#         wb.save(self.save_excel)
#
#     @staticmethod
#     def find_info(pdf_path):
#         content = ""
#         y = []
#         doc = fitz.open(pdf_path)
#         # 拼接所有pdf文本
#         for i in doc:
#             content += i.get_text()
#         # 用来存放未匹配出的字段
#         result = []
#         for i in range(len(x)):
#             try:
#                 y.append(re.search(x[i], content).group(1).strip())
#             except AttributeError:
#                 result.append(title[i])
#                 y.append('')
#         co = '提取失败,'.join(result)
#         if co == "":
#             return y
#         return y + [co + '提取失败']
#
#     def run(self):
#
#         # self.write_csv('w', ["提取文件名称"] + title)
#         for i in os.listdir(self.dir_path):
#             if i.endswith(".pdf"):
#                 _data = [i.replace(".pdf", "")]
#                 logger.info(i)
#                 try:
#                     _data += self.find_info(os.path.join(self.dir_path, i))
#                 except RuntimeError:
#                     _data += ["" for _ in range(12)] + ["文件损坏"]
#
#                 self.data.append(_data)
#                 self.write_excel()
#         logger.info(f"运行完成！运行结果在 {self.save_excel}")


# from pdf2img import pdf2img
# class cs(object):
#     def __init__(self, main_path):
#         self.main_path = main_path
#
#     ''' 调用pdf2img生成jpg文件 '''
#     def cc(self):
#         pdf2img(self.main_path).run()
#
#     ''' 删除所有后缀为jpg的文件 '''
#     def delec(self):
#         for i in os.listdir(self.main_path):
#             if i.find("jpg") != -1:
#                 os.remove(os.path.join(self.main_path, i))
#
#
# if __name__ == '__main__':
#     cs(r'C:\Users\9000\Desktop\pdf').cc()
# pdf2img(r"C:\Users\9000\Desktop\pdf").run()

# ''' 临时文件'''
# import tempfile
# fp = tempfile.TemporaryFile()
# print(fp.name)
# fp.write('两情若是久长时，'.encode('utf-8'))
# fp.write('又岂在朝朝暮暮。'.encode('utf-8'))
# # 将文件指针移到开始处，准备读取文件
# fp.seek(0)
# print(fp.read().decode('utf-8')) # 输出刚才写入的内容
# # 关闭文件，该文件将会被自动删除
# fp.close()
# # 通过with语句创建临时文件，with会自动关闭临时文件
# with tempfile.TemporaryFile() as fp:
#     # 写入内容
#     fp.write(b'I Love Python!')
#     # 将文件指针移到开始处，准备读取文件
#     fp.seek(0)
#     # 读取文件内容
#     print(fp.read()) # b'I Love Python!'
# # 通过with语句创建临时目录
# with tempfile.TemporaryDirectory() as tmpdirname:
#     print('创建临时目录', tmpdirname)
''' 将对象转为二进制对象'''
# import pickle
# # tup1 = ('i like sleep', {1, 2, 3}, None)
# # print(tup1)
# for i in range(100):
#     tup1 = i
#     p1 = pickle.dumps(tup1)
#     print(p1)
#     t2 = pickle.loads(p1)
#     print(t2)
# ''' 将python对象转为二进制文件'''
# import pickle
# tup1 = ('i like sleep')
# with open('a.txt', 'wb') as f:
#     pickle.dump(tup1, f)
# with open('a.txt', 'rb') as e:
#     o = pickle.load(e)
#     print(o)
import asyncio
import time

import pygame

''' 拼接路径'''
# from pathlib import *
# path = PurePath('my_file.txt')
# print(type(path), path)
#
# path1 = PurePath('http:', 'c.biancheng.net', 'python')
# print(path1)
#
# path2 = PurePath('C://./my_file.txt')
# print(path2)

# ''' 查找列表中文件夹名称或者后缀，最后返回'''
# import fnmatch
# #filter()
# print(fnmatch.filter(['dlsf', 'ewro.txt', 'te.py', 'youe.py'], '*.txt'))
# #fnmatch()
# for file in ['word.doc','index.py','my_file.txt']:
#     if fnmatch.fnmatch(file,'*.txt'):
#         print(file)
# #fnmatchcase()
# print([addr for addr in ['word.doc','index.py','my_file.txt','a.TXT'] if fnmatch.fnmatchcase(addr, '*.txt')])
# #translate()
# print(fnmatch.translate('a*b.txt'))

''' 创建临时文件，并写进内存'''
# from tempfile import TemporaryFile
#
# f = TemporaryFile(mode="w+")
# f.write("i like sleep and game")
# f.seek(0)
# link = f.read()
# print(link)
#
#
# from PIL import Image
# import ftplib
# import urllib2
# import StringIO
#
# img_file = urllib.urlopen(img_url)
# try:
#     session = ftplib.FTP('FTP_server_url', id, pw)
#     session.storbinary('STOR image.jpg', img_file)
# except ftplib.all_errors as e:
#     print 'error'
# img_file.close()
# session.quit()
#
#
# import pickle
# tup1 = (r"C:\Users\9000\Desktop\新建文件夹\调解书-黄燕梅-44092119820621424X.pdf")
# with open('a.txt', 'wb') as f:
#     print(pickle.dump(tup1, f))
# with open('a.txt', 'rb') as e:
#     o = pickle.load(e)
#     print(o)

#
# import io
# import base64
# from PIL import Image
#
# def image2byte(image):
#     '''
#     图片转byte
#     image: 必须是PIL格式
#     image_bytes: 二进制
#     '''
#     # 创建一个字节流管道
#     img_bytes = io.BytesIO()
#     # 将图片数据存入字节流管道， format可以按照具体文件的格式填写
#     image.save(img_bytes, format="JPEG")
#     # 从字节流管道中获取二进制
#     image_bytes = img_bytes.getvalue()
#     return image_bytes
#
# def byte2image(byte_data):
#     '''
#     byte转为图片
#     byte_data: 二进制
#     '''
#     image = Image.open(io.BytesIO(byte_data))
#     return image

#
# image_path = r"C:\Users\9000\Desktop\新建文件夹\调解书-黄燕梅-44092119820621424X0001-1.jpg"
# image = Image.open(image_path)
# byte_data = image2byte(image)
# image2 = byte2image(byte_data)
#
#
# a = ['1', '2', '3']
# b = a.index("3")
# print(b)
#
#
# from playwright.sync_api import sync_playwright
#
# with sync_playwright() as p:
#     for browser_type in [p.chromium, p.firefox, p.webkit]:
#         browser = browser_type.launch()
#         page = browser.new_page()
#         page.goto('https://baidu.com/')
#         page.screenshot(path=f'example-{browser_type.name}.png')
#         browser.close()
#
# import asyncio
# from playwright.async_api import async_playwright
#
#
# async def main():
#     async with async_playwright() as p:
#         # Make sure to run headed.
#         browser = await p.chromium.launch(headless=False)
#
#         # Setup context however you like.
#         context = await browser.new_context()  # Pass any options
#         await context.route('**/*', lambda route: route.continue_())
#
#         # Pause the page, and start recording manually.
#         page = await context.new_page()
#         await page.pause()

#
# asyncio.run(main())
#
# from playwright.sync_api import Playwright, sync_playwright, expect
#
# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#
#     # Open new page
#     page = context.new_page()
#
#     # Go to https://www.jd.com/
#     page.goto("https://www.jd.com/")
#
#     # Click input[type="text"]
#     page.locator("input[type=\"text\"]").click()
#
#     # Fill input[type="text"]
#     page.locator("input[type=\"text\"]").fill("dian")
#
#     # Click button:has-text("")
#     # with page.expect_navigation(url="https://search.jd.com/Search?keyword=%E7%94%B5%E8%84%91&enc=utf-8&wq=%E7%94%B5%E8%84%91&pvid=17cc3e696d87448a9cb39d433dfa295a"):
#     with page.expect_navigation():
#         page.locator("button:has-text(\"\")").click()
#
#     # ---------------------
#     context.close()
#     browser.close()
#
# with sync_playwright() as playwright:
#     run(playwright)






# from playwright.sync_api import sync_playwright
#
# def new_cookie(url):
#     cookie = None
#     def set_cookie(req):
#         nonlocal cookie
#         if "cookie" in req.headers:
#             cookie = req.headers["cookie"]
#
#     with sync_playwright() as p:
#         browser = p.firefox.launch()
#         page = browser.new_page()
#         page.on("request", set_cookie)
#         page.goto(url)
#         browser.close()
#     print(cookie)
#     return cookie
#
# print(new_cookie("https://api.bilibili.com/x/web-show/res/locs?pf=0&ids=3449"))
# x = 1
# def func():
#     x = 2
#     def subfunc():
#         nonlocal x
#         x = x + 1
#         print('subfunc内打印的值：%d' % x)
#         return x
#     print('func内打印的值：%d' % x)
#
#     return subfunc()
# func()
# print('func外打印的值：%d' % x)
# def outer():
#     num = 10
#     def inner():
#         nonlocal num   # nonlocal关键字声明
#         num = 100
#         print(num)
#     inner()
#     print(num)
# outer()



# # wright = 600
# # height = 600
# # pygame.init()   # 调用前要初始化pygame
# # winSur = pygame.display.set_mode((wright, height))  # 创建一个黑窗口
# # font = pygame.font.SysFont('my_font.ttf', 30)   # 设置字体第一个参数为字体，第二个是字体大小
# # bg_suface = pygame.Surface((wright, height), flags=pygame.SRCALPHA)   # 将一个图像绘制到另一个图像上方
# # pygame.Surface.convert(bg_suface)
# # bg_suface.fill(pygame.Color(0, 0, 0, 28))
# # winSur.fill((0, 0, 0))
# # letter = [font.render(str(i), True, (0, 255, 0)) for i in range(10)]
# # texts = [
# #     font.render(str(letter[i]), True, (0, 255, 0)) for i in range(10)
# # ]
# # column = int(wright/12)
# # drops = [i for i in range(column)]
# # print(drops)
# # while True:
# #     ...
# #
# # a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
# #
# #
# # from apscheduler.schedulers.blocking import BlockingScheduler
# # sched = BlockingScheduler(timezone='Asia/Shanghai')
# # def job_function():
# #     print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
# # job = sched.add_job(job_function,'interval',hours = 0,minutes = 0,seconds=5,id='')
# # sched.start()
#
# import time
# # def count_down(name, delay):
# #     indents = (ord(name) - ord('A')) * '\t'
# #     print('这是indents',indents)
# #     n = 3
# #     while n:
# #         time.sleep(delay)
# #         duration = time.perf_counter() - start
# #         print('这是duration：', duration)
# #         print('-' * 40)
# #         print(f'{duration:.4f} \t{indents}{name} = {n}')
# #         n -= 1
# # start = time.perf_counter()
# # count_down('A', 1)
# # count_down('B', 0.8)
# # count_down('C', 0.5)
# # print('-' * 40)
# # print('Done')


import asyncio,random,time
#
# async def foo():
#     await asyncio.sleep(random.randint(1,8)/10.0)
#     end=time.time()
#     print(f"foo()耗时{end-start}秒")
#     return 101
#
# async def foo2():
#     await asyncio.sleep(random.randint(1,8)/10.0)
#     end=time.time()
#     print(f"foo2()耗时{end-start}秒")
#     return 102
#
# async def foo3():
#     await asyncio.sleep(random.randint(1,8)/10.0)
#     end=time.time()
#     print(f"foo3()耗时{end-start}秒")
#     return 103
#
# async def main():
#     R = [foo(), foo2(), foo3()]
#     '''
#     await
#     遇到IO操作挂起当前协程（任务），等IO操作完成之后再继续往下执行。
#     当前协程挂起时，事件循环可以去执行其他协程（任务）。
#     '''
#     await asyncio.gather(*R)
#
# if __name__ == "__main__":
#     start=time.time()
#     asyncio.run(main())
#
#     end=time.time()
#     print(f"__main__耗时{end-start}秒")
async def run():
    await asyncio.sleep(1)
    a = input(str('请输入数字'))
    print(a)

async def run1():
    await asyncio.sleep(0.3)
    b = 1
    c = b + 1
    print(c)
async def main():
    x = [run(), run1()]
    await asyncio.gather(*x)
if __name__ == "__main__":
    asyncio.run(main())