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
            // window.location = uuu
        } else {
            console.log(uuu)
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
get_new_url('http://ggzy.zwfwb.tj.gov.cn:80/jyxxzbgg/999321.jhtml')