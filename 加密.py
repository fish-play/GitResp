# ''' md5加密'''
# import hashlib
# import time
# import base64
# # print(time.time())
# # while True:
# #     a = input("请输入加密：")
# #     x = hashlib.md5()
# #     x.update(a.encode(encoding='utf8'))
# #     print('加密前' + a)
# #     print('加密后' + x.hexdigest())
# #
# # #
# # ''' base64加密'''
# # import base64
# #
# # a = input("请输入加密字符：")
# # b = base64.b64encode(a.encode('utf8'))
# # c = base64.b64decode(b)
# # print('加密后：' + b.decode())
# # print('解密后：' + c.decode())
# #
# #
# # ''' 哈希+sha256加密'''
# import hashlib
# #
# s = hashlib.sha256()
# a = "ff417e26-26-73bf-4b7c-b7fe-912d0c3aaa36"
# s.update(a).encode('gbk')
# b = s.hexdigest()
# print(b)
#
# # a = '091MWt0w3zbekY2v1p2w3Gz6Hf2MWt06'
# # '041C0SFa1yRAYC0wZdHa1lxQiS2C0SFe'
# # '011jHh000ClJEN1XEe300YCnxc0jHh0g'
# '011Vj100054tEN10m9300eYFff1Vj10w'
#
# a = "ff417e26-26-73bf-4b7c-b7fe-912d0c3aaa36"
#
#
# '''不是md5'''
# # a = int(time.time()*1000)
# # x = hashlib.md5()
# # print('加密后' + x.hexdigest())
# # 041XKN000co7EN16DF10038jf03XKN0R
# # d41d8cd98f00b204e9800998ecf8427e
#
# '''不是哈希'''
# # s = hashlib.sha256()
# # a = "ff417e26-26-73bf-4b7c-b7fe-912d0c3aaa36"
# # s.update(a)
# # b = s.hexdigest()
# # print(b)
#
# '''不是base64'''
# # a = input("请输入加密字符：")
# # b = base64.b64encode(a.encode('utf8'))
# # c = base64.b64decode(b)
# # print('加密后：' + b.decode())
# # print('解密后：' + c.decode())
#
#
# # # print(bool(type(Ellipsis)))
# # a = [
# #     ['1', 'www', '123'],
# #     ['2', "sss", '456'],
# #     ["3", "xxx", '789'],
# #     ["4", "qqq", '852']
# # ]
# #
# #
# # # for x, y, z in a:
# # #     print(x)
# # #     print(y)
# # #     print(z)
# # ss = zip(a[0], a[1], a[2], a[3])
# # for i in ss:
# #     for e in list(i):
# #         print(e)
# # # if (length := len(a) > 0):
# # #     print(length)
import execjs
from cryptography.hazmat.backends import default_backend

js_code = ("""


var JSEncrypt = function (options) {
  options = options || {};
  this.default_key_size = parseInt(options.default_key_size) || 1024;
  this.default_public_exponent = options.default_public_exponent || '010001'; //65537 default openssl public exponent for rsa key type
  this.log = options.log || false;
  // The private and public key.
  this.key = null;
};

JSEncrypt.prototype.setPublicKey = function(t) {
        this.setKey(t);
    }

function getTimes() {
        var e = "mimashisha555...";
        var t = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5GVku07yXCndaMS1evPIPyWwhbdWMVRqL4qg4OsKbzyTGmV4YkG8H0hwwrFLuPhqC5tL136aaizuL/lN5DRRbePct6syILOLLCBJ5J5rQyGr00l1zQvdNKYp4tT5EFlqw8tlPkibcsd5Ecc8sTYa77HxNeIa6DRuObC5H9t85ALJyDVZC3Y4ES/u61Q7LDnB3kG9MnXJsJiQxm1pLkE7Zfxy29d5JaXbbfwhCDSjE4+dUQoq2MVIt2qVjZSo5Hd/bAFGU1Lmc7GkFeLiLjNTOfECF52ms/dks92Wx/glfRuK4h/fcxtGB4Q2VXu5k68e/2uojs6jnFsMKVe+FVUDkQIDAQAB";
        var o = new JSEncrypt;
        o.setPublicKey(t);
        return encodeURIComponent(ssss(e))
"""
)
# js_code = ("""
#
#
# var xxx = function(t) {
#         try {
#             return be(this.getKey().encrypt(t))
#         } catch (e) {
#             return !1
#         }
#     }
#
# var ssss = function(t) {
#         this.setKey(t)
#     }
#
# var qqq = function(t) {
#         t = t || {},
#         this.default_key_size = parseInt(t.default_key_size) || 1024,
#         this.default_public_exponent = t.default_public_exponent || "010001",
#         this.log = t.log || !1,
#         this.key = null
#     };
#
# function getTimes() {
#         var e = "mimashisha555...";
#         var t = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5GVku07yXCndaMS1evPIPyWwhbdWMVRqL4qg4OsKbzyTGmV4YkG8H0hwwrFLuPhqC5tL136aaizuL/lN5DRRbePct6syILOLLCBJ5J5rQyGr00l1zQvdNKYp4tT5EFlqw8tlPkibcsd5Ecc8sTYa77HxNeIa6DRuObC5H9t85ALJyDVZC3Y4ES/u61Q7LDnB3kG9MnXJsJiQxm1pLkE7Zfxy29d5JaXbbfwhCDSjE4+dUQoq2MVIt2qVjZSo5Hd/bAFGU1Lmc7GkFeLiLjNTOfECF52ms/dks92Wx/glfRuK4h/fcxtGB4Q2VXu5k68e/2uojs6jnFsMKVe+FVUDkQIDAQAB";
#         var o = new JSEncrypt;
#         o.setPublicKey(t)
#         return encodeURIComponent(ssss(e))
#     }
# """
# )

runtime = execjs.get()
context = runtime.compile(js_code)
result = context.call("getTimes")
print(result)

# from cryptography.fernet import Fernet
# import base64
#
#
# e = "mimashisha555..."
# t = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5GVku07yXCndaMS1evPIPyWwhbdWMVRqL4qg4OsKbzyTGmV4YkG8H0hwwrFLuPhqC5tL136aaizuL/lN5DRRbePct6syILOLLCBJ5J5rQyGr00l1zQvdNKYp4tT5EFlqw8tlPkibcsd5Ecc8sTYa77HxNeIa6DRuObC5H9t85ALJyDVZC3Y4ES/u61Q7LDnB3kG9MnXJsJiQxm1pLkE7Zfxy29d5JaXbbfwhCDSjE4+dUQoq2MVIt2qVjZSo5Hd/bAFGU1Lmc7GkFeLiLjNTOfECF52ms/dks92Wx/glfRuK4h/fcxtGB4Q2VXu5k68e/2uojs6jnFsMKVe+FVUDkQIDAQAB"
# # 假设有一个类似的加密函数（这里的例子用 Fernet 对比）
# def encrypt_string(plaintext, key):
#     f = Fernet(key)
#     encrypted_text = f.encrypt(plaintext.encode())
#     return base64.urlsafe_b64encode(encrypted_text).decode()
#
# # 把 JS 公钥转换为 bytes
#
# public_key_bytes = base64.urlsafe_b64decode(t)
#
# # 假设你有 `ssss` 的等效函数，比如直接使用加密库
# def python_ssss(e, public_key):
#     # 使用加密库中的加密方法
#     encrypted_e = encrypt_string(e, public_key_bytes)
#     return encrypted_e
#
# # 替换 "ssss" 为 `python_ssss`
#
# encoded_e = python_ssss(e, public_key_bytes)
# print(encoded_e)