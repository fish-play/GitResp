# # # """
# # # -*- coding: utf-8 -*-
# # # @Time : 2022/9/7 16:58
# # # """
# # # import json
# # # import os
# # # import time
# # #
# # # import requests
# # # from selenium import webdriver
# # # from selenium.webdriver.chrome.webdriver import WebDriver
# # # from selenium.webdriver.support.wait import WebDriverWait
# # #
# # # from flows.flow import FileItem, ListDataFlow, ScriptDef, StringItem, DirectoryItem, UserSelectItem
# # #
# # # from rpalib.log import logger
# # # from rpalib import excel
# # #
# # #
# # # # # 点击
# # # def click(driver, xpath, text=''):
# # #     btn = WebDriverWait(driver, 30).until(lambda el: driver.find_element_by_xpath(xpath))
# # #     btn.click()
# # #     logger.info('点击按钮:' + text)
# # #     time.sleep(2)
# # #
# # #
# # # # 填写输入框
# # # def fill_input(driver, xpath, value, input_name):
# # #     input = WebDriverWait(driver, 30).until(lambda el: driver.find_element_by_xpath(xpath))
# # #     input.send_keys(value)
# # #     logger.info('输入框:' + input_name + ',输入值:' + str(value))
# # #     time.sleep(1)
# # #
# # #
# # # #
# # # #
# # # # 检测文件是否存在
# # # def check_file(item, attach_dir, file_format):
# # #     bqsqs = os.path.join(attach_dir, "诉前保全申请书",  item.respondent_name + "-" + item.respondent_cert_no + "-保全申请书.pdf")
# # #     if not os.path.exists(bqsqs):
# # #         bqsqs = os.path.join(attach_dir, "诉前保全申请书", item.respondent_name + "-" + item.respondent_cert_no + "-保全申请书.jpg")
# # #     ygzl = os.path.join(attach_dir, "申请人资料", "原告资料.pdf")
# # #     if item.agent_name:
# # #         if not check_img_file(os.path.join(attach_dir, "原告代理人"), f"{item.agent_name}_代理人", attach_dir):
# # #             logger.info(f"原告代理人文件不存在:{item.agent_name}")
# # #             return False
# # #
# # #     jkxy = os.path.join(attach_dir, "被申请人资料", item.respondent_name+item.respondent_cert_no,
# # #                          item.respondent_name + "-" + item.respondent_cert_no + "-" + item.app_id + f"-{file_format}.pdf")
# # #
# # #     file_parent_path = os.path.join(attach_dir, "被申请人资料", item.respondent_name + item.respondent_cert_no)
# # #     id_pic_front = f"{item.respondent_name}-{item.respondent_cert_no}-被告身份证正面"
# # #     id_pic_back = f"{item.respondent_name}-{item.respondent_cert_no}-被告身份证反面"
# # #     id_pic = f"{item.respondent_name}-{item.respondent_cert_no}-被告身份证"
# # #     if check_single_file(bqsqs, attach_dir) \
# # #             and check_single_file(ygzl, attach_dir) \
# # #             and check_single_file(jkxy, attach_dir):
# # #         if check_img_file(file_parent_path, id_pic_front, attach_dir) \
# # #                 and check_img_file(file_parent_path, id_pic_back, attach_dir):
# # #             return True
# # #         elif check_img_file(file_parent_path, id_pic, attach_dir):
# # #             return True
# # #         else:
# # #             file = os.path.join(file_parent_path, f"{id_pic}")
# # #             logger.info("文件不存在:" + file)
# # #     return False
# # #
# # #
# # # def check_single_file(file_full_path, attach_dir):
# # #     if os.path.exists(file_full_path):
# # #         return True
# # #     logger.info("文件不存在:" + file_full_path)
# # #     return False
# # #
# # #
# # # def check_img_file(file_parent, file_name, attach_dir):
# # #     file = os.path.join(file_parent, f"{file_name}")
# # #     for suffix in ["jpg", "jpeg", "png", "pdf"]:
# # #         full_path = os.path.join(file + f".{suffix}")
# # #         if os.path.exists(full_path):
# # #             return True
# # #     return False
# # #
# # #
# # # class BaoQuanItem(object):
# # #     # '进件号'
# # #     app_id: str
# # #     # 申请人单位
# # #     spv_name: str
# # #     # 申请人信用代码
# # #     spv_cert_no: str
# # #     # 申请人法定人
# # #     spv_legal: str
# # #     # 申请人手机号
# # #     spv_phone: str
# # #     # 申请人单位地址
# # #     spv_address: str
# # #
# # #     # 代理人姓名
# # #     agent_name: str
# # #     # 代理人证件号
# # #     agent_cert_no: str
# # #     # 代理人手机号
# # #     agent_phone: str
# # #     # 代理人执行号
# # #     agent_work_no: str
# # #     # 代理人律所
# # #     agent_company: str
# # #
# # #     # 被申请人姓名
# # #     respondent_name: str
# # #     # 被申请人证件号
# # #     respondent_cert_no: str
# # #     # 被申请人手机号
# # #     respondent_phone: str
# # #     # 被申请人地址
# # #     respondent_address: str
# # #
# # #     # 申请法院
# # #     court: str
# # #     # 保险公司
# # #     insurance: str
# # #     # 财产价值
# # #     property_value: float
# # #     # 申请保全金额
# # #     amount: float
# # #     # 描述
# # #     description: str
# # #     # 咨询员编号d
# # #     consultant_number: str
# # #     # 提交人身份
# # #     submitter: str
# # #     # requests header
# # #     header: dict
# # #     # cookie bearer
# # #     cookie: str
# # #     bearer: str
# # #
# # #     def __str__(self) -> str:
# # #         return f"{self.app_id}-{self.respondent_cert_no}"
# # #
# # #
# # # class DoBaoQuanJob(object):
# # #     def __init__(self, driver: WebDriver, attach_dir: str, item: BaoQuanItem, file_format) -> None:
# # #         super().__init__()
# # #         self.driver = driver
# # #         self.attach_dir = attach_dir
# # #         self.item = item
# # #         self.file_format = file_format
# # #
# # #     def request(self, url, method="get", data=None):
# # #         for i in range(20):
# # #             try:
# # #                 if method == "post":
# # #                     r = requests.session().post(url, headers=self.item.header, json=data, timeout=60, verify=False)
# # #                     break
# # #                 else:
# # #                     r = requests.session().get(url, headers=self.item.header, timeout=60, verify=False)
# # #                     break
# # #             except Exception as e:
# # #                 print(e)
# # #                 continue
# # #         return r
# # #
# # #     # 担保
# # #     def danbao(self, court, insurance, money):
# # #         # 获得法院ID
# # #         url_court_id = f"https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsqs/xzfy?time={int(round(time.time() * 1000))}&mklx=1"
# # #         court_data = json.loads(self.request(url_court_id).text)
# # #         for x in court_data.get("data")[0].get("children"):
# # #             for i in x.get("children"):
# # #                 for y in i.get("children"):
# # #                     if y.get("name") == court:
# # #                         self.court_id = y.get("id")
# # #                         break
# # #         url_create_baoquan = r"https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsq"
# # #         data_bqsq = \
# # #             {"cBqlb": "1",
# # #              "cBqlx": "1",
# # #              "cDbqk": "1",
# # #              "cFsqj": "1",
# # #              "cTjrlx": "3",  # 律师:1 其他代理人:3
# # #              "nSqbqdcsfy": "40",
# # #              "nSqbqje": f"{money}",
# # #              "nSqfy": self.court_id,
# # #              "nSqfymc": court,
# # #              "time": "1624513711933"}
# # #         if self.item.submitter == '律师':
# # #             data_bqsq["cTjrlx"] = "1"
# # #         else:
# # #             data_bqsq["cTjrlx"] = "3"
# # #         r = self.request(url_create_baoquan, "post", data=data_bqsq)
# # #         self.bqid = json.loads(r.text).get("data")
# # #         logger.info(f"{self.bqid}    -----------------------------")
# # #
# # #     # 添加申请人
# # #     def proposer(self, unit, code, legal, phone, address):
# # #         # 男1 女2
# # #         # 身份证1 护照2 户口簿6
# # #         # 汉1
# # #         # 机关1 事业2 企业3 社会4 民办5
# # #         # 营业执照1 组织2 事业3 统一4
# # #         data = [{
# # #             "cDwxz": "",
# # #             "cEmail": "",
# # #             "cGh": "",
# # #             "cGh1": "",
# # #             "cGh2": "",
# # #             "cGh3": "",
# # #             "cId": self.bqid,
# # #             "cPhoneno": phone,
# # #             "cQyfr": legal,
# # #             "cQymc": unit,
# # #             "cQyzch": "",
# # #             "cQyzzjgdm": code,
# # #             "cSqrlx": "2",  # 法人
# # #             "cSqrxb": None,
# # #             "cSqrxm": "",
# # #             "cTxdz": address,
# # #             "cZjh": "",
# # #             "cZjlx": 4,
# # #             "dtSqrBirthday": "",
# # #             "nMz": None,
# # #             "nNl": None,
# # #             "nZzlx": 4,  # 证照类型
# # #         }]
# # #         return data
# # #
# # #     # 添加被申请人
# # #     def respondent(self, byName, byIdCode, byPhone, byAddress):
# # #         byIdCode = str(byIdCode)
# # #         birth_day = f"{byIdCode[6:14][0:4]}-{byIdCode[6:14][4:6]}-{byIdCode[6:14][6:]}"
# # #         url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/id?time={int(round(time.time() * 1000))}'
# # #         self.Dsrid = self.request(url).json().get("data")
# # #         data = [{
# # #             'cBqDsrid': self.Dsrid,
# # #             'cCzdz': "",
# # #             'cDsrlx': "1",  # 证件类型 身份证1
# # #             'cDsrxb': "1" if int(byIdCode[-2]) % 2 != 0 else "2",  # 性别类型 男1
# # #             'cDsrxm': byName,
# # #             'cDwdz': "",
# # #             'cDwxz': "",
# # #             'cGh': "",
# # #             'cGh1': "",
# # #             'cGh2': "",
# # #             'cGh3': "",
# # #             'cPhoneno': "",
# # #             'cPhoneno_no': "",
# # #             'cQyfr': "",
# # #             'cQymc': "",
# # #             'cQyzcdjh': "",
# # #             'cTxdz': byAddress,
# # #             'cTxdz_no': byAddress,
# # #             'cZjh': byIdCode,
# # #             'cZjh_no': byIdCode,
# # #             'cZjlx': "1",  # 证件类型
# # #             'cZzjgdm': "",
# # #             'dtDsrbirthday': birth_day,
# # #             'nMz': 1,
# # #             'nNl': time.localtime().tm_year - int(birth_day.split('-')[0]),
# # #         }]
# # #         if byPhone != None and byPhone != '':
# # #             data[0]["cPhoneno"] = byPhone
# # #             data[0]["cPhoneno_no"] = byPhone
# # #         return data
# # #
# # #     # 原告代理人
# # #     def add_agent(self):
# # #         item = self.item
# # #         if item.agent_name is None:
# # #             return
# # #         data = [{
# # #             "cBqSqrids": [self.bqid],
# # #             "cDlrlx": "3",  # 代理人类型律师1 近亲属或工作人员3
# # #             "cDlrszls": item.agent_company,
# # #             "cDlrxb": "1" if int(str(item.agent_cert_no)[-2]) % 2 != 0 else "2",  # 性别男1
# # #             "cDlrxm": item.agent_name,
# # #             "cDlrzjh": item.agent_cert_no,
# # #             "cDlrzjhm": item.agent_work_no,
# # #             "cDlrzjlx": "1",  # 证件类型身份证1
# # #             "cGddh": "",
# # #             "cGddh1": "",
# # #             "cGddh2": "",
# # #             "cGddh3": "",
# # #             "cPhone": item.agent_phone,
# # #         }]
# # #         print(data)
# # #         # exit()
# # #         if self.item.submitter == '工作人员':
# # #             data[0]["cDlrzjhm"] = ""
# # #             data[0]["cDlrszls"] = ""
# # #         return data
# # #
# # #     # 添加财产线索
# # #     def property(self, ccName, describe, cost):
# # #         cSqbqccjeTS = ''
# # #         for x, i in enumerate(range(0, len(str(cost)))):
# # #             cSqbqccjeTS += str(cost)[len(str(cost)) - i - 1]
# # #             if ((x + 1) % 3) == 0:
# # #                 cSqbqccjeTS += ','
# # #         cSqbqccjeTS = cSqbqccjeTS[::-1] if cSqbqccjeTS[-1] != ',' else cSqbqccjeTS[::-1][1:]
# # #         data = [{
# # #             "cCclx": "255",  # 财产类型其他255
# # #             "cCclxccxx": "",
# # #             "cCclxcllx": "",
# # #             "cCclxfcdz": "",
# # #             "cCclxfczh": "",
# # #             "cCclxtddcqzh": "",
# # #             "cCclxtdddz": "",
# # #             "cCclxtdmj": "",
# # #             "cCclxzbz": "",
# # #             "cCclxzclpp": "",
# # #             "cCclxzgpdcgsl": "",
# # #             "cCclxzgpdgpmc": "",
# # #             "cCclxzgqdcggs": "",
# # #             "cCclxzgqdczbl": "",
# # #             "cCclxzgqdgsxx": "",
# # #             "cCclxzjjdjjmc": "",
# # #             "cCclxzjjdjjsl": "",
# # #             "cCclxzswdtszh": "",
# # #             "cCclxzzwdzqmc": "",
# # #             "cCclxzzwdzqmz": "",
# # #             "cCclxzzwdzqmzTS": "",
# # #             "cCklxzcldcph": "",
# # #             "cGsd": "",
# # #             "cKhhmc": "",
# # #             "cMs": describe,
# # #             "cSbmc": "",
# # #             "cSqbqccje": cost,
# # #             "cSqbqccjeTS": cSqbqccjeTS,
# # #             "cSqbqccyyz": self.Dsrid,
# # #             "cXjzje": "",
# # #             "cXjzjeTS": "",
# # #             "cYhckzckdw": "",
# # #             "cYhckzckje": "",
# # #             "cYhckzckjeTS": "",
# # #             "cYhckzkhzh": "",
# # #         }]
# # #         return data
# # #
# # #     def basic_baoquan(self):
# # #         # 保全基本信息
# # #         ret1 = self.proposer(self.item.spv_name, self.item.spv_cert_no, self.item.spv_legal, self.item.spv_phone,
# # #                              self.item.spv_address)
# # #         ret2 = self.respondent(self.item.respondent_name, self.item.respondent_cert_no, self.item.respondent_phone,
# # #                                self.item.respondent_address)
# # #         ret3 = self.add_agent()
# # #         ret4 = self.property(self.item.respondent_name, self.item.description, self.item.property_value)
# # #         url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsqinfo?time={int(round(time.time() * 1000))}&bqid={self.bqid}'
# # #         ret = json.loads(requests.get(url, headers=self.item.header, verify=False).text).get("data")
# # #         data = {
# # #             "bqDsrs": ret2,
# # #             "bqJbxx": ret,
# # #             "bqProperties": ret4,
# # #             "bqSqrs": ret1,
# # #             "tBqDlrs": ret3,
# # #             "ccxsId": [],
# # #             "dsrIds": [],
# # #             "sqrIds": [],
# # #             "xwxxIds": [],
# # #             "xwxxs": [],
# # #             "ygdlrIds": [],
# # #             "zjxxIds": [],
# # #             "zjxxs": [],
# # #         }
# # #         url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsq/tempsave?time={int(round(time.time() * 1000))}&bqid={self.bqid}'
# # #         r = self.request(url, method="post", data=data)
# # #         if str(r.status_code) == "200":
# # #             logger.info(f"{self.item.respondent_name}保全基本信息保存完成")
# # #
# # #     # 创建担保申请
# # #     def danbao_create(self, insurance, amount):
# # #         # 保险公司code
# # #         # url = r'https://baoquan.court.gov.cn/wsbq/ssbq/api/commoncodepz?time=&cPid=127000'
# # #         # commoncode = json.loads(self.request(url).text).get('data')
# # #         # for i in commoncode:
# # #         #     if i.get('cName') == insurance:
# # #         #     # if i.get('cName') == "中国大地财产保险股份有限公司":
# # #         #         cCode = i.get('cCode')
# # #         #         break
# # #         # url_dbid = r'https://baoquan.court.gov.cn/wsbq/ssbq/api/ssdb/sqdbxx?time=1624586574035&bqid=%s' % self.bqid
# # #         # url_get_fl = rf'https://baoquan.court.gov.cn/wsbq/commonapi/api/policy/premium?time=1624588329914&preserveAmount=' \
# # #         #              rf'{self.item.property_value}&institution={cCode}&corpId={self.court_id}'
# # #         # data2 = {"preserveAmount": self.item.property_value, "institution": cCode, "corpId": self.court_id}
# # #         # r = json.loads(self.request(url_get_fl, "post", data=data2).text).get("data")
# # #         # data1 = {
# # #         #     "cBqlb": "1",  # 保全类型 财产保全
# # #         #     "cBqlx": "1",  # 保全类别 诉前保全
# # #         #     "cBxgs": cCode,
# # #         #     "cClerkNo": consultant_number,
# # #         #     "cFl": r.get("minRate"),
# # #         #     "cFsqj": "1",
# # #         #     "cFyid": self.court_id,
# # #         #     "cFymc": self.item.court,
# # #         #     "cMaxfl": r.get("maxRate"),
# # #         #     "cTjrlx": "3",  # 提交人类型 其他人
# # #         #     "nDbfy": r.get("maxAmount"),
# # #         #     "nMaxdbfy": r.get("minAmount"),
# # #         #     "nSqbqje": f"{self.item.property_value}",
# # #         # }
# # #         # self.dbid = json.loads(self.request(url_dbid, "post", data=data1).text).get("data")
# # #
# # #         url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/dbxx?time={int(round(time.time() * 1000))}&bqid={self.bqid}'
# # #         payload = {"jbxxs": [{"cSzxid": None, "cSqrxm": "", "cSqbgyy": "", "cDbfs": "5", "cBxgs": "",
# # #                         "cBxgsmc": insurance, "cBdh": "", "nDbjz": amount, "nDbjzTS": "2,000", "cCclx": "",
# # #                         "cDbsm": "", "cDbr": "", "cDbr_require": "", "nSysbuy": 2, "cDbwmc": "", "isAdd": True}],
# # #              "ids": []}
# # #         self.request(url, method='post', data=payload)
# # #
# # #
# # #     def upload(self, file_name, file_full_path, type):
# # #         if type == 1:
# # #             cllx = '1'
# # #             id_ = ''
# # #         elif type == 2:
# # #             cllx = '2'
# # #             id_ = ''
# # #         elif type == 6:
# # #             cllx = '4'
# # #             id_ = str(self.dbid)
# # #         elif type == 7:
# # #             cllx = '3'
# # #             id_ = self.cBqId
# # #
# # #         elif type == 8:
# # #             cllx = '3'
# # #             id_ = self.cBqDsrid
# # #
# # #         elif type == 11:
# # #             cllx = '3'
# # #             id_ = str(int(self.bqid) + 1)
# # #
# # #         elif type == 5:
# # #             cllx = '3'
# # #             id_ = self.cBqDlrid
# # #
# # #         elif type == 9:
# # #             cllx = '4'
# # #             id_ = str(int(self.bqid) + 4)
# # #         elif type == 10:
# # #             cllx = "5"
# # #             id_ = ''
# # #         clid = str(time.time()).replace('.', '')
# # #         clid = clid[0:-2] + '.' + clid[-2:]
# # #         # full_name = os.path.join(filepath)
# # #         if file_name.endswith("pdf"):
# # #             m = "application/pdf"
# # #         else:
# # #             m = "image/jpg"
# # #         files = [('files', (file_name, open(os.path.join(file_full_path), 'rb'), m))]
# # #         # files = {'files': (file_name, open(os.path.join(file_full_path), 'rb'))}
# # #         # files = [("files", (file_name, open(file_path, "rb"), self.fileType.get(file_name.split(".")[-1]))), ]
# # #         url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/sccls/dbxx/fileupload?time={int(round(time.time() * 1000))}'
# # #         data = {'cllx': cllx, "bqid": self.bqid, "clid": clid, "id": id_}
# # #         for i in range(10):
# # #             try:
# # #                 requests.post(url, headers=self.item.header, data=data, files=files, timeout=60, verify=False)
# # #                 logger.info(f"{file_name}上传完成")
# # #                 break
# # #             except Exception as e:
# # #                 logger.info(f"{file_name}上传超时。。重试  error:{e}")
# # #
# # #     def choice_img_file(self, file_parent, file_name):
# # #         for suffix in ["jpg", "jpeg", "png", "pdf"]:
# # #             full_path = os.path.join(file_parent, f"{file_name}.{suffix}")
# # #             if os.path.exists(full_path):
# # #                 return full_path, f"{file_name}.{suffix}"
# # #         raise Exception(f"文件{file_name}不存在")
# # #
# # #     # 上传保全申请书
# # #     def proposer_save(self, jname):
# # #         filename = f"{jname}-{self.item.respondent_cert_no}-保全申请书.pdf"
# # #         file_full_path = os.path.join(self.attach_dir, "诉前保全申请书", filename)
# # #         if not os.path.exists(file_full_path):
# # #             filename = f"{jname}-{self.item.respondent_cert_no}-保全申请书.jpg"
# # #             file_full_path = os.path.join(self.attach_dir, "诉前保全申请书", filename)
# # #         self.upload(filename, file_full_path, 1)
# # #         logger.info(f"上传保全申请书上传成功")
# # #
# # #     # 身份证明材料
# # #     def identity(self, jname):
# # #         url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/bsqrs?time={int(round(time.time() * 1000))}&bqid={self.bqid}'
# # #         data = self.request(url).json().get('data')[0]
# # #         self.cBqDsrid = data.get("cBqDsrid")
# # #         self.cBqId = data.get("cBqId")
# # #         file_full_path = os.path.join(self.attach_dir, "申请人资料", "原告资料.pdf")
# # #         self.upload("原告资料.pdf", file_full_path, 7)
# # #         logger.info("申请人身份证明材料上传成功")
# # #         m = os.path.join(self.attach_dir, "被申请人资料", f"{jname}{self.item.respondent_cert_no}")
# # #         id_pic = f"{jname}-{self.item.respondent_cert_no}-被告身份证"
# # #         if check_img_file(m, id_pic, m):
# # #             full_path, filename = self.choice_img_file(m, f"{jname}-{self.item.respondent_cert_no}-被告身份证")
# # #             self.upload(filename, file_full_path, 8)
# # #             return
# # #         full_path, filename = self.choice_img_file(m, f"{jname}-{self.item.respondent_cert_no}-被告身份证正面")
# # #         self.upload(filename, full_path, 8)
# # #         full_path, filename = self.choice_img_file(m, f"{jname}-{self.item.respondent_cert_no}-被告身份证反面")
# # #         self.upload(filename, full_path, 8)
# # #         logger.info("被申请人身份证明材料上传成功")
# # #
# # #     # 代理人材料
# # #     def proposer_agency(self, path, agent_name):
# # #         if agent_name is None:
# # #             return
# # #         url1 = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/ygdlrs?time={int(round(time.time() * 1000))}&bqid={self.bqid}'
# # #         data3 = self.request(url1).json().get('data')[0]
# # #         self.cBqDlrid = data3.get('cBqDlrid')
# # #         file_parent_path = os.path.join(path, "原告代理人")
# # #         logger.info("原告代理人")
# # #         full_path, filename = self.choice_img_file(file_parent_path, f"{agent_name}_代理人")
# # #         self.upload(filename, full_path, 5)
# # #         logger.info(f"{self.item.app_id}代理人上传成功")
# # #
# # #     # 证据材料
# # #     def zhengjucailiao(self, jname, code):
# # #         print(493, self.file_format)
# # #         filename = f"{jname}-{self.item.respondent_cert_no}-{code}-{self.file_format}.pdf"
# # #         file_full_path = os.path.join(self.attach_dir, "被申请人资料", f"{jname}{self.item.respondent_cert_no}", filename)
# # #         self.upload(filename, file_full_path, 10)
# # #
# # #     # 担保材料
# # #     def danbaocailiao(self):
# # #         url = f"https://baoquan.court.gov.cn/wsbq/ssbq/api/sccls/sccls?time={int(round(time.time() * 1000))}&bqid={self.bqid}"
# # #         self.dbid = self.request(url).json().get("data").get("dbl")
# # #         try:
# # #             self.dbid = self.dbid[0].get("dbid")
# # #         except:
# # #             self.dbid = self.dbid[1].get("dbid")
# # #         file_full_path = os.path.join(self.attach_dir, "担保资料", "担保资料.pdf")
# # #         self.upload("担保资料.pdf", file_full_path, 6)
# # #
# # #     # 起诉状
# # #     def complaint_save(self):
# # #         filename = f"{self.item.respondent_name}-{self.item.app_id}-起诉状.pdf"
# # #         file_full_path = os.path.join(self.attach_dir, "起诉状", filename)
# # #         if os.path.exists(file_full_path):
# # #             self.upload(filename, file_full_path, 2)
# # #             logger.info("上传起诉状:" + file_full_path)
# # #             return
# # #         logger.info("未找到起诉状:" + file_full_path + ",跳过本步骤")
# # #
# # #     def submit(self):
# # #         url = f'https://baoquan.court.gov.cn/wsbq/ssbq/api/bqsq/tj?time={int(round(time.time() * 1000))}&id={self.bqid}'
# # #         r = requests.put(url, headers=self.item.header).text
# # #         logger.info(r)
# # #         message = json.loads(r).get('message')
# # #         if message == "提交成功":
# # #             logger.info(f"{self.item.app_id}担保申请成功")
# # #
# # #     def next(self):
# # #         s = time.time()
# # #         while True:
# # #             self.driver.get("https://baoquan.court.gov.cn/#/myApplication")
# # #             time.sleep(5)
# # #             sel_show = self.driver.find_elements_by_xpath('//*[@id="myApplication"]/div[2]/div[1]/div[1]/button')
# # #             if len(sel_show) > 0:
# # #                 return
# # #             if time.time() - s > 30:
# # #                 raise Exception("页面刷新失败")
# # #             time.sleep(1)
# # #
# # #     def run(self):
# # #         self.danbao(self.item.court, self.item.insurance, self.item.amount)
# # #         time.sleep(0.5)
# # #         self.basic_baoquan()
# # #         time.sleep(0.5)
# # #         self.danbao_create(self.item.insurance, self.item.amount)
# # #         time.sleep(0.5)
# # #         self.proposer_save(self.item.respondent_name)
# # #         time.sleep(0.5)
# # #         self.identity(self.item.respondent_name)
# # #         time.sleep(0.5)
# # #         self.proposer_agency(self.attach_dir, self.item.agent_name)
# # #         self.zhengjucailiao(self.item.respondent_name, self.item.app_id)
# # #         time.sleep(0.5)
# # #         self.danbaocailiao()
# # #         time.sleep(60)
# # #         self.submit()
# # #
# # #
# # # class XJFYBaoQuanFlow(ListDataFlow):
# # #
# # #     def __init__(self, excel_file, attach_dir, username, password, file_format) -> None:
# # #         super().__init__()
# # #         self.excel_file = excel_file
# # #         self.attach_dir = attach_dir
# # #         self.username = username
# # #         self.password = password
# # #         self.file_format = file_format
# # #
# # #     def precheck(self):
# # #         self.load_list()
# # #
# # #     def load_list(self):
# # #         items = excel.loads(
# # #             self.excel_file, BaoQuanItem, {
# # #                 "app_id": {"title": "进件号", "required": True},
# # #                 "spv_name": {"title": "申请人单位", "required": True},
# # #                 "spv_cert_no": {"title": "申请人信用代码", "required": True},
# # #                 "spv_legal": {"title": "申请人法定人", "required": True},
# # #                 "spv_phone": {"title": "申请人手机号", "required": True},
# # #                 "spv_address": {"title": "申请人单位地址", "required": True},
# # #                 "agent_name": {"title": "代理人姓名", "required": False},
# # #                 "agent_cert_no": {"title": "代理人证件号", "required": False},
# # #                 "agent_phone": {"title": "代理人手机号", "required": False},
# # #                 "agent_work_no": {"title": "代理人执行号", "required": False, "default": ""},
# # #                 "agent_company": {"title": "代理人律所", "required": False},
# # #                 "respondent_name": {"title": "被申请人姓名", "required": True},
# # #                 "respondent_cert_no": {"title": "被申请人证件号", "required": True},
# # #                 "respondent_phone": {"title": "被申请人手机号", "required": False},
# # #                 "respondent_address": {"title": "被申请人地址", "required": True},
# # #                 "court": {"title": "申请法院", "required": True},
# # #                 "insurance": {"title": "保险公司", "required": True},
# # #                 "property_value": {"title": "财产价值", "required": True},
# # #                 "amount": {"title": "申请保全金额", "required": True},
# # #                 "description": {"title": "描述", "required": True},
# # #                 "consultant_number": {"title": "咨询员编号", "required": False, "default": ""},
# # #                 "submitter": {"title": "提交人身份", "required": False, "default": ""}
# # #             }
# # #         )
# # #
# # #         error_rows = []
# # #         for item in items:
# # #             item.app_id = str(item.app_id)
# # #             if not check_file(item, self.attach_dir, self.file_format):
# # #                 error_rows.append(item.app_id)
# # #         if len(error_rows) > 0:
# # #             for e in error_rows:
# # #                 logger.info(f"资料文件有异常: {e}")
# # #             raise Exception("资料检查未通过")
# # #         logger.info("数据加载完成")
# # #         return items
# # #
# # #     def open_url(self):
# # #         self.driver.get("https://baoquan.court.gov.cn")
# # #         logger.info("打开网站:https://baoquan.court.gov.cn")
# # #
# # #     def login(self):
# # #         driver = self.driver
# # #         frame = driver.find_element_by_xpath(
# # #             '//*[@id="index"]/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/iframe')
# # #         driver.switch_to.frame(frame)
# # #         fill_input(driver, '//*[@id="root"]/div/form/div[1]/div[1]/div/div/div/input', self.username, '手机号码')
# # #         fill_input(driver, '//*[@id="root"]/div/form/div[1]/div[2]/div/div/div/input', self.password, '密码')
# # #         click(driver, '//*[@id="root"]/div/form/div/div[3]/span', '登录')
# # #         time.sleep(2)
# # #         for i in range(20):
# # #             cookies = self.driver.get_cookies()
# # #             time.sleep(1)
# # #             try:
# # #                 cookies[1]
# # #                 break
# # #             except:
# # #                 continue
# # #         self.cookie = f"Admin-Token={cookies[1].get('value')}; Admin-UserData={cookies[0].get('value')}"
# # #         self.bearer = cookies[1].get('value')
# # #
# # #     def prefun(self):
# # #         option = webdriver.ChromeOptions()
# # #         option.add_experimental_option('excludeSwitches', ['enable-automation'])
# # #         self.driver = webdriver.Chrome(options=option)
# # #         self.open_url()
# # #         self.login()
# # #
# # #     def run_job(self, item):
# # #         item.header = {}
# # #         u_a = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
# # #         cookie = self.cookie
# # #         bearer = self.bearer
# # #         item.cookie = cookie
# # #         item.bearer = bearer
# # #         item.bearer = bearer
# # #         item.header = {
# # #             "Cookie": cookie,
# # #             "Bearer": bearer,
# # #             "User-Agent": u_a
# # #         }
# # #         job = DoBaoQuanJob(self.driver, self.attach_dir, item, self.file_format)
# # #         job.run()
# # #
# # #     def reset(self):
# # #         self.afterfun()
# # #         time.sleep(1)
# # #         self.prefun()
# # #
# # #     def afterfun(self):
# # #         if self.driver:
# # #             self.driver.quit()
# # #
# # #
# # # export = ScriptDef(
# # #     cls=XJFYBaoQuanFlow,
# # #     group="外网保全系统",
# # #     title="保全申请-外网保全申请（黑龙江）",
# # #     arguments=[
# # #         FileItem(title="excel表格", name="excel_file"),
# # #         DirectoryItem(title="附件文件夹", name="attach_dir"),
# # #         UserSelectItem(title="账号", username_field="username", password_field="password"),
# # #         StringItem(title="文件格式（借款协议，就写借款协议）", name="file_format")
# # #     ]
# # # )
# # #
# # # if __name__ == '__main__':
# # #     flow = XJFYBaoQuanFlow(r"C:\Users\9000\Desktop\vvvv\外网保全申请样例\保全申请表头样例-8月-水区50.xlsx", r'C:\Users\9000\Desktop\vvvv\外网保全申请样例\资料样例', '17633602179',
# # #                            'mimashisha555...', "贷款合同")
# # #     flow.run()
# #
# # from datetime import datetime
# # ssss = [{'进件号': '1', '受理法院市': '宁波', '法院名称': '宁波市鄞州区人民法院', '申请人单位': '宁波银行股份有限公司',
# #          '申请人信用代码': '91330200711192037M', '申请人法定人': '陆华裕', '申请人证件号': '330203196409130032',
# #          '申请人手机号': 13819823262, '申请人单位地址': '浙江省宁波市鄞州区福明街道宁东路345号',
# #          '事务所': '浙江宇豪律师事务所', '代理人1姓名': '金典炫', '代理人1联系电话': 15382301752,
# #          '代理人1执业证号': '13302202110360708', '代理人1身份证号码': '330211199701210092',
# #          '代理人1户籍地址': '浙江省宁波市鄞州区福明街道宁东路345号宁波银行股份有限公司', '代理人2姓名': '蔡璐莹',
# #          '代理人2联系电话': 15267850343, '代理人2执业证号': '13302202011189886',
# #          '代理人2身份证号码': '330624199510281123',
# #          '代理人2户籍地址': '浙江省宁波市鄞州区福明街道宁东路345号宁波银行股份有限公司',
# #          '代理人送达地址': '浙江省宁波市鄞州区宁穿路1811号', '被申请人姓名': '陈东东',
# #          '被申请人证件号': '33028219910409919X', '被申请人手机号': 13476167311,
# #          '被申请人地址': '浙江省慈溪市周巷镇三江口村协同心', '被申请人民族': '汉族', '案由': '金融借款合同纠纷',
# #          '诉讼请求': '判令被告立即归还原告贷款本金人民币164798.04元，期内利息9514.29元，逾期利息37447.17元(暂算至2023年02月08日止，此后按年利率22.5%计算至款项实际清偿之日止)，以上暂合计为211759.5元；',
# #          '事实与理由': '原告与各被告分别签订《直接贷专用最高额借款合同》各一份，约定在本合同的有效期内，贷款人在最高贷款限额内，可根据借款人的申请及其借款条件和贷款人的经营状况，决定对借款人一次或分次发放贷款。具体发放的每笔贷款的种类、币种、金额、期限、用途、利率和还款方式等以相应的借款借据及其附件（若有）（包括电子银行借据，下同）记载为准，借款人对此无异议。借款借据是本合同不可分割的组成部分。原告与各被告签订合同的时间详见附表一。原、被告约定，借款人确认接受案涉电子合同，与在纸质合同上手写签字或盖章具有同等法律效力，双方无需另行签署纸质合同或文书。根据各被告的申请，原告向各被告发放贷款，具体发放的每笔贷款的具体金额、借款期限、利率、还款方式、欠款金额详见附表一。现上述各被告已经逾期欠息，未能按合同约定足额归还本息，各被告的行为已违反双方约定，构成违约。原告为维护自身合法权益，依据相关法律法规的规定向贵院提起诉讼，望判如所请。',
# #          '证据名称1': '借款合同',
# #          '证据目的1': '原告向被告借款，就原、被告双方的权利义务、最高贷款限额、被告履行债务的期限和计息方式等做了详细约定。',
# #          '证据名称2': '借款借据', '证据目的2': '被告的用款事实。', '证据名称3': '利息清单',
# #          '证据目的3': '被告的利息计算方式。', '证据名称4': '流水清单', '证据目的4': '被告的尚欠贷款本息金额。',
# #          '保全请求事项': '保全请求事项', '财产线索1': '财付通账户', '财产线索2': '支付宝账户',
# #          '保全事实与理由': '保全事实与理由'},
# #         {'进件号': '2', '受理法院市': '宁波', '法院名称': '宁波市鄞州区人民法院', '申请人单位': '宁波银行股份有限公司',
# #          '申请人信用代码': '91330200711192037M', '申请人法定人': '陆华裕', '申请人证件号': '330203196409130032',
# #          '申请人手机号': '13819823262', '申请人单位地址': '浙江省宁波市鄞州区福明街道宁东路345号',
# #          '事务所': '浙江宇豪律师事务所', '代理人1姓名': '金典炫', '代理人1联系电话': '15382301752',
# #          '代理人1执业证号': '13302202110360708', '代理人1身份证号码': '330211199701210092',
# #          '代理人1户籍地址': '浙江省宁波市鄞州区福明街道宁东路345号宁波银行股份有限公司', '代理人2姓名': '蔡璐莹',
# #          '代理人2联系电话': '15267850343', '代理人2执业证号': '13302202011189886',
# #          '代理人2身份证号码': '330624199510281123',
# #          '代理人2户籍地址': '浙江省宁波市鄞州区福明街道宁东路345号宁波银行股份有限公司',
# #          '代理人送达地址': '浙江省宁波市鄞州区宁穿路1811号', '被申请人姓名': '陈宫星',
# #          '被申请人证件号': '331082199004274256', '被申请人手机号': 15669266207,
# #          '被申请人地址': '浙江省临海市沿江镇上百岩村69号', '被申请人民族': '汉族', '案由': '金融借款合同纠纷',
# #          '诉讼请求': '判令被告立即归还原告贷款本金人民币3402.46元，期内利息161.56元，逾期利息1221.82元(暂算至2023年02月08日止，此后按年利率18.9%计算至款项实际清偿之日止)，以上暂合计为4785.84元；',
# #          '事实与理由': '原告与各被告分别签订《直接贷专用最高额借款合同》各一份，约定在本合同的有效期内，贷款人在最高贷款限额内，可根据借款人的申请及其借款条件和贷款人的经营状况，决定对借款人一次或分次发放贷款。具体发放的每笔贷款的种类、币种、金额、期限、用途、利率和还款方式等以相应的借款借据及其附件（若有）（包括电子银行借据，下同）记载为准，借款人对此无异议。借款借据是本合同不可分割的组成部分。原告与各被告签订合同的时间详见附表一。原、被告约定，借款人确认接受案涉电子合同，与在纸质合同上手写签字或盖章具有同等法律效力，双方无需另行签署纸质合同或文书。根据各被告的申请，原告向各被告发放贷款，具体发放的每笔贷款的具体金额、借款期限、利率、还款方式、欠款金额详见附表一。现上述各被告已经逾期欠息，未能按合同约定足额归还本息，各被告的行为已违反双方约定，构成违约。原告为维护自身合法权益，依据相关法律法规的规定向贵院提起诉讼，望判如所请。',
# #          '证据名称1': '借款合同',
# #          '证据目的1': '原告向被告借款，就原、被告双方的权利义务、最高贷款限额、被告履行债务的期限和计息方式等做了详细约定。',
# #          '证据名称2': '借款借据', '证据目的2': '被告的用款事实。', '证据名称3': '利息清单',
# #          '证据目的3': '被告的利息计算方式。', '证据名称4': '流水清单', '证据目的4': '被告的尚欠贷款本息金额。',
# #          '保全请求事项': '保全请求事项', '财产线索1': '财付通账户', '财产线索2': '支付宝账户',
# #          '保全事实与理由': '保全事实与理由'}]
# # lis = []
# # for i in ssss:
# #     dic = {}
# #     dic["id"] = "xxxxx"
# #     dic["ssdw"] = "1"
# #     dic["dlrlb"] = "1"
# #     dic["wtdlrlb"] = "1"
# #     dic["xm"] = ssss[0]["代理人1姓名"]
# #     dic["sws"] = ssss[0]["事务所"]
# #     dic["lxdh"] = ssss[0]["代理人1联系电话"]
# #     dic["zyzh"] = ssss[0]["代理人1执业证号"]
# #     dic["sfzh"] = ssss[0]["代理人1身份证号码"]
# #     dic["zrrid"] = ""
# #     dic["zzjgid"] = "1267065",
# #     dic["sftdsrsj"] = "2;1267065;1",
# #     dic["sddz"] = ssss[0]["代理人1户籍地址"]
# #
# #     lis.append(dic)
# # print(lis)
# #
# # a = [{
# #     "dwlx": "1",
# #     "id": "1836645",
# #     "xm": "陈东东",
# #     "zjlx ": "1 ",
# #     "zjhm": "330282199104099192",
# #     "xb": "1",
# #     "mz": "1 ",
# #     "gjhdq": "1 ",
# #     "csrq": "1991 - 04 - 09 ",
# #     "sf": "",
# #     "gzdw": "",
# #     "lxdh": "13476167311 ",
# #     "yzbm": "",
# #     "dzyx": "",
# #     "xzz": "",
# #     "sddz": "",
# #     "hjxxdz ": "浙江省慈溪市周巷镇三江口村协同心"
# # }, {
# #     "dwlx": "1 ",
# #     "id": "1836654 ",
# #     "xm": "陈宫星",
# #     "zjlx": "1 ",
# #     "zjhm": "331082199004274256 ",
# #     "xb": "1 ",
# #     "mz": "1 ",
# #     "gjhdq": "1 ",
# #     "csrq": "1990 - 04 - 27 ",
# #     "sf": "",
# #     "gzdw": "",
# #     "lxdh": "15669266207 ",
# #     "yzbm": "",
# #     "dzyx": "",
# #     "xzz": "",
# #     "sddz": "",
# #     "hjxxdz": "浙江省临海市沿江镇上百岩村69号"
# # }],
# a = "123456789"
# a = a[:-3]
# print(a)
import pandas as pd
lists = []
file = r"D:\cs\1.xlsx"
df = pd.read_excel(file, converters={})
g = df.drop_duplicates(subset="序号")
for name in g.index:
    data = df.loc[name].to_dict()
    lists.append(data)
print(lists)





