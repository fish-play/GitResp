"""
-*- coding: utf-8 -*-
@Time : 2022/9/7 16:51
"""
import base64
import datetime
import json
import random
import time

import requests
from rpalib.log import logger
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from flows.flow import ListDataFlow, ScriptDef, FileItem, DirectoryItem, SelectItem
from rpalib import excel


class Item(object):
    # '申请保全金额'
    sqdbje: str
    # 申请人单位
    sqrdw: str
    # 申请人信用代码
    sqrxydm: str
    # 申请人法定人
    sqrfr: str
    # 申请人手机号
    sqrsjh: str
    # 申请人单位地址
    sqrdz: str
    # 被申请人姓名
    dsrxm: str
    # 被申请人手机号（手机号
    dsrsjhm: str
    # 被申请人证件号
    dsrzjh: str
    # 进件号
    dbid: str
    # 代理人律所
    dlrszls: str
    # '代理人姓名(非必填)'
    dlrxm: str
    # 代理人证件号(非必填)
    dlrzjh: str
    # 代理人手机号(非必填)
    dlrsjhm: str
    # 代理人执行号(非必填)
    dlrzjhm: str
    # 咨询员编号(非必填)
    zxybh: str
    # 民族
    dsrmz: str


class Excel_extract(ListDataFlow):
    def __init__(self, excel_file, environment) -> None:
        super().__init__()
        self.excel_file = excel_file
        self.environment = environment
        # 全国地区代码(身份证前两位)
        self.area_code = {
            "北京": "11",
            "天津": "12",
            "河北": "13",
            "山西": "14",
            "内蒙古": "15",
            "辽宁": "21",
            "吉林": "22",
            "黑龙江": "23",
            "上海": "31",
            "江苏": "32",
            "浙江": "33",
            "安徽": "34",
            "福建": "35",
            "江西": "36",
            "山东": "37",
            "河南": "41",
            "湖北": "42",
            "湖南": "43",
            "广东": "44",
            "广西": "45",
            "海南": "46",
            "四川": "51",
            "贵州": "52",
            "云南": "53",
            "西藏": "54",
            "重庆": "50"
        }

    def row2dict(self, row, toprow):
        d = {}
        for i in range(0, len(row)):
            d[toprow[i].value] = row[i].value
        return d

    def get_excel_data(self):
        return excel.loads(
            self.excel_file, Item, {
                'sqdbje': {'title': '申请保全金额', 'required': True},
                'sqrdw': {'title': '申请人单位', 'required': True},
                'sqrxydm': {'title': '申请人信用代码', 'required': True},
                'sqrfr': {'title': '申请人法定人', 'required': True},
                'sqrsjh': {'title': '申请人手机号', 'required': True},
                'sqrdz': {'title': '申请人单位地址', 'required': True},
                'dbid': {'title': '进件号', 'required': True},  # ????(要保证是唯一值)
                'dsrxm': {'title': '被申请人姓名', 'required': True},
                'dsrsjhm': {'title': '被申请人手机号', 'required': True},
                'dsrzjh': {'title': '被申请人证件号', 'required': True},
                'ms': {'title': '描述', 'required': True},
                'ccjz': {'title': '财产价值', 'required': True},
                'dsrjcjzd': {'title': '被申请人地址', 'required': True},
                'area': {'title': '业务发生地区', 'required': True},
                'dlrszls': {'title': '代理人律所', 'required': False},
                'dlrxm': {'title': '代理人姓名', 'required': False},
                'dlrzjh': {'title': '代理人证件号', 'required': False},
                'dlrsjhm': {'title': '代理人手机号', 'required': False},
                'dlrzjhm': {'title': '代理人执行号', 'required': False},
                'zxybh': {'title': '咨询员编号', 'required': False},
                'dsrmz': {'title': '民族', 'required': False},
            })

    def get_birthday(self):
        # 通过身份证号获取出生日期
        if self.birth_month <= 9:
            new_birth_month = f'0{self.birth_month}'
            birthday = "{0}-{1}-{2}".format(self.birth_year, new_birth_month, self.birth_day)
        else:
            birthday = "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)
        return birthday

    def get_sex(self):
        # 男生：1 女生：0
        sex = {1: "男", 0: "女"}
        num = int(self.id[16:17])
        if num % 2 == 0:
            return sex[0]
        else:
            return sex[1]

    def get_age(self):
        # 获取年龄
        now = (datetime.datetime.now() + datetime.timedelta(days=1))
        year = now.year
        month = now.month
        day = now.day

        if year == self.birth_year:
            return 0
        else:
            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):
                return year - self.birth_year - 1
            else:
                return year - self.birth_year

    def get_id_details(self, id):
        self.id = id
        self.birth_year = int(self.id[6:10])
        self.birth_month = int(self.id[10:12])
        self.birth_day = int(self.id[12:14])
        birthday = self.get_birthday()
        sex = self.get_sex()
        age = self.get_age()
        return birthday, sex, age

    def get_data(self, item):
        birthday, sex, age = self.get_id_details(item.dsrzjh)
        # data_t = {"data": [{
        #     'sqdbje': item.sqdbje,
        #     'sqrdw': item.sqrdw,
        #     'sqrxydm': item.sqrxydm,
        #     'sqrfr': item.sqrfr,
        #     'sqrsjh': item.sqrsjh,
        #     'sqrdz': item.sqrdz,
        #     'dbid': str(item.dbid),  # ???? 进件号(要保证是唯一值)
        #     'dsrxm': item.dsrxm,
        #     'dsrxb': sex,
        #     'dsrcsrq': birthday,
        #     'dsrsjhm': item.dsrsjhm,
        #     'dsrzjh': item.dsrzjh,
        #     'dsrjcjzd': item.dsrjcjzd,  # 被申请人地址
        #     'dlrszls': item.dlrszls,
        #     'ms': item.ms,
        #     'ccjz': item.ccjz,
        #     # 非必填
        #     'dsrmz': item.dsrmz,
        #     'dlrxm': item.dlrxm,
        #     'dlrzjh': item.dlrzjh,
        #     'dlrsjhm': item.dlrsjhm,
        #     'dlrzjhm': item.dlrzjhm,
        #     'zxybh': item.zxybh,
        # }]}
        data_t = {
            'sqdbje': item.sqdbje,
            'sqrdw': item.sqrdw,
            'sqrxydm': item.sqrxydm,
            'sqrfr': item.sqrfr,
            'sqrsjh': item.sqrsjh,
            'sqrdz': item.sqrdz,
            'dbid': str(item.dbid),  # ???? 进件号(要保证是唯一值)
            'dsrxm': item.dsrxm,
            'dsrxb': sex,
            'dsrcsrq': birthday,
            'dsrsjhm': item.dsrsjhm,
            'dsrzjh': item.dsrzjh,
            'dsrjcjzd': item.dsrjcjzd,  # 被申请人地址
            'dlrszls': item.dlrszls,
            'ms': item.ms,
            'ccjz': item.ccjz,
            'area': self.area_code.get(item.area, ""),
            # 非必填
            'dsrmz': item.dsrmz,
            'dlrxm': item.dlrxm,
            'dlrzjh': item.dlrzjh,
            'dlrsjhm': item.dlrsjhm,
            'dlrzjhm': item.dlrzjhm,
            'zxybh': item.zxybh,
        }
        return data_t

    def encrypt_initialize(self):
        public_pem = None
        self.MAX_ENCRYPT_BLOCK = 117
        if self.environment == '测试环境':
            # 测试环境密钥
            public_pem = """-----BEGIN PUBLIC KEY-----
                MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCpDhIT5RgSWpHMUc/fO550r5SQZxZJiSmMBHASnFuR4gdLPQXlINCx9QaN
                +JO5C06ZajUkpxvZtpARt5s2r+7UWwZGqiRjJ6FrJW7EQSmwtfAodZrYVe+0hiLcVILMAjWNOh0LslKdHXyetdRwi1ztF5P
                +1gsTUP0gXuFpSZ6FHwIDAQAB
                -----END PUBLIC KEY-----"""
            logger.info('--->测试环境开始加密<---')
        elif self.environment == '生产环境':
            # 生产公钥
            public_pem = """-----BEGIN PUBLIC KEY-----
            MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCg5eKmPxBh6WA8hYfwooIVFVNpC92nvN5blQ0PaaAA+zbHfhDW2MDl
            /SWPZh2X50KBjomwFvpg74jKqaozOKtE9N58WdjzQlSANuUENWWz4yjBcHZBNdK24xLQpCsTldXEKm6z
            /ujJTUJUoWO7yBiTAVt68Fvu0F4Jz2OB++hF5QIDAQAB
            -----END PUBLIC KEY-----"""
            logger.info('--->生产环境开始加密<---')
        rsakey = RSA.importKey(public_pem)
        self.cipher = Cipher_pkcs1_v1_5.new(rsakey)

    def encrypt(self, message):
        # 加密
        src = message.encode("utf-8")
        offset = 0
        out = bytes()
        while offset < len(src):
            if offset + self.MAX_ENCRYPT_BLOCK >= len(src):
                b = src[offset: -1]
            else:
                b = src[offset: offset + self.MAX_ENCRYPT_BLOCK]

            dest = self.cipher.encrypt(b)
            out += dest
            offset += self.MAX_ENCRYPT_BLOCK
        new_out = base64.b64encode(out).decode("utf-8")
        return new_out

    def post_data(self, data):
        # post 发送数据
        url = None
        if self.environment == '测试环境':
            url = 'http://esbtest.zsins.com:8866/11000000001/HanZiAppiyInsurance/V1'
        elif self.environment == '生产环境':
            url = 'https://esb.zsins.com/11000000001/HanZiAppiyInsurance/V1'  # 正式环境接口
        logger.info(f'要发送的data:{data}')
        head = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}
        time.sleep(random.randint(1, 3))
        return_c = requests.post(url=url, data=data, headers=head)
        logger.info(f'返回的状态码：{return_c}, 接口返回的信息：{return_c.text}')

    def run(self):
        self.encrypt_initialize()
        # try:
        data_list = []
        items = self.get_excel_data()
        for item in items:
            logger.info(f'{item.dsrxm}:-->开始处理')
            data = self.get_data(item)
            logger.info(f'拼接出的data：{data}')
            data_list.append(data)
        content_encryption = json.dumps({"data": data_list}, ensure_ascii=False)
        encrypt_data = self.encrypt(content_encryption + "}")
        logger.info(f"要加密的列表总数----> {len(data_list)}")
        self.post_data(encrypt_data)


export = ScriptDef(
    cls=Excel_extract,
    group="外网保全系统",
    title="new_浙商保全数据推送",
    arguments=[
        FileItem(title="excel表格", name="excel_file"),
        SelectItem(title="环境选择", name="environment", options=[
            '测试环境', '生产环境'
        ]),
    ]
)

if __name__ == '__main__':
    excel_file = r'C:\Users\9000\Desktop\【10-14】200自动化脚本-10月-灵丘县维信500 - 副本 - 副本.xlsx'
    # excel_file = r'C:\Users\9000\Desktop\【10-14】200自动化脚本-10月-灵丘县维信500 - 副本(1).xlsx'
    Excel_extract(excel_file, '测试环境').run()