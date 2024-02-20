# a = """
# <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
# <html xmlns="http://www.w3.org/1999/xhtml">
# <head>
#     <title>网上立案材料上传</title>
#     <meta name="renderer" content="webkit">
#     <meta http-equiv="X-UA-Compatible" content="IE=edge">
#     <script type="text/javascript" src="/lsfwpt/js/jquery-1.11.2.min.js"></script>
#     <script type="text/javascript" src="/lsfwpt/js/xJsonNew.js"></script>
#     <script type="text/javascript" src="/lsfwpt/js/jquery.alerts.js"></script>
#
#     <script src="/lsfwpt/js/jquery.ui.widget.js"></script>
#     <script src="/lsfwpt/js/jquery.iframe-transport.js"></script>
#     <script src="/lsfwpt/js/jquery.fileupload.js"></script>
#
#     <script type="text/javascript" src="/lsfwpt/js/wslawzh/wslawzh_clsc.js" charset="UTF-8"></script>
#     <link rel="stylesheet" type="text/css" href="/lsfwpt/css/jalerts/jquery.alerts2.css"/>
#     <link rel="stylesheet" href="/lsfwpt/css/theme.css" type="text/css" media="all"/>
#     <link rel="stylesheet" href="/lsfwpt/css/wslawzh/css/wslawzh.css"/>
#     <link rel="stylesheet" href="/lsfwpt/css/css_new/css/font-awesome.css"/>
#     <script type="text/javascript" src="/lsfwpt/js/common.js"></script>
#     <script type="text/javascript" src="/lsfwpt/layer/layer.js"></script>
#     <script type="text/javascript" src="/lsfwpt/css/xcConfirm/js/xcConfirm.js"></script>
#     <link rel="stylesheet" href="/lsfwpt/css/xcConfirm/css/xcConfirm.css" />
#     <link rel="stylesheet" href="/lsfwpt/css/smallpop/dist/spop.min.css" />
#     <script src="/lsfwpt/css/smallpop/dist/spop.js"></script>
#     <script type="text/javascript" src="/lsfwpt/js/jsencrypt.js"></script>
#     <script type="text/javascript" src="/lsfwpt/js/rsa.js"></script>
#     <script type="text/javascript" src="/lsfwpt/js/base64.js"></script>
#     <style type="text/css">
#         ::-webkit-scrollbar {display: none}
#         div.clxz{float:left;width:auto;margin-left:5px;height:100%;}
#         div.clxz div.bd {position:relative;top:0.8rem;width:5rem;height:5.5rem;float:left;text-align: center;margin-right:3rem;}
#         div.clxz div.bd ul{margin:0px;}
#         div.clxz div.bd ul li{float:left;}
#         div.clxz div.bd ul li a{width:100%;height:auto;position:relative;}
#         div.clxz div.bd ul li a img{width:5.5rem;height:5rem;}
#         div.clxz div.bd ul li a span{word-break: break-all;float:left;width:105%;text-align:center;height:auto;line-height:1rem;position:relative;bottom:0.375rem;left:0rem;color:#575757;font-size: 0.5rem;}
#         div.clxz .bd a.prev{position:absolute;z-index:1;background:url(../../../../img/mjjd_qscl/sanjiaoxing.png) no-repeat;width:0.6rem;height:0.6rem;bottom:45px;left:-0.3rem;background-size:cover;transform:rotate(180deg);}
#         div.clxz .bd a.next{position:absolute;z-index:1;background:url(../../../../img/mjjd_qscl/sanjiaoxing.png) no-repeat;width:0.6rem;height:0.6rem;bottom:45px;right:0.4rem;background-size:cover;}
#         div.clxz div.tianjia{width:4.25rem;height:4.25rem;margin:0.5rem;overflow:hidden;float:left;position:relative;top:0.5rem;left:1rem}
#         div.clxz div.tianjia a{float:left;width:100%;height:100%;}
#         div.clxz div.tianjia a img{float:left;width:100%;height:100%;}
#         .delte_img {position: absolute;float: right;margin-left: 4.9rem;cursor:pointer;width: 2rem;}
#         .progress .bar {position: absolute;top: 2rem;left: 0.3rem;width: 0%;height: 7%;color: #ffffff;float: left;font-size: 0.75rem;text-align: center;align-items: center;display: flex;justify-content: center;text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.25);background-color: #60BB33;background-image: -moz-linear-gradient(top, #149bdf, #0480be);background-image: -webkit-gradient(linear, 0 0, 0 100%, from(#149bdf), to(#0480be));background-image: -webkit-linear-gradient(top, #149bdf, #0480be);background-image: -o-linear-gradient(top, #149bdf, #0480be);background-image: linear-gradient(to bottom, #149bdf, #0480be);background-repeat: repeat-x;filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ff149bdf', endColorstr='#ff0480be', GradientType=0);-webkit-box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.15);-moz-box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.15);box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.15);-webkit-box-sizing: border-box;-moz-box-sizing: border-box;box-sizing: border-box;-webkit-transition: width 0.6s ease;-moz-transition: width 0.6s ease;-o-transition: width 0.6s ease;transition: width 0.6s ease;}
#         .sc_fileName{display: block; height: 20px; line-height: 20px; position: absolute; top: 45px; font-size: 12px; width: 100%; overflow: hidden;text-overflow:ellipsis;}
#         .bd:hover .sc_fileName{display: none;}
#         .yc_fileName{display: none; height: auto; line-height: 20px; position: absolute; top: 48px; font-size: 12px; width: auto;left: 6px;z-index: 999;}
#         .bd:hover .yc_fileName{display: inline-block;background-color:#fff;border: 1px solid #666666;}
#         .ssnr {  width: calc(100%); margin-top:20px;min-height: 0px;}
#         .ssnr .ssqq{margin-top: 20px;}
#     </style>
#     <script type="text/javascript">
#         var path = "/lsfwpt";
#         var lasqid = "1224999";
#         var ajlx = "2001";
#         var fybm = "1326";
#         var fymc = "宁波市鄞州区人民法院";
#         var is_sqtj = "1";
#         var lafs = "ocr";
#         var ay = "9178";
#         var ry_lx = "1";
#         var name = "张鹏";
#         var sffhzs = "0";
#         var ssbqid = "";
#         //立案方式
#         var sfjrjk = "0";
#         var sfmjjd = "0";;
#         var sfyhkjy = "0";
#         var rsatoken = "ivQweHCZp3JOWEGJ+k+k3pdx5dMhV3ePpLmVtY/jTR0lJSYgqaFGMzeLq1olY4Qam4s2r7mBgd11OH3LxfZDqXDeY2EqZsOu0vFd60gHd5z9WcjH/SnlsGG5jPbR5jHod6HhRP9vBqzJyRFKPxFDBrqZnTEWPQzBozVc0qm9rek=";
#     </script>
# </head>
# <body>
# <div class="xlssy_nav">
#     <img class="loge" src="/lsfwpt/zjfyw/images/logo.png" alt=""/>
#     <img class="name" src="/lsfwpt/zjfyw/images/name.png" alt=""/>
#     <p>欢迎您使用浙江法院网!</p>
# </div>
# <div class="xlssy_img" id="xlssy_img">
#     <div class="xlssy_z">
#         <div>网上立案</div>
#     </div>
# </div>
# <div class="zxwzh_header">
#     <img src="/lsfwpt/css/zxwzh/images/xian.png" alt="" class="xxian">
#     <ul>
#         <li class="zbds"><span><i class="fa fa-check-square"></i></span><p>立案告知</p></li>
#         <li class="zbds"><span><i class="fa fa-user-o"></i></span><p>信息登记</p></li>
#         <li class="zbds"><span><i class="fa fa-users"></i></span><p>诉讼内容</p></li>
#         <li class="zbds"><span><i class="fa fa-file-image-o"></i></span><p>材料上传</p></li>
#         <li class=""><span><i class="fa fa-files-o"></i></span><p>起诉预览</p></li>
#         <li class=""><span><i class="fa fa-arrows-alt"></i></span><p>完成</p></li>
#     </ul>
# </div>
# <div class="clsc_content">
#
#     <div class="ffcl" id="ffcl">
#         <span class="ffcl_sapn" id="ffcl_sapn">身份材料
#             <span class="zd_span" style="float:right;font-weight:500;margin-right:70px;" onclick="$('#ffcl_sc').toggle(500)">折叠</span>
#             <span style="color:red;float:right;font-size:16px;margin-right:40px;font-weight:500;"><span tyle="color:#12A1E3;">【上传说明：建议上传jpg/pdf格式材料，最大可上传300M </span>( 上传成功后点击文件名可直接预览 )（<span style="color:red;">*</span>号为必输项）】</span>
#         </span>
#         <div class="ffcl_sc" id="ffcl_sc">
#
#             <div class="ygxx" id="ygxx">
#                 <div class="ssdw">
#                     <span class="ssdw_span">原告</span>
#
#                 </div>
#                 <div class="ygffcl_sc" id="ygffcl_sc"></div>
#             </div>
#
#             <div class="ygdlxx" id="ygdlxx">
#                 <div class="ssdw">
#                     <span class="ssdw_span">原告代理人</span>
#
#                 </div>
#                 <div class="ygdlffcl_sc" id="ygdlffcl_sc">
#                 </div>
#             </div>
#
#             <div class="bgxx" id="bgxx">
#                 <div class="ssdw">
#                     <span class="ssdw_span">被告</span>
#
#                 </div>
#                 <div class="bgffcl_sc" id="bgffcl_sc">
#                 </div>
#             </div>
#
#             <div class="dsrxx" id="dsrxx">
#                 <div class="ssdw">
#                     <span class="ssdw_span">第三人</span>
#
#                 </div>
#                 <div class="dsrffcl_sc" id="dsrffcl_sc">
#                 </div>
#             </div>
#         </div>
#     </div>
#
#     <div class="zjcl" id="zjcl">
#         <span class="zjcl_sapn" id="zjcl_sapn">证据材料
#             <span class="zd_span" style="float:right;font-weight:500;margin-right:70px;" onclick="$('#zjcl_sc').toggle(500)">折叠</span>
#             <span class="zd_span" style="float:right;font-weight:500;margin-right:20px;cursor: pointer;" onclick="addZjcl()">添加</span>
#         </span>
#         <div class="zjcl_sc" id="zjcl_sc">
#             <div class="zjcl_content" id="zjcl_content">
#             </div>
#         </div>
#     </div>
#
#     <div class="ssbq" id="ssbq">
#         <span class="ssbq_sapn" id="ssbq_sapn">诉讼保全</span>
#         <div class="ssbq_content" id="ssbq_content">
#             <div style="height:50px;width:402px;">
#                 <span style="display:inline-block;height:50px;line-height:50px;width:150px;text-align:center;background-color:#f2f7fc;font-size:16px;border-radius:5px 0 0 5px;">是否申请诉讼保全</span>
#                 <div style="height:46px;line-height:50px;width:250px;border: 2px solid #f2f7fc;border-radius:0 5px 5px 0;border-left:0;float:right;">
#                     <div style="height:50px;margin-left:30px;float:left;font-size:16px;"><input type="radio" onchange="ssbqSelect()" name="sfsqssbq" id="sfsqssbq_1" value="1" style="width:15px;height:15px;cursor:pointer;"/>是</div>
#                     <div style="height:50px;margin-left:60px;float:left;font-size:16px;"><input type="radio" onchange="ssbqSelect()" checked name="sfsqssbq" id="sfsqssbq_2" value="2" style="width:15px;height:15px;cursor:pointer;"/>否</div>
#                 </div>
#             </div>
#             <div class="ssbq_bqsqxx" id="ssbq_bqsqxx" style="display: none;">
#                 <div class="xxtx_top">
#                     <span class="xxtx_top_span">保全申请信息</span>
#                 </div>
#                 <table width="100%" style="margin-top:10px;font-size:16px;">
#                     <tr>
#                         <td style="width: 25%;background-color: #f2f7fc;">
#                             <span><font color="red">*</font>申请人选择</span>
#                         </td>
#                         <td colspan="3" style="width: 75%;text-align:left;">
#                             <div class="bqsqxx_radio" id="sqrxx_radio">
#                             </div>
#                         </td>
#                     </tr>
#                     <tr>
#                         <td style="width: 25%;background-color: #f2f7fc;">
#                             <font color="red">*</font>被申请人选择</span>
#                         </td>
#                         <td colspan="3" style="width: 75%;text-align:left;">
#                             <div class="bqsqxx_radio" id="bsqrxx_radio">
#                             </div>
#                         </td>
#                     </tr>
#                 </table>
#                 <div class="ssnr">
#                     <div class="ssqq" id="ssqq">
#                         <span class="ssqq_sapn" id="ssqq_sapn"><span style="color:red">*</span>请求事项
#                             <span class="tj_span" style="float:right;font-size:18px;width:auto;display:inline-block;height:50px;line-height:50px;font-weight:500;position:relative;left:-90px;cursor:pointer;" onclick="addSsqq()">添加</span>
#                         </span>
#                         <table>
#                             <thead>
#                             <tr>
#                                 <th width="15%">序号</th>
#                                 <th width="60%">事项内容</th>
#                                 <th width="25%">操作</th>
#                             </tr>
#                             </thead>
#                             <tbody id="ssqq_tbody">
#                             </tbody>
#                         </table>
#                     </div>
#
#                     <div class="ssqq" id="ccxs">
#                         <span class="ssqq_sapn" id="ccxs_sapn">财产线索
#                             <span class="tj_span" style="float:right;font-size:18px;width:auto;display:inline-block;height:50px;line-height:50px;font-weight:500;position:relative;left:-90px;cursor:pointer;" onclick="addCcxs()">添加</span>
#                         </span>
#                         <table>
#                             <thead>
#                             <tr>
#                                 <th width="15%">序号</th>
#                                 <th width="60%">线索内容</th>
#                                 <th width="25%">操作</th>
#                             </tr>
#                             </thead>
#                             <tbody id="ccxs_tbody">
#                             </tbody>
#                         </table>
#                     </div>
#                     <div class="ssyly" id="ssyly">
#                         <span class="ssyly_sapn" id="ssyly_sapn"><span style="color:red">*</span>事实与理由</span>
#                         <textarea id="lynr" placeholder="请填写事实与理由"></textarea>
#                     </div>
#                 </div>
#             </div>
#             <div class="ssbq_bqclsc" id="ssbq_bqclsc" style="display: none;">
#                 <div class="xxtx_top">
#                     <span class="xxtx_top_span">保全材料上传</span>
#                 </div>
#                 <table width="100%" style="margin-top:10px;font-size:16px;">
#                     <tr>
#                         <td style="width: 25%;background-color: #f2f7fc;">
#                             <span>担保函</span>
#                         </td>
#                         <td style="width: 75%;">
#                             <div class="clxz slideBox">
#                                 <input type="hidden" name="clfl" value="5">
#                                 <input type="hidden" name="clfl_mc" value="保全类">
#                                 <input type="hidden" name="clsm" value="担保函">
#                                 <input class="fileupload" id="dbh_1_fileupload" type="file" data-url="/lsfwpt/servlet/AttachUploadZwyOss?appsec=ivQweHCZp3JOWEGJ+k+k3pdx5dMhV3ePpLmVtY/jTR0lJSYgqaFGMzeLq1olY4Qam4s2r7mBgd11OH3LxfZDqXDeY2EqZsOu0vFd60gHd5z9WcjH/SnlsGG5jPbR5jHod6HhRP9vBqzJyRFKPxFDBrqZnTEWPQzBozVc0qm9rek=" style="display: none;" multiple="">
#                                 <div class="tianjia" id="dbh_1_fileupload_add">
#                                     <a href="javascript:;">
#                                         <img onclick="add_qscl_mjjd('dbh_1_fileupload')" src="/lsfwpt/img/mjjd_qscl/tianjia.png" alt="上传材料">
#                                     </a>
#                                 </div>
#                             </div>
#                         </td>
#                     </tr>
#                 </table>
#             </div>
#         </div>
#     </div>
# </div>
# <div class="bottom_btn_group" >
#     <div  onclick="lastpage()" >上一步</div>
#     <div  onclick="do_save()" >暂存</div>
#     <div  onclick="do_next()" >下一步</div>
# </div>
# <div id="mjjd_qscl_show" style="display: none;">
#     <img src="" id="qscl_show_window"  width="100%" >
#     <iframe src="" width="880px" height="880px" style="display: none;" frameborder="0" scrolling="yes" name="mjjd_mainiframe" id="mjjd_mainiframe">
#     </iframe>
# </div>
# </body>
# </html>
# """
# import re
# s = re.findall("rsatoken = (.*)</script>", a, re.S)[0].replace(";", "").replace("\n", "")
# print(s)
s = {'330282199104099192': {
        '被告330282199104099192身份证明': {'wwstbt': '2000-04bc087a7ebe45629947bfdefd4bdc5f',
                                           'nwstbh': '100324eba7531c5dd74090a378c5c9eb6e529629'},
        '被告330282199104099192证据1': {'wwstbt': '5000-f3f4a233ad774dbfbc560b9efcaa9b5d',
                                        'nwstbh': '1003248078d675667a442ab40d27ea1493e45e46'},
        '被告330282199104099192证据2': {'wwstbt': '5000-c7e313c83dad4559bb44022f6a7cda8e',
                                        'nwstbh': '100324ed9fe1363322454dbc17694b89be408d00'},
        '被告330282199104099192证据3': {'wwstbt': '2000-4afea042e02542d5ba03b194edbf94ab',
                                        'nwstbh': '1003241117fd10bd4542fdbfdb293ed9d7027a59'},
        '被告330282199104099192证据4': {'wwstbt': '4000-86803ae4e3324737b63f76fe127471ec',
                                        'nwstbh': '100324ffbe6267b1c64ca7bbc6938b6fca435202'},
        '被申请人330282199104099192id': '1840809',
        '被告331082199004274256身份证明': {'wwstbt': '1000-d62b7729920f4d10b6fc32b547ec4f17',
                                           'nwstbh': '100324eea3ed13436a44b6ae7fad0fb4316b1402'},
        '被告331082199004274256证据1': {'wwstbt': '1000-1df88c787a964e35a5e070b0c6d2f433',
                                        'nwstbh': '100324a384b515bca24364bc6d2ef01a764bcb52'},
        '被告331082199004274256证据2': {'wwstbt': '5000-347034da42d74188862be6b8c6d3821d',
                                        'nwstbh': '100324b24292374fbd4b65a81392502aa4875c92'},
        '被告331082199004274256证据3': {'wwstbt': '4000-8688b46ee6004665841d55c8e3e48b11',
                                        'nwstbh': '1003245ae66f68a40549db97b7a2db34c808f981'},
        '被告331082199004274256证据4': {'wwstbt': '3000-063bc37cd9af4d36a219efb4e082702d',
                                        'nwstbh': '100324c1003152f91749abac4109e5c9ffeb3314'},
        '被申请人331082199004274256id': '1840810'},
    '331082199004274256': {
        '被告330282199104099192身份证明': {'wwstbt': '2000-04bc087a7ebe45629947bfdefd4bdc5f',
                                           'nwstbh': '100324eba7531c5dd74090a378c5c9eb6e529629'},
        '被告330282199104099192证据1': {'wwstbt': '5000-f3f4a233ad774dbfbc560b9efcaa9b5d',
                                        'nwstbh': '1003248078d675667a442ab40d27ea1493e45e46'},
        '被告330282199104099192证据2': {'wwstbt': '5000-c7e313c83dad4559bb44022f6a7cda8e',
                                        'nwstbh': '100324ed9fe1363322454dbc17694b89be408d00'},
        '被告330282199104099192证据3': {'wwstbt': '2000-4afea042e02542d5ba03b194edbf94ab',
                                        'nwstbh': '1003241117fd10bd4542fdbfdb293ed9d7027a59'},
        '被告330282199104099192证据4': {'wwstbt': '4000-86803ae4e3324737b63f76fe127471ec',
                                        'nwstbh': '100324ffbe6267b1c64ca7bbc6938b6fca435202'},
        '被申请人330282199104099192id': '1840809',
        '被告331082199004274256身份证明': {'wwstbt': '1000-d62b7729920f4d10b6fc32b547ec4f17',
                                           'nwstbh': '100324eea3ed13436a44b6ae7fad0fb4316b1402'},
        '被告331082199004274256证据1': {'wwstbt': '1000-1df88c787a964e35a5e070b0c6d2f433',
                                        'nwstbh': '100324a384b515bca24364bc6d2ef01a764bcb52'},
        '被告331082199004274256证据2': {'wwstbt': '5000-347034da42d74188862be6b8c6d3821d',
                                        'nwstbh': '100324b24292374fbd4b65a81392502aa4875c92'},
        '被告331082199004274256证据3': {'wwstbt': '4000-8688b46ee6004665841d55c8e3e48b11',
                                        'nwstbh': '1003245ae66f68a40549db97b7a2db34c808f981'},
        '被告331082199004274256证据4': {'wwstbt': '3000-063bc37cd9af4d36a219efb4e082702d',
                                        'nwstbh': '100324c1003152f91749abac4109e5c9ffeb3314'},
        '被申请人331082199004274256id': '1840810'}}
