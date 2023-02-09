import json
import os
import time
import random
from openpyxl import Workbook
import dataclasses_json.mm
from runtime.m import ensure,record_state
import requests
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from flows.flow import FileItem, ListDataFlow, ScriptDef, StringItem, DirectoryItem, UserSelectItem

from rpalib.log import logger
from rpalib import excel
from selenium.webdriver.common.by import By

global g_header, g_driver, g_username, g_pwd

# # 点击
def click(driver, xpath, text=''):
    btn = WebDriverWait(driver, 30).until(lambda el: driver.find_element_by_xpath(xpath))
    btn.click()
    logger.info('点击按钮:' + text)
    time.sleep(2)


# 填写输入框
def fill_input(driver, xpath, value, input_name):
    input = WebDriverWait(driver, 30).until(lambda el: driver.find_element_by_xpath(xpath))
    input.send_keys(value)
    logger.info('输入框:' + input_name + ',输入值:' + str(value))
    time.sleep(1)


#
#
# 检测文件是否存在
def check_file(item, attach_dir, file_format):
    bqsqs = os.path.join(attach_dir, "诉前保全申请书", item.respondent_name + "-" + item.respondent_cert_no + "-保全申请书.pdf")
    if not os.path.exists(bqsqs):
        bqsqs = os.path.join(attach_dir, "诉前保全申请书", item.respondent_name + "-" + item.respondent_cert_no + "-保全申请书.jpg")
    ygzl = os.path.join(attach_dir, "申请人资料", "原告资料.pdf")
    if item.agent_name:
        if not check_img_file(os.path.join(attach_dir, "代理人资料"), f"{item.agent_name}_代理人", attach_dir):
            logger.info(f"原告代理人文件不存在:{item.agent_name}")
            return False

    jkxy = os.path.join(attach_dir, "被申请人资料", item.respondent_name + item.respondent_cert_no,
                        item.respondent_name + "-" + item.respondent_cert_no + "-" + item.app_id + f"-{file_format}.pdf")
    file_parent_path = os.path.join(attach_dir, "被申请人资料", item.respondent_name + item.respondent_cert_no)
    id_pic_front = f"{item.respondent_name}-{item.respondent_cert_no}-被告身份证正面"
    id_pic_back = f"{item.respondent_name}-{item.respondent_cert_no}-被告身份证反面"
    id_pic = f"{item.respondent_name}-{item.respondent_cert_no}-被告身份证"
    if check_single_file(bqsqs, attach_dir) \
            and check_single_file(ygzl, attach_dir) \
            and check_single_file(jkxy, attach_dir):
        if check_img_file(file_parent_path, id_pic_front, attach_dir) \
                and check_img_file(file_parent_path, id_pic_back, attach_dir):
            return True
        elif check_img_file(file_parent_path, id_pic, attach_dir):
            return True
        else:
            file = os.path.join(file_parent_path, f"{id_pic}")
            logger.info("文件不存在:" + file)
    return False


def check_single_file(file_full_path, attach_dir):
    if os.path.exists(file_full_path):
        return True
    logger.info("文件不存在:" + file_full_path)
    return False


def check_img_file(file_parent, file_name, attach_dir):
    file = os.path.join(file_parent, f"{file_name}")
    for suffix in ["jpg", "jpeg", "png", "pdf"]:
        full_path = os.path.join(file + f".{suffix}")
        if os.path.exists(full_path):
            return True
    return False


class BaoQuanItem(object):
    # '进件号'
    app_id: str
    # 申请人单位
    spv_name: str
    # 申请人信用代码
    spv_cert_no: str
    # 申请人法定人
    spv_legal: str
    # 申请人手机号
    spv_phone: str
    # 申请人单位地址
    spv_address: str

    # 代理人姓名
    agent_name: str
    # 代理人证件号
    agent_cert_no: str
    # 代理人手机号
    agent_phone: str
    # 代理人执行号
    agent_work_no: str
    # 代理人律所
    agent_company: str

    # 被申请人姓名
    respondent_name: str
    # 被申请人证件号
    respondent_cert_no: str
    # 被申请人手机号
    respondent_phone: str
    # 被申请人地址
    respondent_address: str

    # 申请法院
    court: str
    # 保险公司
    insurance: str
    # 财产价值
    property_value: float
    # 申请保全金额
    amount: float
    # 描述
    description: str
    # 咨询员编号d
    consultant_number: str
    # 提交人身份
    submitter: str
    # requests header
    header: dict
    # cookie bearer


    def __str__(self) -> str:
        return f"{self.app_id}-{self.respondent_cert_no}"


class DoBaoQuanJob(object):
    def __init__(self, driver: WebDriver, attach_dir: str, item: BaoQuanItem, file_format) -> None:
        super().__init__()
        self.driver = driver
        self.attach_dir = attach_dir
        self.item = item
        self.file_format = file_format


    def request(self, url, method="get", data=None):
        for i in range(20):
            try:
                if method == "post":
                    r = requests.session().post(url, headers=g_header, json=data, timeout=60)
                    break
                else:
                    r = requests.session().get(url, headers=g_header, timeout=60)
                    break
            except:
                continue
        return r

    # 担保
    def danbao(self, court, insurance, money):
        # 获得法院ID
        url_court_id = f"https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsqs/xzfy?time={int(round(time.time() * 1000))}&mklx=1"
        court_data = json.loads(self.request(url_court_id).text)
        for x in court_data.get("data")[0].get("children"):
            for i in x.get("children"):
                for y in i.get("children"):
                    if y.get("name") == court:
                        self.court_id = y.get("id")
                        break
        url_create_baoquan = r"https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsq"
        data_bqsq = \
            {"cBqlb": "1",
             "cBqlx": "1",
             "cDbqk": "1",
             "cFsqj": "1",
             "cTjrlx": "3",  # 律师:1 其他代理人:3
             "nSqbqdcsfy": "40",
             "nSqbqje": f"{money}",
             "nSqfy": self.court_id,
             "nSqfymc": court,
             "time": f"{int(time.time() * 1000)}"}
        if self.item.submitter == '律师':
            data_bqsq["cTjrlx"] = "1"
        else:
            data_bqsq["cTjrlx"] = "3"
        r = self.request(url_create_baoquan, "post", data=data_bqsq)
        self.bqid = json.loads(r.text).get("data")

    # 添加申请人
    def proposer(self, unit, code, legal, phone, address):
        # 男1 女2
        # 身份证1 护照2 户口簿6
        # 汉1
        # 机关1 事业2 企业3 社会4 民办5
        # 营业执照1 组织2 事业3 统一4
        data = [{
            "cDwxz": "3",
            "cEmail": "",
            "cGh": "",
            "cGh1": "",
            "cGh2": "",
            "cGh3": "",
            "cId": self.bqid,
            "cPhoneno": phone,
            "cQyfr": legal,
            "cQymc": unit,
            "cQyzch": "",
            "cQyzzjgdm": code,
            "cSqrlx": "2",  # 法人
            "cSqrxb": None,
            "cSqrxm": "",
            "cTxdz": address,
            "cZjh": "",
            "cZjlx": "7",
            "dtSqrBirthday": "",
            "nMz": None,
            "nNl": None,
            "nZzlx": 4,  # 证照类型
        }]
        return data

    # 添加被申请人
    def respondent(self, byName, byIdCode, byPhone, byAddress):
        byIdCode = str(byIdCode)
        birth_day = f"{byIdCode[6:14][0:4]}-{byIdCode[6:14][4:6]}-{byIdCode[6:14][6:]}"
        data = [{
            'cBqDsrid': self.bqid,
            'cCzdz': "",
            'cDsrlx': "1",  # 证件类型 身份证1
            'cDsrxb': "1" if int(byIdCode[-2]) % 2 != 0 else "2",  # 性别类型 男1
            'cDsrxm': byName,
            'cDwdz': "",
            'cDwxz': "",
            'cGh': "",
            'cGh1': "",
            'cGh2': "",
            'cGh3': "",
            'cPhoneno': "",
            'cPhoneno_no': "",
            'cQyfr': "",
            'cQymc': "",
            'cQyzcdjh': "",
            'cTxdz': byAddress,
            'cTxdz_no': byAddress,
            'cZjh': byIdCode,
            'cZjh_no': byIdCode,
            'cZjlx': "1",  # 证件类型
            'cZzjgdm': "",
            'dtDsrbirthday': birth_day,
            'nMz': 1,
            'nNl': time.localtime().tm_year - int(birth_day.split('-')[0]),
        }]
        if byPhone != None and byPhone != '':
            data[0]["cPhoneno"] = byPhone
            data[0]["cPhoneno_no"] = byPhone
        return data

    # 原告代理人
    def add_agent(self):
        item = self.item
        if item.agent_name is None:
            return
        data = [{
            "cBqSqrids": [self.bqid],
            "cDlrlx": "3",  # 代理人类型律师1 近亲属或工作人员3
            "cDlrszls": item.agent_company,
            "cDlrxb": "1" if int(str(item.agent_cert_no)[-2]) % 2 != 0 else "2",  # 性别男1
            "cDlrxm": item.agent_name,
            "cDlrzjh": item.agent_cert_no,
            "cDlrzjhm": item.agent_work_no,
            "cDlrzjlx": "1",  # 证件类型身份证1
            "cGddh": "",
            "cGddh1": "",
            "cGddh2": "",
            "cGddh3": "",
            "cPhone": item.agent_phone,
        }]
        # print(data)
        # exit()
        if self.item.submitter == '工作人员':
            data[0]["cDlrzjhm"] = ""
            data[0]["cDlrszls"] = ""
        return data

    # 添加财产线索
    def property(self, ccName, describe, cost):
        cSqbqccjeTS = ''
        for x, i in enumerate(range(0, len(str(cost)))):
            cSqbqccjeTS += str(cost)[len(str(cost)) - i - 1]
            if ((x + 1) % 3) == 0:
                cSqbqccjeTS += ','
        cSqbqccjeTS = cSqbqccjeTS[::-1] if cSqbqccjeTS[-1] != ',' else cSqbqccjeTS[::-1][1:]
        data = [{
            "cCclx": "255",  # 财产类型其他255
            "cCclxccxx": "",
            "cCclxcllx": "",
            "cCclxfcdz": "",
            "cCclxfczh": "",
            "cCclxtddcqzh": "",
            "cCclxtdddz": "",
            "cCclxtdmj": "",
            "cCclxzbz": "",
            "cCclxzclpp": "",
            "cCclxzgpdcgsl": "",
            "cCclxzgpdgpmc": "",
            "cCclxzgqdcggs": "",
            "cCclxzgqdczbl": "",
            "cCclxzgqdgsxx": "",
            "cCclxzjjdjjmc": "",
            "cCclxzjjdjjsl": "",
            "cCclxzswdtszh": "",
            "cCclxzzwdzqmc": "",
            "cCclxzzwdzqmz": "",
            "cCclxzzwdzqmzTS": "",
            "cCklxzcldcph": "",
            "cGsd": "",
            "cKhhmc": "",
            "cMs": describe,
            "cSbmc": "",
            "cSqbqccje": cost,
            "cSqbqccjeTS": cSqbqccjeTS,
            "cSqbqccyyz": self.bqid,
            "cXjzje": "",
            "cXjzjeTS": "",
            "cYhckzckdw": "",
            "cYhckzckje": "",
            "cYhckzckjeTS": "",
            "cYhckzkhzh": "",
        }]
        return data

    def basic_baoquan(self):
        # 保全基本信息
        ret1 = self.proposer(self.item.spv_name, self.item.spv_cert_no, self.item.spv_legal, self.item.spv_phone,
                             self.item.spv_address)
        ret2 = self.respondent(self.item.respondent_name, self.item.respondent_cert_no, self.item.respondent_phone,
                               self.item.respondent_address)
        ret3 = self.add_agent()
        ret4 = self.property(self.item.respondent_name, self.item.description, self.item.property_value)
        url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsqinfo?time={int(round(time.time() * 1000))}&bqid={self.bqid}'
        ret = json.loads(requests.get(url, headers=self.item.header).text).get("data")
        data = {
            "bqDsrs": ret2,
            "bqJbxx": ret,
            "bqProperties": ret4,
            "bqSqrs": ret1,
            "tBqDlrs": ret3,
            "ccxsId": [],
            "dsrIds": [],
            "sqrIds": [],
            "xwxxIds": [],
            "xwxxs": [],
            "ygdlrIds": [],
            "zjxxIds": [],
            "zjxxs": [],
        }
        url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsq/tempsave?time={int(round(time.time() * 1000))}&bqid={self.bqid}'
        r = self.request(url, method="post", data=data)
        if str(r.status_code) == "200":
            logger.info(f"{self.item.respondent_name}保全基本信息保存完成")

    # 创建担保申请
    def danbao_create(self, insurance, consultant_number):
        # 保险公司code
        url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/commoncodepz?time={int(round(time.time() * 1000))}&cPid=127000'
        commoncode = json.loads(self.request(url).text).get('data')
        for i in commoncode:
            if i.get('cName') == insurance:
                # if i.get('cName') == "中国大地财产保险股份有限公司":
                cCode = i.get('cCode')
                break
        url_dbid = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/ssdb/sqdbxx?time={int(round(time.time() * 1000))}&bqid={self.bqid}'
        url_get_fl = f'https://baoquan.court.gov.cn/wsbq/commonapi/api/policy/premium?time={int(round(time.time() * 1000))}&preserveAmount=' \
                     f'{self.item.property_value}&institution={cCode}&corpId={self.court_id}'
        data2 = {"preserveAmount": self.item.property_value, "institution": cCode, "corpId": self.court_id}
        r = json.loads(self.request(url_get_fl, "post", data=data2).text).get("data")
        data1 = {
            "cBqlb": "1",  # 保全类型 财产保全
            "cBqlx": "1",  # 保全类别 诉前保全
            "cBxgs": cCode,
            "cClerkNo": consultant_number,
            "cFl": r.get("minRate"),
            "cFsqj": "1",
            "cFyid": self.court_id,
            "cFymc": self.item.court,
            "cMaxfl": r.get("maxRate"),
            "cTjrlx": "3",  # 提交人类型 其他人
            "nDbfy": r.get("maxAmount"),
            "nMaxdbfy": r.get("minAmount"),
            "nSqbqje": f"{self.item.property_value}",
        }
        self.dbid = json.loads(self.request(url_dbid, "post", data=data1).text).get("data")

    def upload(self, file_name, file_full_path, type):
        dbid = self.dbid


        res = dataclasses_json.mm.JsonData



        if type == 1:
            cllx = '1'
            id_ = ''
        elif type == 2:
            cllx = '2'
            id_ = ''
        elif type == 3:
            cllx = '3'
            id_ = str(int(dbid) + 1)
        elif type == 4:
            cllx = '3'
            id_ = str(int(dbid) + 2)
        elif type == 5:
            cllx = '3'
            id_ = str(int(dbid) + 3)
        elif type == 6:
            cllx = '5'
            id_ = ''

        clid = str(time.time()).replace('.', '')
        clid = clid[0:-2] + '.' + clid[-2:]
        # full_name = os.path.join(filepath)
        files = {'files': (file_name, open(os.path.join(file_full_path), 'rb'))}
        url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/ssdb/fileupload?time={int(round(time.time() * 1000))}'
        data = {'cllx': cllx, "dbid": dbid, "clid": clid, "id": id_}
        for i in range(10):
            try:
                requests.post(url, headers=self.item.header, params=data, files=files, timeout=60)
                logger.info(f"{file_name}上传完成")
                break
            except Exception as e:
                logger.info(f"{file_name}上传超时。。重试  error:{e}")

    def choice_img_file(self, file_parent, file_name):
        for suffix in ["jpg", "jpeg", "png", "pdf"]:
            full_path = os.path.join(file_parent, f"{file_name}.{suffix}")
            if os.path.exists(full_path):
                return full_path, f"{file_name}.{suffix}"
        raise Exception(f"文件{file_name}不存在")

    # 上传保全申请书
    def proposer_save(self):
        filename = f"{self.item.respondent_name}-{self.item.respondent_cert_no}-保全申请书.pdf"
        file_full_path = os.path.join(self.attach_dir, "诉前保全申请书", filename)
        if not os.path.exists(file_full_path):
            filename = f"{self.item.respondent_name}-{self.item.respondent_cert_no}-保全申请书.jpg"
            file_full_path = os.path.join(self.attach_dir, "诉前保全申请书", filename)
        self.upload(filename, file_full_path, 1)
        logger.info(f"{self.item.app_id}上传保全申请书上传成功")

    # 起诉状
    def complaint_save(self):
        filename = f"{self.item.respondent_name}-{self.item.app_id}-起诉状.pdf"
        file_full_path = os.path.join(self.attach_dir, "起诉状", filename)
        if os.path.exists(file_full_path):
            self.upload(filename, file_full_path, 2)
            logger.info("上传起诉状:" + file_full_path)
            return
        logger.info("未找到起诉状:" + file_full_path + ",跳过本步骤")

    # 上传申请人资料
    def proposer_data(self, path):
        file_full_path = os.path.join(path, "申请人资料", "原告资料.pdf")
        self.upload("原告资料.pdf", file_full_path, 3)
        logger.info("原告法人身份证上传成功")

    def proposer_card(self, path, code, jname):
        file_parent_path = os.path.join(path, "被申请人资料", jname + self.item.respondent_cert_no)
        id_pic = f"{jname}-{self.item.respondent_cert_no}-被告身份证"
        if check_img_file(file_parent_path, id_pic, file_parent_path):
            full_path, filename = self.choice_img_file(file_parent_path,
                                                       f"{jname}-{self.item.respondent_cert_no}-被告身份证")
            self.upload(filename, full_path, 4)
            return
        # 被告身份证正面
        full_path, filename = self.choice_img_file(file_parent_path, f"{jname}-{self.item.respondent_cert_no}-被告身份证正面")
        self.upload(filename, full_path, 4)
        logger.info(f"{self.item.app_id}被告身份证正面上传成功")
        # 被告身份证反面
        full_path, filename = self.choice_img_file(file_parent_path, f"{jname}-{self.item.respondent_cert_no}-被告身份证反面")
        self.upload(filename, full_path, 4)
        logger.info(f"{self.item.app_id}被告身份证反面上传成功")

    # 原告代理人
    def proposer_agency(self, path, agent_name):
        if agent_name is None:
            return
        file_parent_path = os.path.join(path, "代理人资料")
        logger.info("原告代理人")
        full_path, filename = self.choice_img_file(file_parent_path, f"{agent_name}_代理人")
        self.upload(filename, full_path, 5)
        logger.info(f"{self.item.app_id}代理人上传成功")

    # 上传证据材料
    def evidence(self, path, code, jname):
        file_full_path = os.path.join(path, "被申请人资料", jname + self.item.respondent_cert_no,
                                      f"{jname}-{self.item.respondent_cert_no}-{code}-{self.file_format}.pdf")
        self.upload(f"{jname}-{self.item.respondent_cert_no}-{code}-{self.file_format}.pdf", file_full_path, 6)
        logger.info(f"{self.item.app_id}{self.file_format}上传成功")


    def submit(self):
        data = {"jbxxid": self.dbid}
        url = f'https://baoquan.court.gov.cn/wsbq/commonapi/api/policy/guarantee/apply?time={int(round(time.time() * 1000))}&jbxxid={self.dbid}'
        r = self.request(url, 'post', data).text
        message = json.loads(r).get('message')
        if message == "担保申请成功":
            logger.info(f"{self.item.app_id}担保申请成功")
        else:
            logger.error(f"{self.item.app_id}担保申请失败: {r}")

    def next(self):
        s = time.time()
        while True:
            self.driver.get("https://baoquan.court.gov.cn/#/myApplication")
            time.sleep(5)
            sel_show = self.driver.find_elements(By.XPATH, value='//*[@id="myApplication"]/div[2]/div[1]/div[1]/button')
            if len(sel_show) > 0:
                return
            if time.time() - s > 30:
                raise Exception("页面刷新失败")
            time.sleep(1)

    def run(self):
        for x in range(3):
            try:
                self.danbao(self.item.court, self.item.insurance, self.item.amount)
                time.sleep(random.randint(2, 5))
                self.basic_baoquan()
                time.sleep(random.randint(2, 5))
                self.danbao_create(self.item.insurance, self.item.consultant_number)
                time.sleep(random.randint(2, 5))
                self.proposer_save()
                time.sleep(random.randint(2, 5))
                self.complaint_save()
                time.sleep(random.randint(2, 5))
                self.proposer_data(self.attach_dir)
                time.sleep(random.randint(2, 5))
                self.proposer_card(self.attach_dir, self.item.app_id, self.item.respondent_name)
                time.sleep(random.randint(2, 5))
                self.proposer_agency(self.attach_dir, self.item.agent_name)
                time.sleep(random.randint(2, 5))
                self.evidence(self.attach_dir, self.item.app_id, self.item.respondent_name)
                time.sleep(random.randint(2, 5))
                # self.submit()
                # time.sleep(3)
                break
            except:
                print("上传资料错误")
                url = rf'https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsqs?time={int(time.time() * 1000)}&rows=5&page=1&selectValue=sqrxm&searchValue='
                response = requests.get(url=url, headers=self.item.header).json()
                # print(response)
                try:
                    if response["data"] != None or response["data"] != '':
                        attempt(self.item.respondent_name)

                except:
                    time.sleep(3)
                    g_driver.quit()
                    login()
                    attempt(self.item.respondent_name)

                if x == 2:
                    logger.error(f"姓名：{self.item.respondent_name}证件号：{self.item.respondent_cert_no}---因失败次数过多，需要人工干预！")
                    raise ValueError(f"姓名：{self.item.respondent_name}证件号：{self.item.respondent_cert_no}---因失败次数过多，需要人工干预！")




def attempt(g_name):
    url = rf'https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsqs?time={int(time.time() * 1000)}&rows=5&page=1&selectValue=sqrxm&searchValue='
    response = requests.get(url=url, headers=g_header).json()
    # print(response)
    url2 = rf"https://baoquan.court.gov.cn/wsbq/ssbq/api/ssdb/dbsqs?time={int(time.time() * 1000)}&rows=5&page=1&selectValue=sqrxm&searchValue="
    response2 = requests.get(url=url2, headers=g_header).json()
    # print(response2)


    for i in response['data']['list']:
        types = i['cBqzt']
        name = i['cDsrxm']
        cid = i['cId']


        if types == '1' and name == g_name:
            urls = rf'https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsq/logic?time={int(time.time() * 1000)}&id={cid}'
            responses = requests.delete(url=urls, headers=g_header)
            print('保全已删除')

    for i in response2['data']['list']:
        types2 = i['cDbzt']
        name2 = i['cDsrxm']
        cid2 = i['cId']
        if types2 == '1' and name2 == g_name:
            urls2 = rf'https://baoquan.court.gov.cn/wsbq/ssbq/api/ssdb/dbsq?time={int(time.time() * 1000)}&dbid={cid2}'

            responses2 = requests.delete(url=urls2, headers=g_header)
            print('担保已删除')



class XJFYBaoQuanFlow(ListDataFlow):

    def __init__(self, excel_file, attach_dir, username, password, file_format) -> None:
        super().__init__()
        self.excel_file = excel_file
        self.attach_dir = attach_dir
        self.file_format = file_format
        global g_username, g_pwd

        g_username = username
        g_pwd = password

    def precheck(self):
        self.load_list()

    def load_list(self):
        login()
        items = excel.loads(
            self.excel_file, BaoQuanItem, {
                "app_id": {"title": "进件号", "required": True},
                "spv_name": {"title": "申请人单位", "required": True},
                "spv_cert_no": {"title": "申请人信用代码", "required": True},
                "spv_legal": {"title": "申请人法定人", "required": True},
                "spv_phone": {"title": "申请人手机号", "required": True},
                "spv_address": {"title": "申请人单位地址", "required": True},
                "agent_name": {"title": "代理人姓名", "required": False},
                "agent_cert_no": {"title": "代理人证件号", "required": False},
                "agent_phone": {"title": "代理人手机号", "required": False},
                "agent_work_no": {"title": "代理人执行号", "required": False, "default": ""},
                "agent_company": {"title": "代理人律所", "required": False},
                "respondent_name": {"title": "被申请人姓名", "required": True},
                "respondent_cert_no": {"title": "被申请人证件号", "required": True},
                "respondent_phone": {"title": "被申请人手机号", "required": False},
                "respondent_address": {"title": "被申请人地址", "required": True},
                "court": {"title": "申请法院", "required": True},
                "insurance": {"title": "保险公司", "required": True},
                "property_value": {"title": "财产价值", "required": True},
                "amount": {"title": "申请保全金额", "required": True},
                "description": {"title": "描述", "required": True},
                "consultant_number": {"title": "咨询员编号", "required": False, "default": ""},
                "submitter": {"title": "cl", "required": False, "default": ""}
            }
        )

        error_rows = []
        for item in items:
            # item.app_id = str(item.app_id)
            # if not check_file(item, self.attach_dir,self.file_format):
            #     error_rows.append(item.app_id)
            pass
        if len(error_rows) > 0:
            for e in error_rows:
                logger.info(f"资料文件有异常: {e}")
            raise Exception("资料检查未通过")
        logger.info("数据加载完成")
        return items

    def open_url(self):
        self.driver.get("https://baoquan.court.gov.cn")
        logger.info("打开网站:https://baoquan.court.gov.cn")

    def prefun(self):
        # login()
        self.driver = g_driver
    def run_job(self, item):

        item.header = g_header
        job = DoBaoQuanJob(self.driver, self.attach_dir, item, self.file_format)
        job.run()

    def reset(self):
        self.afterfun()
        time.sleep(1)
        self.prefun()

    def afterfun(self):
        if self.driver:
            self.driver.quit()


def login():
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    global g_driver
    g_driver = webdriver.Chrome(options=option)
    g_driver.get("https://baoquan.court.gov.cn")
    logger.info("打开网站:https://baoquan.court.gov.cn")

    frame = g_driver.find_element(By.XPATH,
                                  value='//*[@id=\"index\"]/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/iframe')
    g_driver.switch_to.frame(frame)
    fill_input(g_driver, '//*[@id="root"]/div/form/div[1]/div[1]/div/div/div/input', g_username, '手机号码')
    fill_input(g_driver, '//*[@id="root"]/div/form/div[1]/div[2]/div/div/div/input', g_pwd, '密码')
    click(g_driver, '//*[@id="root"]/div/form/div/div[3]/span', '登录')
    time.sleep(2)
    for i in range(20):
        cookies = g_driver.get_cookies()
        print(len(cookies))
        if len(cookies) == 2:
            login()

        time.sleep(1)
        try:
            cookies[1]
            break
        except:
            continue
    cookie = f"Admin-Token={cookies[1].get('value')}; Admin-UserData={cookies[0].get('value')}"
    global g_header
    bearer = cookies[1].get('value')
    u_a = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    g_header = {
        "Cookie": cookie,
        "Bearer": bearer,
        "User-Agent": u_a
    }




export = ScriptDef(
    cls=XJFYBaoQuanFlow,
    group="外网保全系统",
    title="New_保全申请-外网保全申请-自定义证据材料",
    arguments=[
        FileItem(title="excel表格", name="excel_file"),
        DirectoryItem(title="附件文件夹", name="attach_dir"),
        UserSelectItem(title="账号", username_field="username", password_field="password"),
        StringItem(title="文件格式（借款协议，就写借款协议）", name="file_format"),

    ]
)

if __name__ == '__main__':
    flow = XJFYBaoQuanFlow(r"C:\Users\9000\Desktop\保全\【3-22】1-199-1-201-400（线下）3月马鞍山500-程序-纳百语.xlsx",
                           r'C:\Users\9000\Desktop\保全', '17633602179',
                           'mimashisha555...', '借款协议')
    flow.run()
