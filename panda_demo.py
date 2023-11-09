from typing import List, Dict

import pandas as pd
from log import logger
from functools import singledispatch


class ReadExcel():
    """
        返回df，适用于程序运行后数据填写到原表中
    """

    def __init__(self, excel):
        self.excel = excel
        self.df = pd.read_excel(self.excel, dtype="string")

    def init_data(self):
        self.df.dropna(axis=0, how='all', subset=None, inplace=True)
        self.df.dropna(axis=1, how='all', subset=None, inplace=True)
        self.df.fillna("", inplace=True)
        logger.info(f"{self.df.columns =}")
        if '收案编号' not in self.df.columns:
            self.df["收案编号"] = ""
        if "保全裁定类型" not in self.df.columns:
            self.df["保全裁定类型"] = ""
        if '结果' not in self.df.columns:
            self.df["结果"] = ""
        if "被申请人验证结果" not in self.df.columns:
            self.df["被申请人验证结果"] = ""
        if "是否被其他案件关联" not in self.df.columns:
            logger.info('是否被其他案件关联 不存在！')
            self.df["是否被其他案件关联"] = ""
        if "法定代表人证件种类" not in self.df.columns:
            self.df["法定代表人证件种类"] = ""
        if "法定代表人姓名" not in self.df.columns:
            self.df["法定代表人姓名"] = ""
        if "法定代表人证件号码" not in self.df.columns:
            self.df["法定代表人证件号码"] = ""

        for i in self.df.columns:
            self.df[i] = self.df[i].astype(str)
        print(self.df.columns)
        try:
            self.df.to_excel(self.excel, index=False)
        except Exception as e:
            raise Exception("请关闭表格")

    def check_head(self, data: list):
        head = list(set(data) - set(self.df.columns))
        assert not head, f"{head}表头不存在"


def read_excels(excel_path, title_list, one_value):
    """
        适用于写入新表格,返回列表套字典
        excel_path: 读取表格路径
        title_list: 需要核查的表头，需要传入列表
        one_value: 每行数据的唯一值
    """

    df = pd.read_excel(excel_path, dtype="string")
    error = ",".join(filter(lambda _: _ not in df.columns, title_list))
    assert not error, f"表头缺失：{error}, 请检查excel表头数据！"
    return df.drop_duplicates(one_value).to_dict('records')


def wright_excel(result, save_path):
    """
        result: 必须为列表套列表格式  eg: [["案号"，"结果"],[”xxx“， ”成功“],[”xxx“， ”成功“]]
        save_path: 写入excel的地址
    """
    df = pd.DataFrame(result[1:], columns=result[0], dtype="string")
    df.to_excel(save_path, index=False)


def wright_excel1(result: list, save_path):
    """
        result: 必须为列表套列表格式  eg: [["案号"，"结果"],[”xxx“， ”成功“],[”xxx“， ”成功“]]
        save_path: 写入excel的地址
    """
    pd.DataFrame(data=result, dtype=str).to_excel(save_path, index=False)

