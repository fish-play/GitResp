# from lxml import etree
# import requests
#
# url = 'https://www.xiachufang.com/category/40076/'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
#     'Cookie': 'bid=Nd5VVXOh',
#     'Referer': 'https://www.xiachufang.com/category/40076/?page=2'
# }
# response = requests.get(url=url, headers=headers)
# htm = response.content.decode()
# # print(htm)
# p_list = etree.HTML(htm)
# # print(p_list)
# ff = p_list.xpath('/html/body/div[4]/div/div/div[1]/div[1]/div/div[2]/div[2]/ul/li/div/div/p[1]/a/text()')
# print(ff)
# for i in ff:
#     print(i)

# #
# from lxml import etree
# import requests
#
# url = 'https://baoquan.court.gov.cn'
# heeaders = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
#     'Cookie': 'Admin-Token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMTE2MTE5MTU5Nzg4NDAzIiwibmJmIjoxNjQ3OTMwMTAzLCJpZGNhcmQiOiIzNDAxMjIxOTg5MDcyMDMzNTgiLCJ1c2Vyc291cmNlIjoxLCJleHAiOjE2NDc5NTg5MDMsImlhdCI6MTY0NzkzMDEwM30.535kOUrHuu7C-gubcwDDZGkI8sQW6WjrMKSvL1B5CSfXsE43dXrQY38tm55ovEkJaBBYStDd38eS5fq9KttN5w; Admin-UserData={%22cUserid%22:%221116119159788403%22%2C%22cLoginName%22:%2213955193847%22%2C%22cZjlx%22:%221%22%2C%22cZjh%22:%22340122198907203358%22%2C%22cMz%22:%221%22%2C%22cUsertype%22:%221%22%2C%22cCardname%22:%22%E4%BD%99%E6%B4%AA%E4%BC%9F%22%2C%22cPhoneno%22:%2213955193847%22%2C%22cEmail%22:null%2C%22cTxdz%22:%22%E9%A9%AC%E9%9E%8D%E5%B1%B1%E5%B8%82%E9%9B%A8%E5%B1%B1%E5%8C%BA%E4%B9%9D%E5%8D%8E%E8%A5%BF%E8%B7%AF1369%E5%8F%B79%E6%A0%8B206%22%2C%22cDwdz%22:null%2C%22cDwmc%22:null%2C%22cGh%22:%22%22%2C%22cCertification%22:%22true%22%2C%22cQyfr%22:null%2C%22cBirthdate%22:%221989-07-20%22%2C%22cSex%22:%221%22%2C%22nAge%22:31%2C%22cDwxz%22:null%2C%22cFridentity%22:null%2C%22cUscc%22:null%2C%22nUsersource%22:1%2C%22nZzlx%22:null}',
#     'Bearer': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMTE2MTE5MTU5Nzg4NDAzIiwibmJmIjoxNjQ3OTMwMTAzLCJpZGNhcmQiOiIzNDAxMjIxOTg5MDcyMDMzNTgiLCJ1c2Vyc291cmNlIjoxLCJleHAiOjE2NDc5NTg5MDMsImlhdCI6MTY0NzkzMDEwM30.535kOUrHuu7C-gubcwDDZGkI8sQW6WjrMKSvL1B5CSfXsE43dXrQY38tm55ovEkJaBBYStDd38eS5fq9KttN5w',
#     'Referer': 'https://baoquan.court.gov.cn/'
# }
# response = requests.get(url=url, headers=heeaders)
# htm = response.content.decode()
# p_list = etree.HTML(htm)
# for i in p_list:
#     print(i)

# import json
# import os
# from datetime import datetime
#
# from selenium import webdriver
# from selenium.webdriver.chrome.webdriver import WebDriver
# import time

# strs = '2'
# list2 = ['one', 'two', 'three', 'fore', 'five', 'six', 'seven']
#
# if strs == '2':
#     list = list2[0]
# else:
#     pass
# print(list)
# for i in range(1,6):
#     print(i)

# print(time.strftime("%Y-%m-%d ", time.localtime(time.time())))
# for i in range(1,100):
#     print(i)
# a = '2022-03-23'
# b = '2022-03-24'
# import time
# strftime = datetime.strptime("2017-11-02", "%Y-%m-%d")
#
# strftime2 = datetime.strptime("2017-01-04", "%Y-%m-%d")
#
# print(f"2017-11-02大于2017-01-04： {type(strftime)} ", strftime > strftime2)
# import os
#
# a = os.listdir(r'C:/Users/9000/Desktop/flask_port')
# for file in a:
#     f = open(r'C:/Users/9000/Desktop/flask_port' + "/" + file)
#     print(f)
# import requests
# url = 'http://httpbin.org/get'
# response = requests.get(url)
# # response.encoding='utf8'
# print(response.text)

# x = {1: {2: 2}}
# zz = [2, 3, 4]
#
# z = list(x.keys())[0]
# print(z)
import os
import shutil

# b = os.getcwd()
# print(b)
# c = os.mkdir(b+'\yyy')
# print(os.path.join(b, 'yyy'))
#
#
#
#
#
# a = r'C:\Users\9000\Desktop\CAS583804845702590550'
# b = r'C:\Users\9000\Desktop\复制后的文件夹'
# for i in os.listdir(a):
#     dirs = os.path.join(a, i)
#     shutil.copy(dirs, b)

# lj = r'\\172.29.9.15\资料管理prod\案件材料\CAS688785180631699488'
# dir_path = os.path.join(os.getcwd(), "lswj")
# if not os.path.exists(dir_path):
#     os.makedirs(dir_path)
# for i in os.listdir(lj):
#     dirs = os.path.join(lj, i)
#     shutil.copy(dirs, dir_path)
import os
# x = r"D:\RPA_PRO\rpa\scripts\lswj"
#
# print(os.path.abspath(os.path.join(x, "..")))
# dir_path = r'C:\Users\9000\Desktop\less'
#
# shutil.rmtree(dir_path)




# -*- coding: utf-8 -*-
# 2022/5/20 13:55
import requests
import time
import os
from lxml import etree


# def demo1():
#     url = 'https://opensea.io'
#     header = {
#         'cookie': 'VISITOR_INFO1_LIVE=VR_4QEnt4oI; __Secure-3PSID=IghuotTJznGpAc6VJ_80MVKYSfNUxYuubsFA_usQUEE5jQD5EnyylUTkbplRmR4JLZWkTg.; __Secure-3PAPISID=Z6LMjW_6_A469PxY/AmVFPl9IRo_JMxuKZ; LOGIN_INFO=AFmmF2swRAIgQN4FlhpWDdDreaDVrCJJTB0bxsNTtPkUcsorvPnGzK0CIGRbqnA4Hnu2CZzCWmlR6FhXM80WmLeplZwOeOkG0Z8r:QUQ3MjNmeXJwa3UwbVFKa0tVbUtNQmdGUUM2Ukk1LWdQTWp3M2x4TUlkb3h4NlNlamhOcjI3OWFJbThDWjc5MHlsN21ieDE2emtEZXdtQUh0STN3NDJGdVZuNnpsVFN5WUJDaGFGa2ZFM01XY00xM2QweWlHUnpBR2ljb1QwY0ZQeEZ0QS1KczBGTzNDbk9KTHNFLTVwVWZiM2hUNVlVRHVR; PREF=tz=Asia.Shanghai; YSC=9jwuDShsfwo; __Secure-3PSIDCC=AJi4QfF-Nylgdrs0shuELCC5Kd_dNc6RfCS7pNddb7UaCAegxPSB4O-u4nVVCo0bp_vjpcO9dQ',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
#         'referer': 'https://www.youtube.com/embed/gfGuPd1CELo?playlist=gfGuPd1CELo&autoplay=0&controls=1&loop=1&modestbranding=1&rel=0',
#         'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'no-cors',
#         'sec-fetch-site': 'same-origin',
#     }
#     proxies = {
#         'https': '127.0.0.1:54926',
#         'http': '127.0.0.1:54926'
#     }
#     response = requests.get(url=url, headers=header, proxies=proxies)
#     # response.encoding = 'gbk'
#     html = etree.HTML(response.text)
#     print(response)
#     print(html)
#     # img_src = html.xpath('')
# if __name__ == '__main__':
#     demo1()
# 遍历文件夹下的所有文件
# for i in os.listdir(self.pdf_path):
#     result = []
#     result2 = []
#     errmsg = []
#     result1 = {}
#     # 筛选出后缀为pdf的文件
#     if i.endswith(".pdf"):
#         doc = fitz.open(os.path.join(self.pdf_path, i))
#         result.append(i)
#         for page in doc:
#             text = page.getText()
#             ht_id = re.search("编号：(.*)", text)
#             if ht_id:
#                 if result1.get("编号",None) is None:
#                     result1['编号'] = ht_id.group()
#                 else:
#                     result2.append(result1)
#                     result1 = {}
#                     result1['编号'] = ht_id.group()
#
#             ht_zrr = re.search("甲方（转让人）：(.*)", text)
#             if ht_zrr:
#                 result1['转让人'] = ht_zrr.group()
#
#             jf_id = re.search('\d{17,18}', text)
#             if jf_id:
#                 result1['身份证号码'] = jf_id.group()
#
#             # c_money = re.search("借款本金数额：.*RMB：(.*)）", text, re.S)
#             c_money = re.findall("借款本金数额：.*RMB：(.*)）借款",text,flags=re.S)
#             if c_money:
#                 result1['借款本金数额'] = c_money
#
#
# bd_money = re.search("标的债权本金：(.*?)\（RMB：(.*?)\）", text, re.S)
#
# if bd_money:
#     result.append(bd_money.group().strip(' \n'))
# else:
#     result.append("")
#
#
# print(len(result2))
# print(result2)
# import requests

#
# import requests
# from lxml import etree
#
#
# url = "https://lsfwpt.zjcourt.cn/lsfwpt/showTiff?isPdf=0&wjgs=pdf&textSend=%257B%27RequestMethod%27:%27downloadAknewJftzs%27,%27data%27:%257B%27yjje_urid%27:%27b255d7d27b2f458ca5ea508cc5870844%27,%27wsbh%27:%272%27,%27filename%27:%279cb64342607f4a86b78964ce6d488e9a_2%27%257D%257D&sjhm=15382301752&userName=JXU5MUQxJXU1MTc4JXU3MEFC"
# header = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36',
#     'Cookie': 'JSESSIONID=A4550FA6B44C7763269529D3EA059559; JSESSIONID=9190298E870EA6728BE2A34F1C127C4B'
# }
# response = requests.get(url, headers=header)
# # print(response)
# html_ = response.content
# print(html_)

# from Crypto.Cipher import AES
#
# import base64
#
# password = 'qnbyzzwmdgghmcnm'.encode() # 秘钥
#
# #秘钥：必须是16位字节或者24位字节或者32位字节（因为python3的字符串是unicode编码，需要encode才可以转换成字节型数据）
#
# text = '999321' #需要加密的内容
#
# while len(text.encode('utf-8')) % 16 != 0:  #如果text不⾜16位的倍数就⽤空格补⾜为16位
#         text += '\0'
#
# text=text.encode()
#
# model = AES.MODE_ECB #定义模式
#
# #模式：
#
# #电码本模式（Electronic Codebook Book (ECB)）
#
# #密码分组链接模式（Cipher Block Chaining (CBC)）
#
# #计算器模式（Counter (CTR)）
#
# #密码反馈模式（Cipher FeedBack (CFB)）
#
# #输出反馈模式（Output FeedBack (OFB)）
#
# aes = AES.new(password,model) #创建⼀个aes对象
#
# en_text = aes.encrypt(text) #加密明⽂
#
# #b'\x0b\x0f.\x1fc\x83-/\xac\x04#\x89Qs\x8c\xec'
#
# en_text = base64.encodebytes(en_text) #将返回的字节型数据转进⾏base64编码
#
# #b'Cw8uH2ODLS+sBCOJUXOM7A==\n'
#
# en_text = en_text.decode('utf8') #转换成python中的字符串类型
#
# #Cw8uH2ODLS+sBCOJUXOM7A==
#
# print(en_text)
#



import base64
# from Cryptodome.Cipher import AES
from Crypto.Cipher import AES


# 需要补位，str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)


# 加密方法
def aes_encrypt(key, t, iv):
    aes = AES.new(add_to_16(key), AES.MODE_CBC, add_to_16(iv))  # 初始化加密器
    encrypt_aes = aes.encrypt(add_to_16(t))                    # 先进行 aes 加密
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回 bytes
    return encrypted_text


# 解密方法
def aes_decrypt(key, t, iv):
    aes = AES.new(add_to_16(key), AES.MODE_CBC, add_to_16(iv))         # 初始化加密器
    base64_decrypted = base64.decodebytes(t.encode(encoding='utf-8'))  # 优先逆向解密 base64 成 bytes
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')  # 执行解密密并转码返回str
    return decrypted_text


if __name__ == '__main__':
    secret_key = 'qnbyzzwmdgghmcnm'   # 密钥
    text = '999321!'   # 加密对象
    iv = secret_key           # 初始向量
    encrypted_str = aes_encrypt(secret_key, text, iv)
    print('加密字符串：', encrypted_str)
    decrypted_str = aes_decrypt(secret_key, encrypted_str, iv)
    print('解密字符串：', decrypted_str)












