"""
-*- coding: utf-8 -*-
@Time : 2022/9/7 17:05
"""
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import json
import os
import time
import requests
from openpyxl import load_workbook
from flows.flow import ScriptDef, UserSelectItem, DirectoryItem, FileItem, ListDataFlow, StringItem, NumberItem
from rpalib.log import logger
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


def gen_key(obj, item):
    return item.app_id


class FYBaoQuanFlow(object):
    def __init__(self, excel_file, attach_dir, username, password, file_format, defendant_age, cache_path) -> None:
        self.excel_file = excel_file
        self.attach_dir = attach_dir
        self.username = username
        self.password = password
        self.file_format = file_format
        self.defendant_age = defendant_age
        self.cache_path = cache_path
        self.lists = []

    # 接受异常
    def expect_fun(self, e, _):
        print('进入异常处理')
        logger.error(e)
        print('异常处理完成')

    def load_excel(self):
        wb = load_workbook(filename=self.excel_file)
        sh = wb.worksheets[0]
        self.data = {}
        i = 1
        for row in sh.rows:
            if i:
                i = 0
                continue
            if not row[0].value: continue
            self.data[f"{row[0].value}"] = \
                {
                    "jjh": row[0].value, "sqfy": row[1].value, "bxgs": row[2].value, "bqje": row[3].value,
                    "sqrdw": row[4].value, "sqrxydm": row[5].value, "sqrfdr": row[6].value, "sqrsjh": row[7].value,
                    "sqrdwdz": row[8].value,
                    "bsqr": row[9].value, "bsqrzjh": row[10].value, "bcqrsjh": row[11].value, "bsqrdi": row[12].value,
                    "ms": row[18].value,
                    "ccjz": row[19].value
                }

    # 输入地址
    def open_url(self):
        self.driver.get("https://baoquan.court.gov.cn")
        logger.info("打开网站:https://baoquan.court.gov.cn")

    # 登录保全系统
    def login(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_argument(rf'--user-data-dir={self.cache_path}')
        self.driver = webdriver.Chrome(options=option)
        self.open_url()

        frame = self.driver.find_element(By.XPATH,
                                         value='//*[@id=\"index\"]/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/iframe')
        self.driver.switch_to.frame(frame)
        fill_input(self.driver, '//*[@id="root"]/div/form/div[1]/div[1]/div/div/div/input', self.username, '手机号码')
        fill_input(self.driver, '//*[@id="root"]/div/form/div[1]/div[2]/div/div/div/input', self.password, '密码')
        click(self.driver, '//*[@id="root"]/div/form/div/div[3]/span', '登录')
        time.sleep(2)
        for i in range(20):
            cookies = self.driver.get_cookies()

            time.sleep(1)
            try:
                cookies[1]
                break
            except:
                continue
        self.cookie = f"Admin-Token={cookies[1].get('value')}; Admin-UserData={cookies[0].get('value')}"
        self.bearer = cookies[1].get('value')
        u_a = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        self.header = {
            "Cookie": self.cookie,
            "Bearer": self.bearer,
            "User-Agent": u_a
        }

    def request(self, url, method="get", data=None):
        for i in range(20):
            try:
                if method == "post":
                    r = requests.session().post(url, headers=self.header, json=data, timeout=60)
                    break
                else:
                    r = requests.session().get(url, headers=self.header, timeout=60)
                    break
            except Exception as e:

                continue

        return r

    # 担保的基本信息
    def danbao_jbxx(self, court, insurance, money):
        # 获得法院ID
        url_court_id = f"https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsqs/xzfy?time={int(time.time() * 1000)}&mklx=1"
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
    def respondent(self, byName, byIdCode, byPhone, byAddress, ress):

        byIdCode = str(byIdCode)
        birth_day = f"{byIdCode[6:14][0:4]}-{byIdCode[6:14][4:6]}-{byIdCode[6:14][6:]}"
        data = [{
            'cBqDsrid': ress,
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

    # 添加财产线索
    def property(self, ccName, describe, cost, ress):
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
            "cSqbqccyyz": ress,
            "cXjzje": "",
            "cXjzjeTS": "",
            "cYhckzckdw": "",
            "cYhckzckje": "",
            "cYhckzckjeTS": "",
            "cYhckzkhzh": "",
        }]
        return data

    # 保全基本信息
    def basic_baoquan(self, item):

        items = self.data.get(item[0])

        ret1 = self.proposer(items.get("sqrdw"), items.get("sqrxydm"), items.get("sqrfdr"), items.get("sqrsjh"),
                             items.get("sqrdwdz"))
        #
        ret2s = []
        ret4s = []
        for item in item:
            itemes = self.data.get(item)
            url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/id?time={int(time.time() * 1000)}'
            res = requests.get(url)
            ress = json.loads(res.text).get("data")

            ret2 = self.respondent(itemes.get("bsqr"), itemes.get("bsqrzjh"), itemes.get("bcqrsjh"),
                                   itemes.get("bsqrdi"), ress)
            ret2s.append(ret2[0])
            ret4 = self.property(itemes.get('bsqr'), itemes.get("ms"), itemes.get("ccjz"), ress)
            ret4s.append(ret4[0])

        # sys.exit()

        url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsqinfo?time={int(time.time() * 1000)}&bqid={self.bqid}'
        ret = json.loads(requests.get(url, headers=self.header).text).get("data")
        data = {
            "bqDsrs": ret2s,
            "bqJbxx": ret,
            "bqProperties": ret4s,
            "bqSqrs": ret1,
            "tBqDlrs": [],
            "ccxsId": [],
            "dsrIds": [],
            "sqrIds": [],
            "xwxxIds": [],
            "xwxxs": [],
            "ygdlrIds": [],
            "zjxxIds": [],
            "zjxxs": [],
        }
        url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsq/tempsave?time={int(time.time() * 1000)}&bqid={self.bqid}'
        r = self.request(url, method="post", data=data)
        if str(r.status_code) == "200":
            logger.info(f"{items.get('cDsrxm')}保全基本信息保存完成")

    # 创建担保申请
    def danbao_create(self, insurance, ccjz):
        url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/dbxx?time={int(round(time.time() * 1000))}&bqid={self.bqid}'
        payload = {"jbxxs": [{"cSzxid": None, "cSqrxm": "", "cSqbgyy": "", "cDbfs": "5", "cBxgs": "",
                              "cBxgsmc": insurance, "cBdh": "", "nDbjz": ccjz, "nDbjzTS": "2,000", "cCclx": "",
                              "cDbsm": "", "cDbr": "", "cDbr_require": "", "nSysbuy": 2, "cDbwmc": "", "isAdd": True}],
                   "ids": []}
        self.request(url, method='post', data=payload)

    def upload(self, file_name, file_full_path, type):
        if type == 1:
            cllx = '1'
            id_ = ''
        elif type == 2:
            cllx = '2'
            id_ = ''
        elif type == 6:
            cllx = '4'
            id_ = str(self.dbid)
        elif type == 7:
            cllx = '3'
            id_ = self.cBqId
        elif type == 8:
            cllx = '3'
            id_ = self.cBqDsrid
        elif type == 11:
            cllx = '3'
            id_ = str(int(self.bqid) + 1)
        elif type == 9:
            cllx = '4'
            id_ = str(int(self.bqid) + 4)
        elif type == 10:
            cllx = "5"
            id_ = ''
        clid = str(time.time()).replace('.', '')
        clid = clid[0:-2] + '.' + clid[-2:]
        # full_name = os.path.join(filepath)
        if file_name.endswith("pdf"):
            m = "application/pdf"
        else:
            m = "image/jpg"
        files = [('files', (file_name, open(os.path.join(file_full_path), 'rb'), m))]
        # files = {'files': (file_name, open(os.path.join(file_full_path), 'rb'))}
        # files = [("files", (file_name, open(file_path, "rb"), self.fileType.get(file_name.split(".")[-1]))), ]
        url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/sccls/dbxx/fileupload?time={int(round(time.time() * 1000))}'
        data = {'cllx': cllx, "bqid": self.bqid, "clid": clid, "id": id_}
        for i in range(10):
            try:
                requests.post(url, headers=self.header, data=data, files=files, timeout=60, verify=False)
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
    def proposer_save(self, jname, bsqrzjh):
        filename = f"{jname}-{bsqrzjh}-保全申请书.pdf"
        file_full_path = os.path.join(self.attach_dir, "诉前保全申请书", filename)
        if not os.path.exists(file_full_path):
            filename = f"{jname}-{bsqrzjh}-保全申请书.jpg"
            file_full_path = os.path.join(self.attach_dir, "诉前保全申请书", filename)
        self.upload(filename, file_full_path, 1)
        logger.info(f"上传保全申请书上传成功")

    # 身份证明材料
    def identity(self, items):
        url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/bsqrs?time={int(round(time.time() * 1000))}&bqid={self.bqid}'
        data = self.request(url).json().get('data')[0]
        # self.cBqDsrid = data.get("cBqDsrid")
        self.cBqId = data.get("cBqId")
        file_full_path = os.path.join(self.attach_dir, "申请人资料", "原告资料.pdf")
        self.upload("原告资料.pdf", file_full_path, 7)
        logger.info("申请人身份证明材料上传成功")
        c = 0
        for i in items:
            urls = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/bsqrs?time={int(round(time.time() * 1000))}&bqid={self.bqid}'
            datas = self.request(urls).json().get('data')[c]
            self.cBqDsrid = datas.get("cBqDsrid")
            itemes = self.data.get(i)
            m = os.path.join(self.attach_dir, "被申请人资料", f"{itemes.get('bsqr')}{itemes.get('bsqrzjh')}")
            id_pic = f"{itemes.get('bsqr')}-{itemes.get('bsqrzjh')}-被告身份证"
            if check_img_file(m, id_pic, m):
                full_path, filename = self.choice_img_file(m, f"{itemes.get('bsqr')}-{itemes.get('bsqrzjh')}-被告身份证")
                self.upload(filename, file_full_path, 8)
                return

            full_path, filename = self.choice_img_file(m, f"{itemes.get('bsqr')}-{itemes.get('bsqrzjh')}-被告身份证正面")
            self.upload(filename, full_path, 8)
            full_path, filename = self.choice_img_file(m, f"{itemes.get('bsqr')}-{itemes.get('bsqrzjh')}-被告身份证反面")
            self.upload(filename, full_path, 8)
            logger.info("被申请人身份证明材料上传成功")
            c += 1

    # 证据材料
    def zhengjucailiao(self, jname, bsqrzjh, code):
        filename = f"{jname}-{bsqrzjh}-{code}-{self.file_format}.pdf"
        file_full_path = os.path.join(self.attach_dir, "被申请人资料", f"{jname}{bsqrzjh}",
                                      filename)
        self.upload(filename, file_full_path, 10)

    # 担保材料
    def danbaocailiao(self):
        url = f"https://baoquan.court.gov.cn/wsbq/ssbq/api/sccls/sccls?time={int(round(time.time() * 1000))}&bqid={self.bqid}"
        self.dbid = self.request(url).json().get("data").get("dbl")
        try:
            self.dbid = self.dbid[0].get("dbid")
        except:
            self.dbid = self.dbid[1].get("dbid")
        file_full_path = os.path.join(self.attach_dir, "担保资料", "担保资料.pdf")
        self.upload("担保资料.pdf", file_full_path, 6)

    def submit(self, jjh):
        url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsq/tj?time={int(round(time.time() * 1000))}&id={self.bqid}'
        r = requests.put(url, headers=self.header).text
        logger.info(r)
        message = json.loads(r).get('message')
        if message == "提交成功":
            logger.info(f"{jjh}担保申请成功")

    def run_job(self, items):
        item = self.data.get(items[0])
        self.danbao_jbxx(item.get("sqfy"), item.get('bxgs'), item.get('bqje'))
        time.sleep(0.5)
        self.basic_baoquan(items)
        time.sleep(0.5)
        self.danbao_create(item.get('bxgs'), item.get('ccjz'))
        time.sleep(0.5)
        self.proposer_save(item.get('bsqr'), item.get('bsqrzjh'))
        time.sleep(0.5)
        self.identity(items)
        time.sleep(0.5)
        self.zhengjucailiao(item.get('bsqr'), item.get('bsqrzjh'), item.get('jjh'))
        time.sleep(0.5)
        self.danbaocailiao()
        time.sleep(60)
        self.submit(item.get('jjh'))

    def run(self):
        try:
            self.load_excel()
            if len(self.data) % int(self.defendant_age) != 0:
                raise Exception(logger.error("表格数据量与输入的人数不符合，请手动更改！"))
        except:
            raise
        self.login()
        for item in self.data:
            self.lists.append(item)

        while len(self.lists) > 0:
            print("------------------------------")
            list = []
            for i in range(int(self.defendant_age)):
                # j 为案号
                j = self.lists.pop(0)
                list.append(j)
            for i in range(3):
                try:
                    self.run_job(list)
                    break
                except:
                    logger.error(list, "出错，请检查！")
                    continue

        self.driver.quit()


export = ScriptDef(
    cls=FYBaoQuanFlow,
    group="外网保全系统",
    title="保全申请-外网保全申请自定义一对多版",
    arguments=[
        FileItem(title="excel表格", name="excel_file"),
        DirectoryItem(title="附件文件夹", name="attach_dir"),
        UserSelectItem(title="账号", username_field="username", password_field="password"),
        StringItem(title="文件格式（借款协议，就写借款协议）", name="file_format"),
        StringItem(title="自定义人数", name="defendant_age"),
        DirectoryItem(title="缓存文件夹", name="cache_path")
    ]
)

if __name__ == '__main__':
    FYBaoQuanFlow(r"C:\Users\9000\Desktop\一对多样例\【8-3】长丰200(1).xlsx",
                  r'C:\Users\9000\Desktop\一对多样例\样例辅助',
                  r'15637773596', r'Wxb2259354168', '一次债转协议', 5, r'C:\Users\9000\Desktop\缓存').run()