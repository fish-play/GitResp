# -*- coding=utf-8 -*-
import sys

# rows = [{'进件号': '1', '受理法院市': '宁波', '法院名称': '宁波市鄞州区人民法院', '申请人单位': '宁波银行股份有限公司', '申请人信用代码': '91330200711192037M', '申请人法定人': '陆华裕', '申请人证件号': '330203196409130032', '申请人手机号': 13819823262, '申请人单位地址': '浙江省宁波市鄞州区福明街道宁东路345号', '事务所': '浙江宇豪律师事务所', '代理人1姓名': '张鹏', '代理人1联系电话': 15382301752, '代理人1执业证号': '13302202110360708', '代理人1身份证号码': '411303200005276735', '代理人1户籍地址': '浙江省宁波市鄞州区福明街道宁东路345号宁波银行股份有限公司', '代理人2姓名': '蔡璐莹', '代理人2联系电话': 15267850343, '代理人2执业证号': '13302202011189886', '代理人2身份证号码': '330624199510281123', '代理人2户籍地址': '浙江省宁波市鄞州区福明街道宁东路345号宁波银行股份有限公司', '代理人送达地址': '浙江省宁波市鄞州区宁穿路1811号', '被申请人姓名': '陈东东', '被申请人证件号': '330282199104099192', '被申请人手机号': 13476167311, '被申请人地址': '浙江省慈溪市周巷镇三江口村协同心', '被申请人民族': '汉族', '案由': '金融借款合同纠纷', '诉讼请求': '判令被告立即归还原告贷款本金人民币164798.04元，期内利息9514.29元，逾期利息37447.17元(暂算至2023年02月08日止，此后按年利率22.5%计算至款项实际清偿之日止)，以上暂合计为211759.5元；', '事实与理由': '原告与各被告分别签订《直接贷专用最高额借款合同》各一份，约定在本合同的有效期内，贷款人在最高贷款限额内，可根据借款人的申请及其借款条件和贷款人的经营状况，决定对借款人一次或分次发放贷款。具体发放的每笔贷款的种类、币种、金额、期限、用途、利率和还款方式等以相应的借款借据及其附件（若有）（包括电子银行借据，下同）记载为准，借款人对此无异议。借款借据是本合同不可分割的组成部分。原告与各被告签订合同的时间详见附表一。原、被告约定，借款人确认接受案涉电子合同，与在纸质合同上手写签字或盖章具有同等法律效力，双方无需另行签署纸质合同或文书。根据各被告的申请，原告向各被告发放贷款，具体发放的每笔贷款的具体金额、借款期限、利率、还款方式、欠款金额详见附表一。现上述各被告已经逾期欠息，未能按合同约定足额归还本息，各被告的行为已违反双方约定，构成违约。原告为维护自身合法权益，依据相关法律法规的规定向贵院提起诉讼，望判如所请。', '证据名称1': '借款合同', '证据目的1': '原告向被告借款，就原、被告双方的权利义务、最高贷款限额、被告履行债务的期限和计息方式等做了详细约定。', '证据名称2': '借款借据', '证据目的2': '被告的用款事实。', '证据名称3': '利息清单', '证据目的3': '被告的利息计算方式。', '证据名称4': '流水清单', '证据目的4': '被告的尚欠贷款本息金额。', '保全请求事项': '保全请求事项', '财产线索1': '财付通账户', '财产线索2': '支付宝账户', '保全事实与理由': '保全事实与理由'}, {'进件号': '2', '受理法院市': '宁波', '法院名称': '宁波市鄞州区人民法院', '申请人单位': '宁波银行股份有限公司', '申请人信用代码': '91330200711192037M', '申请人法定人': '陆华裕', '申请人证件号': '330203196409130032', '申请人手机号': '13819823262', '申请人单位地址': '浙江省宁波市鄞州区福明街道宁东路345号', '事务所': '浙江宇豪律师事务所', '代理人1姓名': '金典炫', '代理人1联系电话': '15382301752', '代理人1执业证号': '13302202110360708', '代理人1身份证号码': '330211199701210092', '代理人1户籍地址': '浙江省宁波市鄞州区福明街道宁东路345号宁波银行股份有限公司', '代理人2姓名': '蔡璐莹', '代理人2联系电话': '15267850343', '代理人2执业证号': '13302202011189886', '代理人2身份证号码': '330624199510281123', '代理人2户籍地址': '浙江省宁波市鄞州区福明街道宁东路345号宁波银行股份有限公司', '代理人送达地址': '浙江省宁波市鄞州区宁穿路1811号', '被申请人姓名': '陈宫星', '被申请人证件号': '331082199004274256', '被申请人手机号': 15669266207, '被申请人地址': '浙江省临海市沿江镇上百岩村69号', '被申请人民族': '汉族', '案由': '金融借款合同纠纷', '诉讼请求': '判令被告立即归还原告贷款本金人民币3402.46元，期内利息161.56元，逾期利息1221.82元(暂算至2023年02月08日止，此后按年利率18.9%计算至款项实际清偿之日止)，以上暂合计为4785.84元；', '事实与理由': '原告与各被告分别签订《直接贷专用最高额借款合同》各一份，约定在本合同的有效期内，贷款人在最高贷款限额内，可根据借款人的申请及其借款条件和贷款人的经营状况，决定对借款人一次或分次发放贷款。具体发放的每笔贷款的种类、币种、金额、期限、用途、利率和还款方式等以相应的借款借据及其附件（若有）（包括电子银行借据，下同）记载为准，借款人对此无异议。借款借据是本合同不可分割的组成部分。原告与各被告签订合同的时间详见附表一。原、被告约定，借款人确认接受案涉电子合同，与在纸质合同上手写签字或盖章具有同等法律效力，双方无需另行签署纸质合同或文书。根据各被告的申请，原告向各被告发放贷款，具体发放的每笔贷款的具体金额、借款期限、利率、还款方式、欠款金额详见附表一。现上述各被告已经逾期欠息，未能按合同约定足额归还本息，各被告的行为已违反双方约定，构成违约。原告为维护自身合法权益，依据相关法律法规的规定向贵院提起诉讼，望判如所请。', '证据名称1': '借款合同', '证据目的1': '原告向被告借款，就原、被告双方的权利义务、最高贷款限额、被告履行债务的期限和计息方式等做了详细约定。', '证据名称2': '借款借据', '证据目的2': '被告的用款事实。', '证据名称3': '利息清单', '证据目的3': '被告的利息计算方式。', '证据名称4': '流水清单', '证据目的4': '被告的尚欠贷款本息金额。', '保全请求事项': '保全请求事项', '财产线索1': '财付通账户', '财产线索2': '支付宝账户', '保全事实与理由': '保全事实与理由'}]
rows = [{"被申请人证件号": "330282199104099192"}, {"被申请人证件号": "331082199004274256"}]

# paper_data = {'营业执照': {'wwstbt': '3000-57dc474aee624e138d7343e9259bd374',
#                            'nwstbh': '100324d6b909bbee8f4523bd69bab84b9380dc32'},
#               '法定代表人身份证件': {'wwstbt': '3000-53f2f278d47f48e78ee55a3a6312dcb4',
#                                      'nwstbh': '1003242d2ffb194e5344ad8cfaf9860348671e94'},
#               '法定代表人身份证明书': {'wwstbt': '1000-914fe7d2ddc24e0ca9d3266f2a9fa16f',
#                                        'nwstbh': '1003245fb89846cecb4ddc939b2b572c3aacb424'},
#               '授权委托书1': {'wwstbt': '4000-ea18498b018443ec83150ea84558f108',
#                               'nwstbh': '10032462f5db754ab34e06aba0d6ea68f5bdf426'},
#               '公函1': {'wwstbt': '1000-0a059bd448d4455abfab64d3ec8ddc82',
#                         'nwstbh': '1003249ac844638da9421f842af134847dcc0513'},
#               '执业证1': {'wwstbt': '3000-9b6d83a13b004c8e9cac3f27f7e58262',
#                           'nwstbh': '1003241c4727704ca24cfab6639a9cabbb768b43'},
#               '授权委托书2': {'wwstbt': '2000-0465de1335d8481896df8cd28389b75f',
#                               'nwstbh': '100324e92d50284a1a474685f01eb77fd9f8fa67'},
#               '公函2': {'wwstbt': '5000-86f749e2796749f1ba92de6fd6361a8b',
#                         'nwstbh': '100324c70ee7095d74420da85d9b14750a800215'},
#               '执业证2': {'wwstbt': '3000-27cd4abb3862420685c732df267af31d',
#                           'nwstbh': '100324da15a6d2b0e24f7d8250fc3416425cc156'},
#               '被告330282199104099192身份证明': {'wwstbt': '4000-0ae4c5512a7647e2b09f33fe81e22895',
#                                                  'nwstbh': '100324c4a308a91af94ec08c004021efe8fd4c76'},
#               '被告330282199104099192证据1': {'wwstbt': '4000-e3cf8e7e5b0f4f3fb3adbd03926abd1b',
#                                               'nwstbh': '100324242a62cff1ec43acaae756b3531ee3f344'},
#               '被告330282199104099192证据2': {'wwstbt': '3000-60d3cd2057c24f0283f636b197253589',
#                                               'nwstbh': '100324e16f153af43e4e4d847fe5676b230cf744'},
#               '被告330282199104099192证据3': {'wwstbt': '3000-467908108ffd4cdcb7c24ddecde0255d',
#                                               'nwstbh': '100324acffc62068a649cca5683977f88b8e3644'},
#               '被告330282199104099192证据4': {'wwstbt': '2000-2f027507b74a4ce3904e260d93613015',
#                                               'nwstbh': '100324da794726acc845378a60df6bbc73d5bf20'},
#               '被告331082199004274256身份证明': {'wwstbt': '4000-870dc0809456494599511a05f06d77c7',
#                                                  'nwstbh': '10032407b99d41414742ca83535adf63aecc7167'},
#               '被告331082199004274256证据1': {'wwstbt': '4000-844f861e1ff542ff8048d6075fe84ba0',
#                                               'nwstbh': '10032408bc32580b4a4fd6949b2aa0ae25838d58'},
#               '被告331082199004274256证据2': {'wwstbt': '1000-1bf85b00672540dca0e6764a57d04484',
#                                               'nwstbh': '1003240d97ed1394834ecf8ebe0831ff9d791075'},
#               '被告331082199004274256证据3': {'wwstbt': '2000-b5b0074c6e7f4a35a2d1ff4ac26aeba5',
#                                               'nwstbh': '100324249b503d1cbb4e688cc2a80084f19a6a47'},
#               '被告331082199004274256证据4': {'wwstbt': '4000-797751e0b9bf42c6b0897c7f8665c7e2',
#                                               'nwstbh': '100324c408f734b4ae463c88b5f73da7a515a417'}}
#
# bg_id_data = {'被申请人330282199104099192id': '1840899', '被申请人331082199004274256id': '1840900'}

# paper_data.update(bg_id_data)
# print(paper_data.keys())
all_data = {'330282199104099192': {'被告330282199104099192证据1': {'nwstbh': '100324242a62cff1ec43acaae756b3531ee3f344',
                                                                   'wwstbt': '4000-e3cf8e7e5b0f4f3fb3adbd03926abd1b'},
                                   '被告330282199104099192证据2': {'nwstbh': '100324e16f153af43e4e4d847fe5676b230cf744',
                                                                   'wwstbt': '3000-60d3cd2057c24f0283f636b197253589'},
                                   '被告330282199104099192证据3': {'nwstbh': '100324acffc62068a649cca5683977f88b8e3644',
                                                                   'wwstbt': '3000-467908108ffd4cdcb7c24ddecde0255d'},
                                   '被告330282199104099192证据4': {'nwstbh': '100324da794726acc845378a60df6bbc73d5bf20',
                                                                   'wwstbt': '2000-2f027507b74a4ce3904e260d93613015'},
                                   '被告330282199104099192身份证明': {
                                       'nwstbh': '100324c4a308a91af94ec08c004021efe8fd4c76',
                                       'wwstbt': '4000-0ae4c5512a7647e2b09f33fe81e22895'},
                                   '被申请人330282199104099192id': '1840899'},
            '331082199004274256': {'被告331082199004274256证据1': {'nwstbh': '10032408bc32580b4a4fd6949b2aa0ae25838d58',
                                                                   'wwstbt': '4000-844f861e1ff542ff8048d6075fe84ba0'},
                                   '被告331082199004274256证据2': {'nwstbh': '1003240d97ed1394834ecf8ebe0831ff9d791075',
                                                                   'wwstbt': '1000-1bf85b00672540dca0e6764a57d04484'},
                                   '被告331082199004274256证据3': {'nwstbh': '100324249b503d1cbb4e688cc2a80084f19a6a47',
                                                                   'wwstbt': '2000-b5b0074c6e7f4a35a2d1ff4ac26aeba5'},
                                   '被告331082199004274256证据4': {'nwstbh': '100324c408f734b4ae463c88b5f73da7a515a417',
                                                                   'wwstbt': '4000-797751e0b9bf42c6b0897c7f8665c7e2'},
                                   '被告331082199004274256身份证明': {
                                       'nwstbh': '10032407b99d41414742ca83535adf63aecc7167',
                                       'wwstbt': '4000-870dc0809456494599511a05f06d77c7'},
                                   '被申请人331082199004274256id': '1840900'}}


zlis = []
for i in rows:
    z = {}
    z["url"] = all_data[i['被申请人证件号']][f"被告{i['被申请人证件号']}身份证明"]["nwstbh"]
    z["nw_oss_url"] = all_data[i['被申请人证件号']][f"被告{i['被申请人证件号']}身份证明"]["wwstbt"]
    z["file_name"] = "被告身份证明.pdf"
    z["clfl"] = "10"
    z["clfl_mc"] = "当事人身份材料",
    z["clsm"] = "被告身份证明"
    z["is_merge"] = "0"
    z["is_original"] = "1"
    z["clsx"] = "2"
    z["tjr_name"] = "张鹏"
    z["tjr_lx"] = "1"
    z["sort"] = "1"
    z["zrrid"] = all_data[i['被申请人证件号']][f"被申请人{i['被申请人证件号']}id"]
    zlis.append(z)
print(zlis)

# for cid in rows:
#     one_data = {}
#     for cid_data in paper_data:
#         if cid["被申请人证件号"] in cid_data:
#             one_data[cid_data] = paper_data[cid_data]
#             all_data[cid["被申请人证件号"]] = one_data
#
# from pprint import pprint
# pprint(all_data)
