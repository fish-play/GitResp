"""
-*- coding: utf-8 -*-
@Time : 2022/9/14 9:43
"""
"""
-*- coding: utf-8 -*-
@Author : zp
@Time : 2022/7/5 14:48
@File : nb_odr.py
"""
import datetime
import os.path
import sys
import time
import pandas as pd
from flows.flow import ScriptDef, FileItem, UserSelectItem, ListDataFlow, DirectoryItem
from rpalib.browser import Browser
from rpalib import browser
from rpalib.log import logger
from selenium.webdriver.common.by import By
from openpyxl import Workbook


class ODR(ListDataFlow, Browser):

    def __init__(self, username, password, excel_path, saved_path):
        self.username = username
        self.password = password
        self.excel_path = excel_path
        self.saved_path = saved_path
        self.lists = []
        self.error_list = []
        self.url = "https://yundr.gov.cn/jsp/login/loginBymediate.html"
        self.driver = browser.Browser().driver

    def read_excel(self):
        df = pd.read_excel(self.excel_path)
        g = df.drop_duplicates(subset="案号")
        for name in g.index:
            data = df.loc[name].to_dict()
            self.lists.append(data)
        # print(self.lists)

    def login(self):
        try:
            self.driver.get(self.url)
            self.is_visible('//li[text()="调解机构"]').click()
            self.browser_clear_and_send(self.is_visible('//input[@placeholder="请输入手机号"]'), self.username)
            self.browser_clear_and_send(self.is_visible('//input[@placeholder="请输入密码"]'), self.password)
            self.is_visible('//span[text()="登录"]').click()
            time.sleep(20)
            return True
        except Exception as e:
            return e.args[0]

    def click_element(self):
        self.error_list = [["案号"]]
        for an_hao in self.lists:

            logger.info(f"开始执行{an_hao['案号']}")
            ah = str(an_hao["案号"])
            try:
                # 等待页面加载结束
                for i in range(100):
                    if self.driver.find_element(By.XPATH, '/html/body/div[@class="loading"]').is_displayed() == False:
                        break
                    time.sleep(1)
                # 输入案号
                self.is_visible('//*[@id="keyword"]').clear()
                self.is_visible('//*[@id="keyword"]').send_keys(ah)
                # 点击搜索
                self.is_visible('//a[text()="搜索"]').click()
                # 等待页面加载结束
                for i in range(100):
                    if self.driver.find_element(By.XPATH, '/html/body/div[@class="loading"]').is_displayed() == False:
                        break
                    time.sleep(1)
                # 点击更多
                self.is_visible('//button[@class="btn btn-default dropdown-toggle moreBtn"]').click()
                # 点击分配调解员
                self.is_visible('//button[text()="分配调解员"]').click()
                # 点击输入框
                self.is_visible('//*[@id="myModal2"]//button[text()="搜索"]/../input').clear()
                self.is_visible('//*[@id="myModal2"]//button[text()="搜索"]/../input').send_keys('赵泽宁')
                # 点击搜索
                self.is_visible('//*[@id="myModal2"]//button[text()="搜索"]').click()
                # 点击选择
                self.is_visible('//*[@id="myModal2"]/div/div/div/div[2]/div/div[4]/button[text()="选择"]').click()
                # 点击弹窗确定
                self.is_visible('//span[text()="确定"]').click()

                time.sleep(2)
                # 点击第二个弹窗确定
                for i in range(5):
                    if self.is_visible('//*[@class="layui-layer layui-layer-dialog"]/div[3]/a[text()="确定"]'):
                        print(self.is_visible('//*[@class="layui-layer layui-layer-dialog"]/div[3]/a[text()="确定"]').text)
                        self.is_visible('//*[@class="layui-layer layui-layer-dialog"]/div[3]/a[text()="确定"]').click()
                        print(222)
                        break
                    else:
                        time.sleep(1)

                        continue

                print(111)


                # 等待页面加载结束
                for i in range(100):
                    if self.driver.find_element(By.XPATH, '/html/body/div[@class="loading"]').is_displayed() == False:
                        break
                    time.sleep(1)
                time.sleep(5)
            except Exception:
                logger.error(f"{ah}-网络错误或页面出现错误，请检查！")
                self.error_list.append([ah])
                self.login()
                continue

    def run(self):
        try:
            self.read_excel()
            assert self.login() is True, Exception("登录失败！")
        except Exception as e:
            logger.error(e.args[0])
            self.driver.quit()
        self.click_element()
        if len(self.error_list) > 1:
            # now = datetime.datetime.now()
            # nows = str(now.strftime("%Y-%m-%d-%H-%M-%S"))
            # a = os.getcwd()
            # path = os.path.join(a, f"error-{nows}.txt")
            # for i in self.error_list:
            #     with open(path, "a") as file:
            #         file.write(i + f"时间为：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n")
            # logger.info(f"错误信息保存在：{path}")
            now = datetime.datetime.now()
            nows = str(now.strftime("%Y-%m-%d-%H-%M-%S"))
            wb = Workbook()
            ws = wb.worksheets[0]
            [ws.append(i) for i in self.error_list]
            wb.save(os.path.join(self.saved_path, f"output-{nows}.xlsx"))
            logger.error(f"报错信息保存在{os.path.join(self.saved_path, f'output-{nows}.xlsx')}")


export = ScriptDef(
    cls=ODR,
    group="宁波银行",
    title="宁波ODR立案",
    arguments=[
        UserSelectItem(title="账号", username_field="username", password_field="password"),
        FileItem(title="excel文件路径", name="excel_path"),
        DirectoryItem(title="错误l保存路径：", name="saved_path"),

    ]
)
if __name__ == '__main__':
    ODR(r'18892679255', r'123456yzfy', r"C:\Users\9000\Desktop\odr.xlsx", r"C:\Users\9000\Desktop\985").run()