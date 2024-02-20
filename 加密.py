''' md5加密'''
import hashlib
import time
import base64
# print(time.time())
# while True:
#     a = input("请输入加密：")
#     x = hashlib.md5()
#     x.update(a.encode(encoding='utf8'))
#     print('加密前' + a)
#     print('加密后' + x.hexdigest())
#
# #
# ''' base64加密'''
# import base64
#
# a = input("请输入加密字符：")
# b = base64.b64encode(a.encode('utf8'))
# c = base64.b64decode(b)
# print('加密后：' + b.decode())
# print('解密后：' + c.decode())
#
#
# ''' 哈希+sha256加密'''
import hashlib
#
s = hashlib.sha256()
a = "ff417e26-26-73bf-4b7c-b7fe-912d0c3aaa36"
s.update(a).encode('gbk')
b = s.hexdigest()
print(b)

# a = '091MWt0w3zbekY2v1p2w3Gz6Hf2MWt06'
# '041C0SFa1yRAYC0wZdHa1lxQiS2C0SFe'
# '011jHh000ClJEN1XEe300YCnxc0jHh0g'
'011Vj100054tEN10m9300eYFff1Vj10w'

a = "ff417e26-26-73bf-4b7c-b7fe-912d0c3aaa36"


'''不是md5'''
# a = int(time.time()*1000)
# x = hashlib.md5()
# print('加密后' + x.hexdigest())
# 041XKN000co7EN16DF10038jf03XKN0R
# d41d8cd98f00b204e9800998ecf8427e

'''不是哈希'''
# s = hashlib.sha256()
# a = "ff417e26-26-73bf-4b7c-b7fe-912d0c3aaa36"
# s.update(a)
# b = s.hexdigest()
# print(b)

'''不是base64'''
# a = input("请输入加密字符：")
# b = base64.b64encode(a.encode('utf8'))
# c = base64.b64decode(b)
# print('加密后：' + b.decode())
# print('解密后：' + c.decode())


# # print(bool(type(Ellipsis)))
# a = [
#     ['1', 'www', '123'],
#     ['2', "sss", '456'],
#     ["3", "xxx", '789'],
#     ["4", "qqq", '852']
# ]
#
#
# # for x, y, z in a:
# #     print(x)
# #     print(y)
# #     print(z)
# ss = zip(a[0], a[1], a[2], a[3])
# for i in ss:
#     for e in list(i):
#         print(e)
# # if (length := len(a) > 0):
# #     print(length)
