"""
-*- coding: utf-8 -*-
@Time : 2022/11/18 12:41
"""
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
url = "http://ggzy.zwfwb.tj.gov.cn/jyxxzfcg/index.jhtml"

response = requests.get(url, headers=headers).text
print(response)
