#  提取pdf图片
import pdfplumber
import os

lss = []
path = r"C:\Users\9000\Desktop\model-大同瑞合盈企业管理咨询有限公司.pdf"
with pdfplumber.open(path) as pdf:
    second_pag = pdf.pages[0]
    action_Name = second_pag.extract_tables()
    for i in action_Name[0]:
        # print(i[2])
        # print(i)

        lss.append(i)
    print(lss)
    dsr_name = lss[1][2]
    zdqsr = lss[2][2]
    sfz = lss[3][4]
    phone = lss[6][2]
    print(dsr_name, zdqsr, sfz, phone)
second_pag = pdf.pages[0]