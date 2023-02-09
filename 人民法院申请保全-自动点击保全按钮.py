"""
-*- coding: utf-8 -*-
@Time : 2022/9/7 17:10
"""
# import tkinter as tk
# import tkinter.font as tkFont
#
#
# class App:
#     def __init__(self, root, request_code):
#         #setting title
#         root.title("软件注册")
#         #setting window size
#         width=596
#         height=336
#         screenwidth = root.winfo_screenwidth()
#         screenheight = root.winfo_screenheight()
#         alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
#         root.geometry(alignstr)
#         root.resizable(width=False, height=False)
#         root.configure(bg="white")
#
#         GButton_700=tk.Button(root)
#         GButton_700["bg"] = "#00ced1"
#         ft = tkFont.Font(family='黑体',size=12)
#         GButton_700["font"] = ft
#         GButton_700["fg"] = "#000010"
#         GButton_700["justify"] = "center"
#         GButton_700["text"] = "确认"
#         GButton_700.place(x=150,y=220,width=108,height=33)
#         GButton_700["command"] = self.GButton_700_command
#
#         GButton_34=tk.Button(root)
#         GButton_34["bg"] = "white"
#         ft = tkFont.Font(family='黑体',size=12)
#         GButton_34["font"] = ft
#         GButton_34["fg"] = "#000000"
#         GButton_34["justify"] = "center"
#         GButton_34["text"] = "取消"
#         GButton_34.place(x=350,y=220,width=107,height=32)
#         GButton_34["command"] = self.GButton_34_command
#
#         GLabel_156=tk.Label(root)
#         ft = tkFont.Font(family='黑体',size=10)
#         GLabel_156["font"] = ft
#         GLabel_156["bg"] = 'white'
#         GLabel_156["fg"] = "#333333"
#         GLabel_156["justify"] = "center"
#         GLabel_156["text"] = f"获取注册码，请将下面字符(已复制到剪贴板)发送给工作人员获取\n{request_code[:20]}..."
#         GLabel_156.place(x=0, y=120,width=595,height=46)
#
#         self.GLabel_158 = tk.Label(root)
#         ft = tkFont.Font(family='黑体', size=10)
#         self.GLabel_158["font"] = ft
#         self.GLabel_158["bg"] = 'white'
#         self.GLabel_158["fg"] = "#333333"
#         self.GLabel_158["justify"] = "center"
#         self.GLabel_158.place(x=400, y=90, width=100, height=15)
#
#         self.NewPasswordEdit = tk.Entry(root)
#         self.NewPasswordEdit["borderwidth"] = "1px"
#         ft = tkFont.Font(family='黑体', size=15)
#         self.NewPasswordEdit["font"] = ft
#         self.NewPasswordEdit["fg"] = "#333333"
#         self.NewPasswordEdit["justify"] = "center"
#         self.NewPasswordEdit["text"] = "Entry"
#         self.NewPasswordEdit.place(x=200, y=80, width=200, height=36)
#
#         GLabel_157 = tk.Label(root)
#         ft = tkFont.Font(family='黑体', size=15)
#         GLabel_157["font"] = ft
#         GLabel_157["bg"] = 'white'
#         GLabel_157["fg"] = "#333333"
#         GLabel_157["justify"] = "center"
#         GLabel_157["text"] = "请输入注册码"
#         GLabel_157.place(x=0, y=25, width=595, height=46)
#
#     def GButton_700_command(self):
#
#         self.code = self.NewPasswordEdit.get()
#
#         return self.NewPasswordEdit.get()
#
#
#     def GButton_34_command(self):
#         print("exit")
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     def exit_app_x():
#         print(123)
#         root.quit()
#     root.protocol("WM_DELETE_WINDOW", exit_app_x)
#     app = App(root, "123")
#     root.mainloop()
import json
import time
import requests

from selenium import webdriver

from flows.flow import ListDataFlow, StringItem, ScriptDef, UserSelectItem
from rpalib.log import logger


class BaodanshenqingFlow(ListDataFlow):
    def __init__(self, username, password, data):
        super().__init__()
        self.data = data
        self.browser = webdriver.Chrome()
        self.browser.get('https://baoquan.court.gov.cn/#/home/index')
        self.browser.maximize_window()
        frame = self.browser.find_element_by_xpath(
            '//*[@id=\"index\"]/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/iframe')
        self.browser.switch_to.frame(frame)
        self.browser.find_element_by_xpath('//*[@id="root"]/div/form/div[1]/div[1]/div/div/div/input').send_keys(
            username)
        self.browser.find_element_by_xpath('//*[@id="root"]/div/form/div[1]/div[2]/div/div/div/input').send_keys(
            password)
        ret = self.browser.find_element_by_xpath('//*[@id="root"]/div/form/div/div[3]/span')
        ret.click()
        time.sleep(10)
        while True:
            cookies = self.browser.get_cookies()
            print(cookies)
            if len(cookies) >= 2:
                bearer = cookies[1].get('value')
                break
            time.sleep(1)
        cookies = f"Admin-UserData={cookies[0].get('value')}"
        logger.info("获取到cookie")
        self.headers = {"Accept": "*/*",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Connection": "keep-alive",
                        "Bearer": bearer,
                        "Cookie": cookies,
                        "Host": "baoquan.court.gov.cn",
                        "Referer": "https://baoquan.court.gov.cn/",
                        "sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                        "sec-ch-ua-mobile": "?0",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36", }

    def run(self):
        i = 1
        while True:
            logger.info(f"开始获取第{i}页")
            time.sleep(2)
            url = f"https://baoquan.court.gov.cn/wsbq/ssbq/api/ssdb/dbsqs?time={int(round(time.time() * 1000))}&rows=5&page={i}&selectValue=sqrxm&searchValue="
            i += 1
            ret = requests.get(url, headers=self.headers)
            print(self.headers)
            lists = json.loads(ret.text).get("data").get("list")
            bigger = 0
            if lists:
                for x in lists:
                    if x.get("dtTjsj"):
                        a = self.data.split('-')
                        b = x.get("dtTjsj").split('-')
                        print(a, b)
                        if int(a[0]) > int(b[0]):
                           bigger = 1
                        if int(a[0]) == int(b[0]) and int(a[1]) > int(b[1]):
                            bigger = 1
                        if int(a[0]) == int(b[0]) and int(a[1]) == int(b[1]) and int(a[2]) > int(b[2]):
                            bigger = 1
                        if bigger == 1:
                            break
                        if len(x.get("showBtn")) == 20:
                            r = requests.post(f'https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsq/sqbq?dbid={x.get("cId")}',
                                                headers=self.headers, data=json.dumps({'dbid': x.get("cId")}))
                            time.sleep(2)
                            if json.loads(r.text).get("data"):
                                requests.put(f'https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsq/tj?time={int(round(time.time() * 1000))}&id={json.loads(r.text).get("data").get("cId")}', headers=self.headers, data=json.dumps({'time': str(int(round(time.time() * 1000))),'id': json.loads(r.text).get("data").get("cId")}))
                                logger.info(f"{x.get('cSqbh')}: 提交完成")
                            else:
                                logger.info(f"{x.get('cSqbh')}: {json.loads(r.text).get('message')} 截止时间：{self.data}, 当前时间：{x.get('dtTjsj')}")
                            del r
                if bigger == 1:
                    logger.info(f"{self.data}之前的数据执行完成，结束")
                    break
            else:
                logger.info("所有数据执行完成，结束")
                break
            time.sleep(5)

export = ScriptDef(
        cls=BaodanshenqingFlow,
        group="外网保全系统",
        title="人民法院申请保全-自动点击保全按钮",
        description="人民法院申请保全-自动点击保全按钮",
        arguments=[
            UserSelectItem(title="账号", username_field="username", password_field="password"),
            StringItem(title="时间", name="data"),
        ]
    )

if __name__ == '__main__':
    BaodanshenqingFlow("18768132451", "Tcx123456.", "2020-01-02").run()