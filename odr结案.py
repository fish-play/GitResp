"""
-*- coding: utf-8 -*-

@Author : zp
@Time : 2022/7/5 17:42
@File : nb_odf_jiean.py
"""
"""
-*- coding: utf-8 -*-

@Author : zp
@Time : 2022/7/5 14:48
@File : nb_odr.py
"""
import datetime
import os.path
import time
import pandas as pd
from flows.flow import ScriptDef, FileItem, UserSelectItem, ListDataFlow, DirectoryItem
from rpalib.browser import Browser
from rpalib import browser
from rpalib.log import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

    def login(self):
        try:
            self.driver.get(self.url)
            self.browser_clear_and_send(self.is_visible('//input[@placeholder="请输入手机号"]'), self.username)
            self.browser_clear_and_send(self.is_visible('//input[@placeholder="请输入密码"]'), self.password)
            self.is_visible('//span[text()="登录"]').click()
            return True
        except Exception as e:
            return e.args[0]

    def click_element(self):
        self.error_list = [["案号", "错误缘由"]]

        for ah_hao in self.lists:
            logger.info(f'开始执行{ah_hao["案号"]}')
            # print(ah_hao["案号"])
            try:
                # 点击纠纷案件
                self.is_visible('//a[text()="纠纷案件"]').click()
                # 等待页面刷新
                self.is_visible('//span[text()="诉调纠纷"]')
            except Exception:
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                logger.error("70" + f'{ah_hao["案号"]}' + "网络超时！")
                self.login()
                continue


            try:
                # 输入案号
                self.is_visible('//div[@class="fr"]/input[@class="form-control"]').clear()
                self.is_visible('//div[@class="fr"]/input[@class="form-control"]').send_keys(ah_hao["案号"])
                # 点击搜索框
                self.is_visible('//button[text()="搜索"]').click()
            except Exception:
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                logger.error("71" + f'{ah_hao["案号"]}' + "网络超时！")
                self.login()
                continue

            # 判断案号是否一制
            try:
                num = 0
                for i in range(20):
                    print(num)
                    # if self.is_visible('//label[text()="诉调案号"]/../p[@class="fl ng-binding"]', wait_time=20):
                    if str(self.is_visible('//label[text()="诉调案号"]/../p[@class="fl ng-binding"]').text) == f'{ah_hao["案号"]}':
                        print(self.is_visible('//label[text()="诉调案号"]/../p[@class="fl ng-binding"]').text)
                        break
                    else:
                        print(111)
                        if num >= 20:
                            break
                        num += 1
                        time.sleep(1)
                        continue
            except Exception:
                print(103)
                if self.is_visible('//div[text()="没有数据！"]').text == "没有数据！":
                    print(self.is_visible('//div[text()="没有数据！"]').text)
                    self.error_list.append([ah_hao["案号"], "该案号没有数据！"])
                    print(97, self.error_list)
                    logger.error('93' + f'{ah_hao["案号"]}' + "该案号没有数据！")
                    self.login()
                    continue
                else:
                    logger.error("92" + f'{ah_hao["案号"]}' + "网络超时！")
                    self.error_list.append([ah_hao["案号"], "网络超时！"])
                    self.login()
                    continue
            # 判断是否为等待调解
            try:
                self.is_visible('//div[text()="等待调解"]').text == "等待调解"
            except Exception:
                continue

            try:
                # # 点击查详情
                self.is_visible('//div[@class="row"]/div/div/button[text()="查看详情"]')
                self.is_visible('//div[@class="row"]/div/div/button[text()="查看详情"]').click()
            except Exception:
                logger.error("92" + f'{ah_hao["案号"]}' + "网络超时！")
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                self.login()
                continue
            try:
                # 点击编辑
                self.is_visible('//span[text()="编辑"]')
                self.is_visible('//span[text()="编辑"]').click()
            except Exception:
                logger.error("101" + f'{ah_hao["案号"]}' + "网络超时！")
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                self.login()
                continue

            try:
                # 清空法定代表人信息
                self.is_visible('//*[@id="casePersonalCheck"]/div[1]//input[@placeholder="请输入代表人姓名"]', wait_time=60)
                self.is_visible('//*[@id="casePersonalCheck"]/div[1]//input[@placeholder="请输入代表人姓名"]').send_keys(Keys.CONTROL, "a")
                time.sleep(0.5)
                self.is_visible('//*[@id="casePersonalCheck"]/div[1]//input[@placeholder="请输入代表人姓名"]').send_keys(Keys.DELETE)
                # self.is_visible('//*[@id="casePersonalCheck"]/div[1]//input[@placeholder="请输入代表人姓名"]').clear()
            except Exception:
                logger.error("107" + f'{ah_hao["案号"]}' + "网络超时！")
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                self.login()
                continue
            time.sleep(0.5)
            try:
                # 清空手机号
                self.is_visible('//*[@id="casePersonalCheck"]/div[1]//input[@placeholder="请输入手机号码"]')
                self.is_visible('//*[@id="casePersonalCheck"]/div[1]//input[@placeholder="请输入手机号码"]').send_keys(Keys.CONTROL, "a")
                time.sleep(0.5)
                self.is_visible('//*[@id="casePersonalCheck"]/div[1]//input[@placeholder="请输入手机号码"]').send_keys(Keys.DELETE)
                # self.is_visible('//*[@id="casePersonalCheck"]/div[1]//input[@placeholder="请输入手机号码"]').clear()
            except Exception:
                logger.error("115" + f'{ah_hao["案号"]}' + "网络超时！")
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                self.login()
                continue
            time.sleep(0.5)
            try:
                # 删除申请人2
                self.is_visible('//*[@id="casePersonalCheck"]/div[2]//span[text()="删除"]')
                self.is_visible('//*[@id="casePersonalCheck"]/div[2]//span[text()="删除"]').click()
            except Exception:
                logger.error("120" + f'{ah_hao["案号"]}' + "网络超时！")
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                self.login()
                continue
            time.sleep(0.5)
            try:
                # 点击确定
                self.is_visible('//a[text()="确定"]', wait_time=60)
                self.is_visible('//a[text()="确定"]').click()
            except Exception:
                logger.error("129" + f'{ah_hao["案号"]}' + "网络超时！")
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                self.login()
                continue
            time.sleep(0.5)
            try:
                # 清空被申请人1的手机号
                self.is_visible('//*[@id="casePersonalCheck"]/div[3]//input[@placeholder="请输入联系方式"]')
                self.is_visible('//*[@id="casePersonalCheck"]/div[3]//input[@placeholder="请输入联系方式"]').clear()
            except Exception:
                logger.error("136" + f'{ah_hao["案号"]}' + "网络超时！")
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                self.login()
                continue
            time.sleep(0.5)
            # 点击空白
            self.is_visible('//*[@id="caseInfoEdit"]').click()

            # 点击保存
            try:
                self.is_visible('//div[text()="保存"]')
                self.is_visible('//div[text()="保存"]').click()
            except Exception:
                logger.error("174" + f'{ah_hao["案号"]}' + "网络超时！")
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                self.login()
                continue

            # 确认成功
            try:
                self.is_visible('//div[@class="layui-layer layui-layer-dialog"]/div[text()="操作成功"]')
                if self.is_visible('//div[@class="layui-layer layui-layer-dialog"]/div[text()="操作成功"]').text == "操作成功":
                    self.is_visible('//div[@class="layui-layer layui-layer-dialog"]/div[text()="操作成功"]/..//a[text()="确定"]').click()
            except Exception:
                logger.error("184" + f'{ah_hao["案号"]}' + "网络超时！")
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                self.login()
                continue

            # 页面拉倒最顶端
            for i in range(5):
                if self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL, Keys.HOME):
                    break
                else:
                    time.sleep(1)
                    continue
            time.sleep(1)

            # 点击调解状态
            try:
                self.is_visible('//*[@id="toggleStatus"]')
                self.is_visible('//*[@id="toggleStatus"]').click()
            except Exception:
                logger.error("195" + f'{ah_hao["案号"]}' + "网络超时！")
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                self.login()
                continue

            time.sleep(1)
            # 点击调解成功
            try:
                self.is_visible('//button[text()="调解状态 "]/..//li[text()="调解成功"]')
                self.is_visible('//button[text()="调解状态 "]/..//li[text()="调解成功"]').click()
            except Exception:
                logger.error("206" + f'{ah_hao["案号"]}' + "网络超时！")
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                self.login()
                continue
            time.sleep(1)
            # 点击达成口头协议
            try:
                self.is_visible('//li[text()="达成口头调解协议"]')
                self.is_visible('//li[text()="达成口头调解协议"]').click()
            except Exception:
                logger.error("216" + f'{ah_hao["案号"]}' + "网络超时！")
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                self.login()
                continue
            time.sleep(1)
            # 输入原因
            try:
                self.is_visible('//*[@id="reAllotSuc"]/div[@class="modal-box-centent"]/div[@class="box-centent-bottom"]/span[text()="原因"]/..//textarea')
                self.is_visible('//*[@id="reAllotSuc"]/div[@class="modal-box-centent"]/div[@class="box-centent-bottom"]/span[text()="原因"]/..//textarea').send_keys("调解成功")
            except Exception:
                logger.error("226" + f'{ah_hao["案号"]}' + "网络超时！")
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                self.login()
                continue
            time.sleep(1)
            # 点击确定
            try:
                self.is_visible('//*[@id="reAllotSuc"]/div[@class="modal-box-centent"]/div[@class="box-centent-bottom"]/span[text()="原因"]/../..//input[@value="确定"]')
                self.is_visible('//*[@id="reAllotSuc"]/div[@class="modal-box-centent"]/div[@class="box-centent-bottom"]/span[text()="原因"]/../..//input[@value="确定"]').click()
            except Exception:
                logger.error("236" + f'{ah_hao["案号"]}' + "网络超时！")
                self.error_list.append([ah_hao["案号"], "网络超时！"])
                self.login()
                continue

            # 点解第二个确定
            try:
                self.is_visible('//*[@class="layui-layer layui-layer-dialog"]//a[text()="确定"]')
                self.is_visible('//*[@class="layui-layer layui-layer-dialog"]//a[text()="确定"]').click()
            except Exception:
                self.login()
                continue
            time.sleep(1)

    def run(self):
        try:
            self.read_excel()
            assert self.login() is True, Exception("登录失败！")
        except Exception as e:
            logger.error(e.args[0])
            self.driver.quit()
        self.click_element()
        print(self.error_list)
        if len(self.error_list) > 1:
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
    title="宁波ODR结案",
    arguments=[
        UserSelectItem(title="账号", username_field="username", password_field="password"),
        FileItem(title="excel文件路径", name="excel_path"),
        DirectoryItem(title="错误保存路径：", name="saved_path"),

    ]
)

if __name__ == '__main__':
    ODR(r'18892679712', r'a0000000', r"C:\Users\9000\Desktop\试跑ODR结案11人.xlsx", r'C:\Users\9000\Desktop\ODR').run()