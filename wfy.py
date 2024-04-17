# -*- coding=utf-8 -*-
import os
import sys
import time, datetime
from typing import List
from mars.core.job import Job, JobType, DirectoryItem, SelectItem, FileItem, TaskInfo
from mars.core.log import logger
from uiautomation import Control
from PIL import ImageGrab
from PIL import Image
import pandas as pd
import re
import uiautomation
import win32api
import win32con
import pyautogui
from mars.rpalib.public import unit_testing
from mars.rpalib import tablesheet

OPTIONS = {"陕西省": "wxeb54303833a1fafd", "河北省": "wx52e5d083970ca3c0", "浙江省": "wx0ee1b0751f2aabcc",
           "福建省": "wx47f0f433442c6871", "重庆市": "wxf0e5e53a29ed4117", "广东省": "wx2006640312f6571f",
           "河南省": "wx53e74d7d55128c10", "湖北省": "wxf69c8463bd75ad44", "山东省": "wx92ba2fe8ff8dcbfd",
           "辽宁省": "wxec882ea9ce2726c6", "江西省": "wx0f74a03b8cb028eb", "安徽省": "wxf588fa6b90fa17b9",
           "江苏省": "wxc4e30c1507cc52cf", "黑龙江省": "wxfb1ba8b399cea2f9", "吉林省": "wx354706e7f760f6f3",
           "山西省": "wxbd798b19c5d7f15b", "内蒙古自治区": "wxc408de87cb68274e", "天津市": "wx90dca58e50c1023a",
           "甘肃省": "wx19ebe9f1c655d44d", "贵州省": "wxa6d40a50372562bc", "海南省": "wxacf9ab9cbb3f241c",
           "湖南省": "wx6eaf749a026ea093", "云南省": "wx7d3d9ca67c6ebcf5", "四川省": "wx93f27d4d1f1a3d08",
           }


class Program(Job):
    def __init__(self, task_info: TaskInfo):
        self.form_data = task_info.formData
        self.win = uiautomation.PaneControl(Name="人民法院在线服务")
        self.filename = time.strftime(
            "%Y-%m-%d %H时%M分%S秒", time.localtime())  # 启动时间
        self.row = None  # 行数据
        self.derail = task_info.formData.get('derail')
        self.case_type = task_info.formData.get('case_type')
        self.tjz_path = task_info.formData.get('tjz_path')
        self.dsh_path = task_info.formData.get('dsh_path')
        self.download_way = task_info.formData.get('download_way')
        self.download_paper = task_info.formData.get('download_paper')
        self.data = None
        self.li = []

    def read_excel(self):
        df = pd.read_excel(self.path)

        logger.info("加载表头")
        logger.info(tablesheet.sheet)

        # 校验表头
        list_head = []  # 请在这里添加需要检查的表头
        head = set(list_head) - set(df.columns)
        assert len(list(head)) == 0, Exception(f"{head} 表头不存在")

        # 检查必要目录结构
        dir_list = ["被告资料", "原告资料"]  # 请添加dir_path 必须要存在的目录
        for i in dir_list:
            if not os.path.exists(os.path.join(self.dir_path, i)):
                print(os.path.join(self.dir_path, i))
                raise Exception(f'{os.path.join(self.dir_path, i)}目录不存在,请检查')
        # if not os.path.exists(os.path.join(self.dir_path, "原告资料", "原告资料.pdf")):
        #     raise FileExistsError(
        #         f'{os.path.join(self.dir_path, "原告资料", "原告资料.pdf")}文件不存在,请检查')

        list_temp = re.findall('代理人\d+姓名', '-'.join(df.columns.tolist()))
        if not list_temp: raise Exception("表格代理人识别失败 请重新填写代理人表头")

        # 去除空行列
        df.dropna(axis=0, how='all', inplace=True)
        df.dropna(axis=1, how='all', inplace=True)
        df.fillna("", inplace=True)

        # 增加列 根据需要增加
        if '行号' not in df.columns:
            df.insert(loc=0, column='行号', value=[
                i + 1 for i in range(len(df))])
        if '执行状态' not in df.columns:
            df["执行状态"] = ""
        if '错误原因' not in df.columns:
            df["错误原因"] = ""
        if '执行截图状态' not in df.columns:
            df['执行截图状态'] = ""

        # 将数据全部转成str方便输入
        for i in df.columns:
            df[i] = df[i].astype(str)

        if len(df) == 0:
            logger.info("表格无数据,程序结束")
            sys.exit()

        tablesheet.sheet.set_row_header(["被申请人姓名", '被申请人证件号', '执行状态', '错误原因', '执行截图状态'])

        # 判断文件是否被打开
        try:
            df2 = df.drop('行号', axis=1)
            df2.to_excel(self.path, index=False)
        except Exception as e:
            print(e)
            logger.error(f"访问被拒绝 请关闭表格 {self.path}")
            sys.exit()
        return df

    def GetFirstChild(self, control):
        return control.GetFirstChildControl()

    def GetNextSibling(self, control):
        return control.GetNextSiblingControl()

    def enumeration(self, value, maxDepth=None):
        data_list = []
        for control, depth in uiautomation.WalkTree(value, getFirstChild=self.GetFirstChild,
                                                    getNextSibling=self.GetNextSibling, includeTop=True,
                                                    maxDepth=maxDepth):
            if '人民法院在线服务' in control.Name:
                if re.findall('人民法院在线服务\w+$', control.Name):
                    data_list.append(control)
                    return control

    def is_open(self):
        """判断窗口是否在最前端并已经打开"""
        try:
            self.win = self.enumeration(uiautomation.GetRootControl(), 2)
            print("win", self.win)
            self.win.SetTopmost(True)
            logger.info("获取窗口信息")
            if self.win.BoundingRectangle.width() <= 0 and self.win.BoundingRectangle.height() <= 0:
                logger.error("法院窗口置顶失败,请手动将法app至最前端")
                return False
            return True
        except Exception as e:
            logger.error("请打开人民法院在线服务")
            return False

    def is_node(self, value, _type, datetime: float = 1):
        for i in range(int(datetime)):
            try:
                "等待元素出现"
                if _type == "TextControl":
                    node = self.win.TextControl(Name=value)
                    print(node)
                    time.sleep(0.3)
                    return node
                elif _type == "ButtonControl":
                    node = self.win.ButtonControl(Name=value)
                    print(node)
                    time.sleep(0.3)
                    return node
            except Exception as e:
                print(e)
                time.sleep(1)
                datetime -= 1
                if datetime < 0:
                    return None

    def court_choice(self):
        logger.info(f'申请所在市: {self.row.get("申请所在市")}')
        node = self.win.TextControl(Name=self.row.get("申请所在市")).GetParentControl().GetParentControl()
        for c, d in uiautomation.WalkControl(node, maxDepth=2):
            if d == 2:
                c.Click()
            if c.Name == self.row.get("申请所在市"):
                break

        logger.info(f'申请法院: {self.row.get("申请法院")}')
        node = self.win.TextControl(Name=self.row.get("申请法院")).GetParentControl().GetParentControl()
        for c, d in uiautomation.WalkControl(node, maxDepth=2):
            if d == 2: c.Click()
            if c.Name == self.row.get("申请法院"): break

        self.win.TextControl(Name=f"{self.case_type}").Click()

        if self.province == '浙江省':
            self.win.ButtonControl(Name="下一步").Click()
        else:
            self.win.TextControl(Name="下一步").Click()
        return True

    def GetControl(self, names: List[str]) -> Control:
        for control, depth in uiautomation.WalkControl(self.win):
            if control.Name.strip() in names:
                return control

    def register(self):
        if self.win.Name == "人民法院在线服务浙江":
            self.win.TextControl(Name="在线立案").Click()
        else:
            self.win.TextControl(Name="我要立案").Click()
        # 有些时候点击我要立案后审判立案的窗口不会立刻显示出来
        while True:
            try:
                self.win.ButtonControl(Name="审判立案").Click()
            except:
                print(11)
                continue
            break
        try:
            # 部分情况下没有不愿意按钮 超时跳过
            self.win.TextControl(Name="不愿意").Click()
        except Exception as e:
            print(e)

        self.win.ButtonControl(Name="审判立案").Click()
        self.win.ButtonControl(Name="为他人或公司等组织申请").Click()
        return True

    def txt_define(self):
        if self.province == "江苏省":
            self.win.ButtonControl(Name="下一步/").Click()
            time.sleep(0.2)
            return True
        label = '一、因身份认证和诉讼需要，本平台将采集各类用户的姓名、身份证号、手机号等信息。进入本平台并认证，视为同意采集上述信息。'
        self.win.TextControl(Name=label).Click()
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -150)
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -150)
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -150)
        time.sleep(0.2)
        if self.province == '浙江省':
            self.win.ButtonControl(Name='我已知晓，继续立案').Click()
        else:
            self.win.ButtonControl(Name="下一步").Click()
        return True

    def upload_file(self, item, path, index: int):

        print("上传", item)
        for i in range(10):
            if \
                    self.win.TextControl(
                        Name='当事人身份证明').GetParentControl().GetParentControl().GetParentControl().GetChildren()[
                        index].GetChildren()[0].GetChildren()[0].BoundingRectangle.width() > 0:
                self.win.TextControl(
                    Name='当事人身份证明').GetParentControl().GetParentControl().GetParentControl().GetChildren()[
                    index].GetChildren()[0].GetChildren()[0].Click()
                break
            time.sleep(0.5)

        self.win.TextControl(Name="本地PDF").Click()

        for i in range(2):
            # 等待文件上传按钮出现
            node = self.is_node("知道了", "ButtonControl", 6)
            if not node:
                logger.error("上传按钮(知道了)未找到")
                raise Exception("上传按钮(知道了)未找到")
            node.Click()

            # 等待窗口打开并操作
            for i in range(10):
                win = uiautomation.WindowControl(Name="打开")
                if win.Exists():
                    win.EditControl(Name="文件名(N):").SendKeys(path)
                    win.ButtonControl(Name="打开(O)").Click()
                    break
                elif i == 10:
                    self.win.ButtonControl(Name="关闭").Click()
                    raise Exception("上传输入框打开失败")
                time.sleep(0.5)

            # 判断上传成功
            node = self.is_node("上传材料", "TextControl", 10)

            if not node:
                if self.win.TextControl(Name='提示').Exists():
                    self.win.ButtonControl(Name="确认").Click()
                    continue
                else:
                    raise Exception(f"{path} 资料上传失败")
            return True

    def upload(self):
        if self.province == '浙江省':
            self.upload_file("起诉状 ", self.row.get("起诉状"), 1)
            if self.derail == '是':
                self.upload_file("支付令", self.row.get("支付令"), 1)

            for file in self.row.get("当事人身份证明"):
                print("当事人身份证明:",
                      self.upload_file("当事人身份证明", file, 3))

            self.upload_file("委托代理人委托手续和身份材料", self.row.get("授权委托书"), 5)
            for j in self.row.get("代理人列表"):
                self.upload_file("委托代理人委托手续和身份材料", j.get("代理人身份证"), 5)
            if self.form_data.get("type_") == '执业律师':
                self.upload_file('委托代理人委托手续和身份材料', self.row.get("所函"), 5)

            # 下拉
            self.win.TextControl(Name="当事人身份证明").Click()
            for i in range(10):
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -80)

            tmp = ['证据材料', '证据目录及证据材料']
            control = self.GetControl(tmp)
            if not control:
                raise Exception(f"控件：{tmp} 获取失败")
            for file in self.row.get("证据材料"):
                print(f"证据材料: {file}", self.upload_file(control.Name, file, 7))

            # 滚动
            self.win.TextControl(Name=control.Name).Click()
            for i in range(10):
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -150)
            if self.row['申请法院'] == "湖州市南浔区人民法院":
                print("其他材料：", self.upload_file("其他材料", self.row.get("保全申请书"), 9))
                print("其他材料：", self.upload_file("其他材料", self.row.get("查控冻结申请书"), 9))
                print("其他材料：", self.upload_file("其他材料", self.row.get("保函"), 9))
        else:
            self.upload_file("起诉状 ", self.row.get("起诉状"), 1)

            for file in self.row.get("当事人身份证明"):
                print("当事人身份证明:",
                      self.upload_file("当事人身份证明", file, 3))

            self.upload_file("委托代理人委托手续和身份材料", self.row.get("授权委托书"), 5)
            for j in self.row.get("代理人列表"):
                self.upload_file("委托代理人委托手续和身份材料", j.get("代理人身份证"), 5)
            print(111)
            if self.form_data.get("type_") == '执业律师':
                self.upload_file('委托代理人委托手续和身份材料', self.row.get("所函"), 5)

            # 下拉
            self.win.TextControl(Name="当事人身份证明").Click()
            for i in range(10):
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -80)

            tmp = ['证据材料', '证据目录及证据材料']
            control = self.GetControl(tmp)
            if not control:
                raise Exception(f"控件：{tmp} 获取失败")
            for file in self.row.get("证据材料"):
                print(f"证据材料: {file}", self.upload_file(control.Name, file, 7))

        # 下拉
        self.win.TextControl(Name=control.Name).Click()
        for i in range(round(len(self.row.get('证据材料'))/3)+5):
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -150)
        if self.download_way == "引入":
            control = self.GetControl(["送达地址确认书"])
            # 送达地址确认书  点击引用 选择第一个
            # self.win.TextControl(Name="送达地址确认书").GetParentControl().ImageControl().Click()
            control.GetParentControl().ImageControl().Click()
            node = self.win.ButtonControl(Name="选择")
            if not node.Exists():
                raise Exception('确认送达书不存在请在微信中设置')
            node.Click()
        else:
            self.upload_file('送达地址确认书', self.row.get("送达地址确认书"), 11)
        # 滚动
        self.win.TextControl(Name=control.Name).Click()
        for i in range(10):
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -150)
        if self.province == "福建省":
            print(1)
            if self.download_paper == "本地上传":
                if self.row.get("收款账户确认书").endswith('pdf'):
                    self.upload_file("收款账户确认书", self.row.get("收款账户确认书"), 13)
                else:
                    self.upload_jpg("收款账户确认书", self.row.get("收款账户确认书"), 13)
            elif self.download_paper == "引入":
                control = self.GetControl(["收款账户确认书"])
                control.GetParentControl().ImageControl().Click()
                try:
                    self.win.TextControl(Name="删除").Click()
                    self.win.ButtonControl(Name="确定").Click()
                except Exception:
                    ...
                # 点击添加收款账户
                self.win.TextControl(Name="添加收款账户").Click()
                print("收款人姓名:", self.input_to("收款人姓名", self.row.get("收款人姓名")))
                print("统一社会代码:", self.input_to("统一社会代码", self.row.get("统一社会信用代码")))
                print("收款人账户:", self.input_to("收款人账户", self.row.get("收款人账户")))
                print("收款人开户行:", self.input_to("收款人开户行", self.row.get("收款人开户行")))
                print("联系方式:", self.input_to("联系方式", self.row.get("联系方式")))
                self.win.TextControl(Name="确认生成收款账户确认书").Click()
                node = self.win.ButtonControl(Name="选择")
                if not node.Exists():
                    raise Exception('收款账户确认书不存在请在微信中设置')
                node.Click()
        # 下一步
        if self.province == '浙江省':
            self.win.ButtonControl(Name="下一步").Click()
            time.sleep(5)
        else:
            self.win.TextControl(Name="下一步").Click()
        return True

    def upload_jpg(self, data_name, file, num: int):
        for i in range(10):
            if self.win.TextControl(
                    Name='当事人身份证明').GetParentControl().GetParentControl().GetParentControl().GetChildren()[
                num].GetChildren()[0].GetChildren()[0].BoundingRectangle.width() > 0:
                self.win.TextControl(
                    Name='当事人身份证明').GetParentControl().GetParentControl().GetParentControl().GetChildren()[
                    num].GetChildren()[0].GetChildren()[0].Click()
                break
            time.sleep(0.5)
        self.win.TextControl(Name="图片相册").Click()
        for i in range(2):
            for i in range(10):
                win = uiautomation.WindowControl(Name="打开")
                if win.Exists():
                    win.EditControl(Name="文件名(N):").SendKeys(file)
                    win.ButtonControl(Name="打开(O)").Click()
                    break
                elif i == 10:
                    self.win.ButtonControl(Name="关闭").Click()
                    raise Exception("上传输入框打开失败")
                time.sleep(0.5)

            # 判断上传成功
            node = self.is_node("上传材料", "TextControl", 10)
            if not node:
                if self.win.TextControl(Name='提示').Exists():
                    self.win.ButtonControl(Name="确认").Click()
                    continue
                else:
                    raise Exception(f"{path} 资料上传失败")
            break
        self.win.TextControl(Name="确认").Click()
        while True:
            if self.win.TextControl(Name="正在转换文件").Exists():
                continue
            break

    def mouse_move(self, x1, y1):
        # print(x1, y1)
        x, y = win32api.GetCursorPos()
        y += y1
        x += x1
        # print(x, y)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.5)
        win32api.SetCursorPos((x, y))
        time.sleep(0.5)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def select(self, name: str, index: int, item: str):

        try:
            node_type = self.win.TextControl(
                Name=name).GetParentControl().GetParentControl()
            node = node_type.TextControl(5, None, index)

            # 判断值是否匹配 匹配则不用处理
            if node.Name == item:
                return True
            else:
                node.Click()
                mz = self.win.TextControl(Name=item)

                # 提取选项列表
                index_list = []
                hw_list = []
                for i in mz.GetParentControl().GetParentControl().GetChildren():
                    for j in i.GetChildren():
                        index_list.append(j.Name)
                        hw_list.append(j)
                # 操作选项
                # 对代理人针对处理
                start = 0 if "请选择" == node.Name else index_list.index(
                    node.Name)
                end = index_list.index(item)
                while True:
                    if start > end:
                        print("上拉")
                        node = hw_list[start]
                        print(node)
                        node.MoveCursorToInnerPos()
                        self.mouse_move(0, 49)
                        start -= 1
                    elif end > start:
                        node = hw_list[start]
                        node.MoveCursorToInnerPos()
                        self.mouse_move(0, -49)
                        start += 1
                    elif start == end:
                        time.sleep(1)
                        break
                time.sleep(1.5)
                self.win.HyperlinkControl(Name="确定").Click()

            return True
        except Exception as e:
            logger.error(f"select Error {name} 操作失败:", e)
            raise Exception(f"select Error {name} 操作失败:", e)

    def input_value(self, name: str, value: str):
        try:
            node_type = self.win.TextControl(
                Name=name).GetParentControl().GetParentControl()
            node = node_type.EditControl()
            # print(node)
            node.Click()
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            # print(value)
            node.SendKeys("{delete}" + "{}".format(value))
            return True
        except Exception as e:
            logger.error(f"input_value Error {name} 操作失败:", e)
            raise Exception(f"input_value Error {name} 操作失败:", e)

    def input_to(self, item, value):
        node = self.win.TextControl(Name=item)
        # print(node.BoundingRectangle)
        if node.BoundingRectangle.width() == 0 and node.BoundingRectangle.height() == 0:
            raise Exception("元素异常捕获,界面出现异常")
        node.Click()
        pyautogui.press('Tab')
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        uiautomation.SetClipboardText(str(value))
        pyautogui.hotkey('ctrl', 'v')
        return True

    def plaintiff(self):
        self.win.TextControl(Name="添加诉讼参与人").Click()
        print("身份类型:", self.select("身份类型", 3, "原告"))
        print("当事人类型处理:", self.select("当事人类型", 3, "法人"))
        Flag = True
        i = 10
        while i and Flag:
            if self.GetControl(["法人"]): Flag = False
            print("重新选择当事人类型:", self.select("当事人类型", 3, "法人"))
            time.sleep(1)
            i -= 1
        if Flag: raise Exception("原告当事人类型选择失败")

        print("单位名称:", self.input_to("单位名称", self.row.get("申请人单位")))
        print("单位住所地:", self.input_to(
            "单位住所地", self.row.get("申请人单位地址").replace(" ", "")))
        print("证照类型:", self.select("证照类型", 3, "社会统一信用代码证"))
        print("证照号码:", self.input_to("证照号码", self.row.get("申请人单位证照号码")))
        print("法定代表人姓名:", self.input_to("法定代表人姓名", self.row.get("申请人法定人")))
        print("法定代表人职务:", self.input_to("法定代表人职务", self.row.get("申请人职务")))
        self.win.TextControl(Name="证件号码").Click()
        for i in range(10):
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -150)
        time.sleep(0.4)
        print("证件类型:", self.select("证件类型", 2, "居民身份证"))
        print("证件号码:", self.input_to("证件号码", self.row.get("法人身份证")))
        print("手机号码:", self.input_to("手机号码", self.row.get("申请人手机号")))
        # print("单位性质:", self.select("单位性质", 2, "私营企业"))
        # 保存
        self.win.ButtonControl(Name="保存").Click()
        return True

    def defendant(self):
        self.win.TextControl(Name="添加诉讼参与人").Click()
        print("身份类型:", self.select("身份类型", 3, "被告"))
        print("当事人类型处理:", self.select("当事人类型", 3, "自然人"))
        Flag = True
        i = 10
        while i and Flag:
            if self.GetControl(["自然人"]): Flag = False
            print("重新选择当事人类型:", self.select("当事人类型", 3, "自然人"))
            time.sleep(1)
            i -= 1
        if Flag: raise Exception("被告当事人类型选择失败")
        print("姓名:", self.input_to("姓名", self.row.get("被申请人姓名")))
        print("证件类型:", self.select("证件类型", 2, "居民身份证"))
        print("证件号码:", self.input_to("证件号码", self.row.get("被申请人证件号")))
        for i in range(10):
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -150)
        time.sleep(2)
        print("住所:", self.input_to("住所", self.row.get("被申请人地址")))
        print("手机号码:", self.input_to("手机号码", self.row.get("被申请人手机号")))

        # 保存9910828
        self.win.ButtonControl(Name="保存").Click()

    def del_agent(self):
        """根据列表删除对应信息"""
        node = self.win.TextControl(Name="当事人信息").GetParentControl().GetParentControl()
        control_list = []
        for i in ["代理人", "被告", "原告"]:
            try:
                print(f"开始获取 {i} 元素")
                control1 = node.TextControl(Name=i).GetParentControl(
                ).GetParentControl().GetParentControl()
                print(control1)
                control_list.append(control1)
            except Exception as e:
                print(e)

        for node in control_list:
            while True:
                but = node.ImageControl()
                if but.Exists():
                    but.Click()
                    self.win.ButtonControl(Name="确定").Click()
                else:
                    break

        print("删除信息成功")

    def add_agent(self, row):

        try:
            self.win.TextControl(Name=f"{self.row['代理人姓名']}").Click()

            if self.form_data.get("type_") == '执业律师':
                # 选择类型
                print("代理人类型:", self.select("代理人类型", 3, "执业律师"))
                # 输入证件号码
                print("执业证号:", self.input_to("执业证号", row.get("代理人执业证号")))
            else:
                # 选择类型
                print("代理人类型:", self.select("代理人类型", 3, "当事人的近亲属或工作人员"))

            # 输入手机号码
            print("手机号码:", self.input_to("手机号码", row.get("代理人手机号")))

            return
        except:
            pass

        self.win.TextControl(Name="添加诉讼参与人").Click()

        # 选择代理人
        print("身份类型:", self.select("身份类型", 3, "代理人"))
        Flag = True
        i = 10
        while i and Flag:
            if self.GetControl(["代理人"]): Flag = False
            print("重新选择身份类型:", self.select("身份类型", 3, "代理人"))
            time.sleep(1)
            i -= 1
        if Flag: raise Exception("代理人身份类型选择失败")

        # 勾选
        for i in range(20):
            if not self.win.CheckBoxControl().GetTogglePattern().ToggleState:
                self.win.CheckBoxControl().GetTogglePattern().Toggle()
                time.sleep(1)
                if self.win.CheckBoxControl().GetTogglePattern().ToggleState:
                    break
                else:
                    continue
            time.sleep(1)

        if not self.win.CheckBoxControl().GetTogglePattern().ToggleState:
            raise Exception('勾选选项勾选失败')

        if self.form_data.get("type_") == '执业律师':
            # 选择类型
            print("代理人类型:", self.select("代理人类型", 3, "执业律师"))
            # 输入证件号码
            print("执业证号:", self.input_to("执业证号", row.get("代理人执业证号")))
        else:
            # 选择类型
            print("代理人类型:", self.select("代理人类型", 3, "当事人的近亲属或工作人员"))

        # 输入姓名
        print("姓名:", self.input_to("姓名", row.get("代理人姓名")))

        # 选择身份证
        print("证件类型:", self.select("证件类型", 3, "居民身份证"))

        # 输入证件号码
        print("证件号码:", self.input_to("证件号码", row.get("代理人证件号")))

        # 输入职业机构
        print("执业机构:", self.input_to("执业机构", row.get("代理人职业机构")))

        # 输入手机号码
        print("手机号码:", self.input_to("手机号码", row.get("代理人手机号")))

        # 点击保存
        self.win.ButtonControl(Name="保存").Click()

    def del_all(self):
        """删除所有数据"""
        node = self.win.TextControl(Name="当事人信息").GetParentControl().GetParentControl()
        node_list = []
        for c, d in uiautomation.WalkControl(node, maxDepth=4):
            if c.Name == "待补全":
                node_list.append(c)

        if len(node_list) > 5:
            for i in range(10):
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -150)

        for i in node_list[::-1]:
            node = i.GetParentControl().GetParentControl()
            node.ImageControl().Click()
            try:
                self.win.ButtonControl(Name="确定").Click()
            except:
                pass

    def data_check(self):
        # 输入标金额
        node = self.win.EditControl()
        node.Click()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        uiautomation.SetClipboardText(str(self.row["标的金额"]))
        pyautogui.hotkey('ctrl', 'v')

        # 判断元素消失也需要等待时间, 故先做等待处理 如后期机器运行等待时间不一在做循环等待元素消失
        time.sleep(2)

        # 删除数据
        self.del_all()
        time.sleep(2)
        # 添加原告
        self.plaintiff()

        # 添加被告
        self.defendant()

        # 删除数据
        self.del_all()
        if self.province == '浙江省':

            # 添加代理人
            rows = []
            for i in range(1, len(self.row["代理人列表"]) + 1):
                rows.append({"代理人姓名": self.row[f'代理人{i}姓名'],
                             "代理人证件号": self.row.get(f"代理人{i}证件号"),
                             "代理人手机号": self.row.get(f"代理人{i}手机号"),
                             "代理人执业证号": self.row.get(f"代理人{i}执业证"),
                             "代理人职业机构": self.row.get(f"代理人{i}执业机构"),
                             })

            for i in rows:
                self.add_agent(i)
        else:
            # 添加代理人
            rows = []
            for i in range(1, len(self.row["代理人列表"]) + 1):
                rows.append({"代理人姓名": self.row[f'代理人{i}姓名'],
                             "代理人证件号": self.row.get(f"代理人{i}证件号"),
                             "代理人手机号": self.row.get(f"代理人{i}手机号"),
                             "代理人执业证号": self.row.get(f"代理人{i}执业证"),
                             "代理人职业机构": self.row.get(f"代理人{i}执业机构"),
                             })

            for i in rows:
                self.add_agent(i)

        # 删除数据
        self.del_all()

        return True

    # 简单的校验数据是否为空 路径是否存在
    def check(self, data):
        if type(data) == str:
            if not os.path.exists(str(data)):
                raise Exception(f"{data}文件不存在,请检查文件是否真实存在或者对应字段是否有误")
            return

        for key, value in data.items():
            if self.dir_path in str(value):
                if not os.path.exists(str(value)):
                    print(str(value))
                    raise Exception(f"{key}文件不存在,请检查文件是否真实存在或者对应字段是否有误")
            if type(value) == list:
                for item in value:
                    self.check(item)

    def data_processing(self):

        self.row["起诉状"] = os.path.join(self.dir_path, '起诉状',
                                          f'{self.row.get("被申请人姓名")}-{self.row.get("被申请人证件号")}-起诉状.pdf')
        if self.derail == '是':
            self.row["支付令"] = os.path.join(self.dir_path, '支付令申请书',
                                              f'{self.row.get("被申请人姓名")}-{self.row.get("被申请人证件号")}-支付令申请书.pdf')
        self.row["授权委托书"] = os.path.join(self.dir_path, '代理人资料', "授权委托书",
                                              f'{self.row.get("被申请人姓名")}-{self.row.get("被申请人证件号")}-授权委托书.pdf')

        list_temp = re.findall('代理人\d+姓名', '-'.join(self.data.columns.tolist()))
        if not list_temp: raise Exception("表格代理人失败请处理")
        self.row["代理人列表"] = [{
            "代理人身份证": os.path.join(self.dir_path, '代理人资料', f'代理人身份证{index + 1}.pdf'),
        } for index, value in enumerate(list_temp)]
        if self.form_data.get("type_") == '执业律师':
            self.row["所函"] = os.path.join(self.dir_path, "代理人资料", "所函",
                                            f"{self.row.get('被申请人姓名')}-{self.row.get('被申请人证件号')}-所函.pdf")

        if self.download_way == "本地上传":
            self.row["送达地址确认书"] = os.path.join(self.dir_path, "送达地址确认书",
                                                      f"{self.row.get('被申请人姓名')}-{self.row.get('被申请人证件号')}-送达地址确认书.pdf")
        if self.province == "福建省" and self.download_paper == "本地上传":
            paper_file = os.path.join(self.dir_path, "收款账号确认书")
            for paper_name in os.listdir(paper_file):
                if f"{self.row.get('被申请人姓名')}-{self.row.get('被申请人证件号')}-收款账号确认书" in paper_name:
                    self.row["收款账户确认书"] = os.path.join(self.dir_path, "收款账号确认书", paper_name)
                    break

            # paper_name = f"{self.row.get('被申请人姓名')}-{self.row.get('被申请人证件号')}-收款账号确认书.pdf"
            # if paper_name not in os.listdir(os.path.join(self.dir_path, "收款账号确认书")):
            #     paper_name = f"{self.row.get('被申请人姓名')}-{self.row.get('被申请人证件号')}-收款账号确认书.jpg"
            # self.row["收款账户确认书"] = os.path.join(self.dir_path, "收款账号确认书", paper_name)

        temp = os.path.join(self.dir_path, '被告资料',
                            f'{self.row.get("被申请人姓名")}{self.row.get("被申请人证件号")}')

        if self.province == '浙江省' and self.row['申请法院'] == "湖州市南浔区人民法院":
            temp_s = os.path.join(self.dir_path, '保全申请书',
                                  f'{self.row.get("被申请人姓名")}-{self.row.get("被申请人证件号")}-保全申请书.pdf')
            self.row["保全申请书"] = temp_s  # 保全申请书
            temp_s = ''
            for path_s in os.listdir(os.path.join(self.dir_path, '查控冻结申请书')):
                if self.row.get("被申请人姓名") in path_s and self.row.get("被申请人证件号") in path_s:
                    temp_s = os.path.join(self.dir_path, '查控冻结申请书', path_s)
            self.row["查控冻结申请书"] = temp_s  # 查控冻结申请书
            temp_s = os.path.join(self.dir_path, '保函', '担保资料.pdf')
            self.row["保函"] = temp_s  # 保函
        self.row["证据材料"] = []
        self.row["当事人身份证明"] = []
        for file in os.listdir(temp):
            if file.endswith('.db'):
                continue
            if "被告身份证" in file:
                self.row["当事人身份证明"].append(os.path.join(temp, file))
                continue
            self.row["证据材料"].append(os.path.join(temp, file))

        self.row["当事人身份证明"].append(os.path.join(
            self.dir_path, '原告资料', self.row.get("申请人单位"), '原告资料.pdf'))

        # 校验文件路径
        self.check(self.row)
        print("文件处理完毕")
        print(self.row)

    def out_excel(self, data):
        data_to = {}
        for item in data:
            for key, value in item.items():
                if item.get("执行完成") == "执行完成":
                    break
                if key in ["起诉状", "当事人身份证明", "委托代理人委托手续", "委托代理人身份材料", "证据材料"]:
                    continue
                if data_to.get(key):
                    data_to[key].append(value)
                else:
                    data_to[key] = [value]
        df = pd.DataFrame.from_dict(data_to)

        if data_to:
            logger.info(f"生成执行失败表格中{os.path.join(self.path, '执行失败.xlsx')}")
            df.to_excel(
                os.path.join(self.path, f'执行失败-{time.strftime("%Y-%m-%d %H时%M分%S秒", time.localtime())}.xlsx'),
                index=False)
            return
        logger.info(f"执行成功")

    def submit(self):
        if self.province == '浙江省':
            self.win.ButtonControl(Name='提交').Click()
        else:
            self.win.TextControl(Name='提交').Click()
        # 点击确定
        node = self.is_node('确定', 'ButtonControl', 10)
        if not node.Exists():
            raise Exception("案件提交失败，点击提交后未确认提交按钮，请确认数据是否正确")

        node.Click()
        for i in range(60):
            node = self.win.TextControl(Name="立案申请信息")
            if not node.Exists():
                return True
            time.sleep(1)
        raise Exception('案件已暂存,提交失败,请检查')

    def out(self):
        for c, d in uiautomation.WalkControl(self.win):
            if c.Name == '后退' or c.Name == "主页":
                c.Click()
                self.out()
                break
        return

    def out_wx(self):
        try:
            self.win.ButtonControl(Name="关闭").Click()
            time.sleep(3)
        except:
            self.win.ButtonControl(Name="关闭").Click()
            time.sleep(3)

    @unit_testing
    def main(self, i):
        logger.info("正在处理运行数据")
        self.data_processing()
        logger.info(f"我要立案,进入网上立案{self.register()}")
        logger.info(f"选择法院:{self.court_choice()}")
        logger.info(f"立案须知:{self.txt_define()}")
        logger.info(f"上传资料:{self.upload()}")
        logger.info(f"资料补全:{self.data_check()}")
        return

    def open_wx(self):
        """打开微信小程序"""
        path = fr"WechatAppLauncher.exe -launch_appid={OPTIONS.get(self.province)}"
        # path = fr"D:\Program Files (x86)\Tencent\WeChat\WechatAppLauncher.exe -launch_appid={OPTIONS.get(self.province)}"
        print(path)
        os.system(path)
        time.sleep(3)  # 等待小程序打开
        assert self.is_open(), "打开微信小程序失败"

    def dsh(self, now_time, let, top, right, button):
        self.win.TextControl(Name="待审核").Click()
        # self.win.TextControl(Name="审核通过").Click()
        time.sleep(2)
        logger.info('------------------------->开始截第一张图！')
        img = ImageGrab.grab()
        jpg_name = f'待审核-{now_time}.jpg'
        jpg_num = 1
        while True:
            if jpg_name not in os.listdir(self.tjz_path):
                break
            jpg_name = jpg_name.split(f"{now_time}")[0] + f"{now_time}-" + f"{jpg_num}.jpg"
            jpg_num += 1
        jpg_path = os.path.join(self.tjz_path, jpg_name)
        img.save(jpg_path)
        # 剪切图片成对应比例
        img_one = Image.open(jpg_path)
        img_ones = img_one.crop((let, top, right, button))
        # 截取成功并保存到本地
        img_ones.save(jpg_path)
        self.win.TextControl(Name=f'{self.row["申请人单位"]}诉{self.row["被申请人姓名"]}一案').Click()
        # self.win.TextControl(Name=f'湖南磊实企业咨询管理有限公司诉林燕君一案').Click()
        while True:
            # 获取立案法院内容判断是否加载出来
            if self.win.TextControl(Name=f'立案法院').GetParentControl().GetParentControl().GetChildren()[
                        2].GetChildren()[0].Name == self.row["申请法院"]:
                break
        logger.info('------------------------->开始截第二张图！')
        img1 = ImageGrab.grab()
        jpg_name1 = self.row["被申请人姓名"] + self.row["被申请人证件号"] + ".jpg"
        jpg_path1 = os.path.join(self.dsh_path, jpg_name1)
        img1.save(jpg_path1)
        # 剪切图片成对应比例
        img_two = Image.open(jpg_path1)
        img_twos = img_two.crop((let, top, right, button))
        # 截取成功并保存到本地
        img_twos.save(jpg_path1)
        self.out()

    def screenshots(self):
        try:
            logger.info("进入截图函数！！！！")
            """ 截图保存 """
            if self.win.Name == "人民法院在线服务浙江":
                self.win.TextControl(Name="在线立案").Click()
            else:
                self.win.TextControl(Name="我要立案").Click()
            while True:
                try:
                    self.win.ButtonControl(Name="审判立案").Click()
                except:
                    print(11)
                    continue
                break
            try:
                # 部分情况下没有不愿意按钮 超时跳过
                self.win.TextControl(Name="不愿意").Click()
            except Exception as e:
                print(e)
            logger.info("获取当前日期！！！！")
            now_time = datetime.date.today()
            if self.province == "浙江省":
                logger.info("当前案件为浙江的案件！！！")
                self.win.TextControl(Name="您可通过案件名称查询").Click()
                uiautomation.SetClipboardText(f'{self.row["申请人单位"]}诉{self.row["被申请人姓名"]}一案')
                # uiautomation.SetClipboardText(f'名称暂无')
                pyautogui.hotkey('ctrl', 'v')
                self.win.TextControl(Name="筛选").GetParentControl().GetParentControl().GetChildren()[0].GetChildren()[
                    0].Click()
                # 当前案件类型
                an_type = self.win.TextControl(
                    Name="筛选").GetParentControl().GetParentControl().GetParentControl().GetChildren()[
                    2].GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[8].GetChildren()[0]
                # 获取小程序的页面大小
                area = self.win.TextControl(Name="筛选").GetParentControl().GetParentControl().GetParentControl()
                position = area.Element.CurrentBoundingRectangle
                let, top, right, button = position.left, position.top, position.right, position.bottom
                # 截第一张图
                logger.info("------------------------->开始截第一张图！")
                img = ImageGrab.grab()
                jpg_name = f'{an_type.Name}-{now_time}.jpg'
                # jpg_num 记录当前文件夹中是否已经存在同名的文件，如果有就在文件名后缀添加数字进行区分
                jpg_num = 1
                while True:
                    if jpg_name not in os.listdir(self.tjz_path):
                        break
                    jpg_name = jpg_name.split(f"{now_time}")[0] + f"{now_time}-" + f"{jpg_num}.jpg"
                    jpg_num += 1
                jpg_path = os.path.join(self.tjz_path, jpg_name)
                img.save(jpg_path)
                # 剪切图片成对应比例
                imgs = Image.open(jpg_path)
                imgE = imgs.crop((let, top, right, button))
                # 截取成功并保存到本地
                imgE.save(jpg_path)
                # 点进该案件
                an_type.Click()
                while True:
                    # 获取立案法院内容判断是否加载出来
                    if self.win.TextControl(Name=f'立案法院').GetParentControl().GetParentControl().GetChildren()[
                        2].GetChildren()[0].Name == self.row["申请法院"]:
                        break
                # 截第二张图
                logger.info('------------------------->开始截第二张图！')
                img1 = ImageGrab.grab()
                jpg_name1 = self.row["被申请人姓名"] + self.row["被申请人证件号"] + ".jpg"
                jpg_path1 = os.path.join(self.dsh_path, jpg_name1)
                img1.save(jpg_path1)
                # 剪切图片成对应比例
                img1s = Image.open(jpg_path1)
                img1E = img1s.crop((let, top, right, button))
                # 截取成功并保存到本地
                img1E.save(jpg_path1)
                self.out()
                return '截图成功'
            logger.info("当前案件为其他省份的案件！！！")
            self.win.TextControl(Name="提交中").Click()
            # 获取小程序窗口大小
            area = self.win.TextControl(
                Name="提交中").GetParentControl().GetParentControl().GetParentControl().GetParentControl()
            position = area.Element.CurrentBoundingRectangle
            let, top, right, button = position.left, position.top, position.right, position.bottom
            time.sleep(3)
            if len(self.win.TextControl(
                    Name="全部").GetParentControl().GetParentControl().GetParentControl().GetParentControl().GetChildren()[
                       1].GetChildren()[0].GetChildren()[0].GetChildren()) != 0:
                logger.info("当前微信没有提交中的案件！！！")
                # 起诉对象
                qs_name = self.win.TextControl(
                    Name="全部").GetParentControl().GetParentControl().GetParentControl().GetParentControl().GetChildren()[
                    1].GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[0].Name
                # 起诉时间
                qs_time = self.win.TextControl(
                    Name="全部").GetParentControl().GetParentControl().GetParentControl().GetParentControl().GetChildren()[
                    1].GetChildren()[0].GetChildren()[0].GetChildren()[5].GetChildren()[0].Name
                # 判断是否为当前账号
                if f'{self.row["申请人单位"]}诉{self.row["被申请人姓名"]}一案' == qs_name and str(now_time) == qs_time:
                    # if f'{self.row["申请人单位"]}诉{self.row["被申请人姓名"]}一案' == qs_name and '2023-07-06' == qs_time:
                    logger.info('------------------------->开始截第一张图！')
                    # 截第一张图
                    img = ImageGrab.grab()
                    jpg_name = f'提交中-{now_time}.jpg'
                    # jpg_num 记录当前文件夹中是否已经存在同名的文件，如果有就在文件名后缀添加数字进行区分
                    jpg_num = 1
                    while True:
                        if jpg_name not in os.listdir(self.tjz_path):
                            break
                        jpg_name = jpg_name.split(f"{now_time}")[0] + f"{now_time}-" + f"{jpg_num}.jpg"
                        jpg_num += 1
                    jpg_path = os.path.join(self.tjz_path, jpg_name)
                    img.save(jpg_path)
                    # 剪切图片成对应比例
                    img_one = Image.open(jpg_path)
                    img_ones = img_one.crop((let, top, right, button))
                    # 截取成功并保存到本地
                    img_ones.save(jpg_path)
                    # 点入查看详细信息
                    self.win.TextControl(Name=f'{self.row["申请人单位"]}诉{self.row["被申请人姓名"]}一案').Click()
                    while True:
                        # 获取立案法院内容判断是否加载出来
                        if self.win.TextControl(Name=f'立案法院').GetParentControl().GetParentControl().GetChildren()[
                            2].GetChildren()[0].Name == self.row["申请法院"]:
                            break
                    # 截第二张图
                    logger.info('------------------------->开始截第二张图！')
                    img1 = ImageGrab.grab()
                    jpg_name1 = self.row["被申请人姓名"] + self.row["被申请人证件号"] + ".jpg"
                    jpg_path1 = os.path.join(self.dsh_path, jpg_name1)
                    img1.save(jpg_path1)
                    # 剪切图片成对应比例
                    img_two = Image.open(jpg_path1)
                    img_twos = img_two.crop((let, top, right, button))
                    # 截取成功并保存到本地
                    img_twos.save(jpg_path1)
                    self.out()
                    return '截图成功'
                else:
                    logger.info("当前案件在待审核类型中!!!!")
                    self.dsh(now_time, let, top, right, button)
                return '截图成功'
            else:
                logger.info("当前案件在待审核类型中")
                self.dsh(now_time, let, top, right, button)
                return '截图成功'
        except Exception as e:
            logger.error(str(e), e.__traceback__.tb_lineno)
            return '截图失败'

    def run(self):
        logger.info(self.form_data)
        self.path = self.form_data.get("excel_path")
        self.path = self.form_data.get("excel_path").replace("/", "\\")
        self.dir_path = self.form_data.get("dir_path").replace("/", "\\")
        # 读取表格
        self.data = self.read_excel()
        logger.info(f"任务量{len(self.data)}")
        # 循环处理任务
        old_province = ""
        # 循环次数
        num = 0
        for i in self.data.index:
            num += 1
            try:
                self.row = self.data.loc[i].to_dict()
                logger.info(f"行号：{self.row['行号']} 开始运行")
                if self.row["执行状态"] == "执行成功": continue
                self.province = self.row["申请所在省份"]
                self.open_wx()
                if num != 1:
                    if old_province != self.province:
                        logger.info("新地区，关闭原来的微法院，等待2秒打开新地区微法院！")
                        self.out_wx()
                        time.sleep(2)
                        self.open_wx()
                old_province = self.province
                # 打开小程序
                self.main(i, fun=self.out)
                # 提交不要参与重试 避免重复提交
                # logger.info(f"提交:{self.submit()}")
                time.sleep(2)
                self.out()
                photo_type = ''
                for error_num in range(3):
                    logger.info(f"开始第{error_num}执行截图函数！！！！")
                    photo_type = self.screenshots()
                    if photo_type == "截图成功": break
                    self.out()
                    time.sleep(2)

                self.data.loc[i]['执行状态'] = "执行成功"
                self.data.loc[i]['错误原因'] = ''
                self.data.loc[i]['执行截图状态'] = photo_type
            except Exception as e:
                logger.error(e, exc_info=True)
                self.data.loc[i]['执行状态'] = "执行失败"
                self.data.loc[i]['错误原因'] = str(e)
                self.data.loc[i]['执行截图状态'] = "截图失败"
                self.out_wx()
            finally:
                tablesheet.sheet.add_row(self.data.loc[i].to_dict())
            # 写入结果
            logger.info(f'{self.data.loc[i]["行号"]} 运行结束')
            df = self.data.drop('行号', axis=1)
            df.to_excel(self.path, index=False)

            # # 重新启动微信小程序
            # if self.data.loc[i]['执行状态'] == "执行失败":
            #     os.system('taskkill /f /im WeChatAppEx.exe')
            #     self.open_wx()

    def clear(self):
        print("destory")

    class Meta:
        id = "com.hanzi.wfy.spla"
        name = "微法院-审判立案"
        version = "1.7.0"
        type = JobType.MANUAL
        form = []
        group = "微法院"
        description = ""
        arguments = [
            FileItem(title="excel表格 rpa会直接将结果写入运行表格,建议自行做好备份", name="excel_path"),
            DirectoryItem(title="文件目录", name="dir_path"),
            SelectItem(title="请选择代理人", name="type_", options=['执业律师', '当事人的近亲属或工作人员']),
            SelectItem(title='是否上传支付令', name='derail', options=['是', '否']),
            SelectItem(title='案件类型', name='case_type', options=['民事一审', '诉前调解']),
            SelectItem(title='送达地址确认书上传方式', name='download_way', options=['引入', '本地上传']),
            SelectItem(title='收款账户确认书上传方式', name='download_paper', options=['引入', '本地上传', "不上传"]),
            DirectoryItem(title="提交中保存目录", name="tjz_path"),
            DirectoryItem(title="待审核保存目录", name="dsh_path"),
        ]


if __name__ == '__main__':
    excel = r"C:\Users\9000\Desktop\新建文件夹 (2)\审判立案测试-2个律师代理人(1).xlsx"
    path = r"C:\Users\9000\Desktop\新建文件夹 (2)\微法院-收款账号确认老命名资料"
    tjz_path = r'C:\Users\9000\Desktop\新建文件夹 (2)\out\提交中目录'
    dsh_path = r'C:\Users\9000\Desktop\新建文件夹 (2)\out\待审核目录'
    a = TaskInfo()
    a.formData = {"excel_path": excel, "dir_path": path, "tjz_path": tjz_path, 'dsh_path': dsh_path,
                  'type_': '执业律师',
                  'derail': '是', 'case_type': '民事一审', 'download_way': "本地上传", "download_paper": "引入"}
    x = Program(a).run()
    print(x)
