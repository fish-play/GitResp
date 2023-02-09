"""
-*- coding: utf-8 -*-
@Time : 2022/11/15 9:11
"""
import os.path
import re
import sys
import execjs
import base64
from Crypto.Cipher import AES
import requests
from lxml import etree

url = r'http://ggzy.zwfwb.tj.gov.cn/jyxx/index.jhtml'
header = {
    'Cookie': 'clientlanguage=zh_CN; JSESSIONID=27C58AD82D340C2FB020623E179D7972',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Referer': 'http://ggzy.zwfwb.tj.gov.cn/jyxxgcjs/index.jhtml'
}
response = requests.get(url, headers=header)
htm = response.content.decode()
p_list = etree.HTML(htm)
print(p_list)
ff = p_list.xpath("//ul[@class='article-list2']/li//a/@url")
# js方法
ctx = execjs.compile("""
const CryptoJS = require("crypto-js");
function get_new_url(url) {
    var s = "qnbyzzwmdgghmcnm";
    var hh = url;
    if (typeof (hh) == 'undefined' || hh == '#') {
        hh = $(this).attr("url");
        if (typeof (hh) == 'undefined' || hh == '#') {
            return
        }
    }
    var aa = hh.split("/");
    var aaa = aa.length;
    var bbb = aa[aaa - 1].split('.');
    var ccc = bbb[0];
    var cccc = bbb[1];
    var r = /^\+?[1-9][0-9]*$/;
    var ee = '_blank';
    if (r.test(ccc) && cccc.indexOf('jhtml') != -1) {
        var srcs = CryptoJS.enc.Utf8.parse(ccc);
        var k = CryptoJS.enc.Utf8.parse(s);
        var en = CryptoJS.AES.encrypt(srcs, k, {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        });
        var ddd = en.toString();
        ddd = ddd.replace(/\//g, "^");
        ddd = ddd.substring(0, ddd.length - 2);
        var bbbb = ddd + '.' + bbb[1];
        aa[aaa - 1] = bbbb;
        var uuu = '';
        for (i = 0; i < aaa; i++) {
            uuu += aa[i] + '/'
        }
        uuu = uuu.substring(0, uuu.length - 1);
        if (typeof (ee) == 'undefined') {
            console.log(uuu)
            return uuu
            // window.location = uuu
        } else {
            console.log(uuu)
            return uuu
            // window.open(uuu)
        }
    } else {
        if (typeof (ee) == 'undefined') {
            window.location = hh
        } else {
            window.open(hh)
        }
    }
    return false
}
""")
for i in ff:
    print(i)
    # 调用js方法
    e = ctx.call("get_new_url", f"{i}")
    print(fr"{e}")







