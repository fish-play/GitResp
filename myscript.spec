# -*- coding:utf-8 -*-
import re
import os
from flows.flow import ListDataFlow, FileItem, ScriptDef, SelectItem, UserSelectItem, DirectoryItem, StringItem
from rpalib.log import logger
import openpyxl
import pandas as pd
from openpyxl import Workbook
import datetime, dateutil
from dateutil.relativedelta import relativedelta
from openpyxl.styles import *
import time



class NB_LiXi(ListDataFlow):

    def __init__(self, summary_statement, excel_path, save_path, select_data):

        self.summary_statement = summary_statement
        self.excel_path = excel_path
        self.save_path = save_path
        self.select_data = select_data
        self.types = ""
        self.file_name = None
        self.g = None
        self.dkr_name = None
        self.dkr_id = None
        self.dkr_dkzh = None
        self.all_file = None
        self.listes = []
        self.appen = []
        self.dkr_zhlist = []
        self.error = []

    def read_summary_statement(self):
        logger.info("开始读取表格！")
        df = pd.read_excel(self.summary_statement)
        self.g = df.groupby(['借款人姓名', '身份证号'])

    def read_ben_xi(self, excel, rowq, e, yqlv, zbsybj, zbsyqnlx):

        # 读取第二张表
        wb = openpyxl.load_workbook(self.excel_path)
        sheets = wb.sheetnames[0]
        ws = wb[sheets]
        rows = ws.rows
        lists = []
        alls = []
        sss = [['贷款账号'], ['期数'], ['应还本息'], ['本金'], ['利息'], ['实还本金'], ['实还利息']]
        for age in sss:
            alls.append(age)
        for row in rows:
            line = [col.value for col in row]
            lists.append(line)
        yhbj_sum = 0
        bj_sum = 0
        lx_sum = 0
        shbj_sum = 0
        shlx_sum = 0
        jz_data = None
        ys_year = None
        for i in lists[1:][0:]:
            if str(i[0:1][0]) == str(e):
                alls.append(i[0:1])
                year = str(i[1:2][0])
                ys_year = year
                year = re.search("(.*?) ", year).group(1).replace("-", "/")
                alls.append([year])
                jz_data = year
                alls.append(i[2:3])
                yhbj_sum = yhbj_sum + float(i[2:3][0])
                alls.append(i[3:4])
                bj_sum = bj_sum + float(i[3:4][0])
                alls.append(i[4:5])
                lx_sum = lx_sum + float(i[4:5][0])
                alls.append(i[5:6])
                shbj_sum = shbj_sum + float(i[5:6][0])
                alls.append(i[6:7])
                shlx_sum = shlx_sum + float(i[6:7][0])
            else:
                continue
        # print(alls)
        # 应还本金合计
        try:
            yhbj_sum = '%.2f' % yhbj_sum
            # 本金合计
            bj_sum = '%.2f' % bj_sum
            # 利息合计
            lx_sum = '%.2f' % lx_sum
            # 实还本金合计
            shbj_sum = '%.2f' % shbj_sum
            # 实还利息合计
            shlx_sum = '%.2f' % shlx_sum
            hj = [[''], ["合计"], [yhbj_sum], [bj_sum], [lx_sum], [shbj_sum], [shlx_sum]]
            for age in hj:
                alls.append(age)
            # jz_data  截止日期
            # 截止本金
            jz_bjs = float(bj_sum) - float(shbj_sum)
            jz_bj = '%.2f' % jz_bjs
            # 截止利息
            jz_lxs = float(lx_sum) - float(shlx_sum)
            jz_lx = '%.2f' % jz_lxs
            # print("截止利息", jz_lx)
            jz = [[""], [f"截止{jz_data}"], [""], [jz_bj], [jz_lx], [""], [""]]
            for abort in jz:
                alls.append(abort)
            # 最后一行
            # print(ys_year)
            datetime7 = datetime.datetime.strptime(ys_year, "%Y-%m-%d %H:%M:%S")
            zh_data = datetime7 + dateutil.relativedelta.relativedelta(days=1)  # 减1天
            zh_datas = re.search("(.*?) ", str(zh_data)).group(1).replace("-", "/")
            select_data = str(self.select_data) + " " + "00:00:00"
            srsj = datetime.datetime.strptime(f"{select_data}", "%Y-%m-%d %H:%M:%S")
            # print(srsj)
            # print(datetime7)
            qkts = srsj - datetime7
            qktss = re.search("(.*?) ", str(qkts)).group(1)
            data = str(self.select_data).replace("-", "/")
            # print(int(qktss))
            zh_lv = float(jz_bj) * float(yqlv) * 0.01 / 360 * int(qktss)
            zh_lvs = '%.2f' % zh_lv
            zhs = [[""], [f"{zh_datas}-{data}"], [""], [jz_bj], [zh_lvs], [""], [""]]
            for abort_data in zhs:
                alls.append(abort_data)
            new_x = [l[0] for l in alls]
            all_list = []
            for one_list in [new_x[i:i + 7] for i in range(0, len(new_x), 7)]:
                all_list.append(one_list)
                # print(one_list)
            self.all_file = all_list
        except:
            logger.error("数据未找到")

        wq = excel.active
        x = ["A", "B", "C", "D", "E", "F", "G"]
        # print(rowq)
        e = int(rowq) + 2
        border = Border(left=Side(border_style=None,
                                  color='FF000000',
                                  style='thin'),
                        right=Side(border_style=None,
                                   color='FF000000',
                                   style='thin'),
                        top=Side(border_style=None,
                                 color='FF000000',
                                 style='thin'),
                        bottom=Side(border_style=None,
                                    color='FF000000',
                                    style='thin'))
        font_ = Font(size=10)
        for q in self.all_file:
            # print("这是q",q)
            e += 1
            for r in range(7):
                wq[f"{x[r]}{e}"] = q[r]
                wq[f"{x[r]}{e}"].border = border
                wq[f"{x[r]}{e}"].font = font_
                # print(wq[f"{x[r]}{e}"])
        # print('这是加入小计前的行书',e)
        print(zbsybj)
        print(zbsyqnlx)
        line = e + 2
        wq[f"D{line}"].value = "小计"
        wq[f"E{line}"].value = "本金"
        wq[f"F{line}"].value = f"{jz_bj}"
        if float(jz_bj)+1 < float(zbsybj) or float(jz_bj)-1 > float(zbsybj):
            wq[f"G{line}"].value = "不一致"
            self.error.append(f"{self.dkr_name}-{self.dkr_id}-{self.dkr_dkzh}本金不一致")
        wq[f"E{int(line) + 1}"].value = "期内利息"
        wq[f"F{int(line) + 1}"].value = f"{jz_lx}"
        if float(jz_lx)+1 < float(zbsyqnlx) or float(jz_lx)-1 > float(zbsyqnlx):
            wq[f"G{int(line) + 1}"].value = "不一致"
            self.error.append(f"{self.dkr_name}-{self.dkr_id}-{self.dkr_dkzh}期内利息不一致")
        wq[f"E{int(line) + 2}"].value = "罚息"
        wq[f"F{int(line) + 2}"].value = f"{zh_lvs}"
        wq[f"E{int(line) + 3}"].value = "总计"
        zong_ji = float(jz_bj) + float(jz_lx) + float(zh_lvs)
        zong_ji = '%.2f' % zong_ji
        wq[f"F{int(line) + 3}"].value = f"{zong_ji}"
        a = wq.max_row
        return a, bj_sum, jz_bj, jz_lx, zh_lvs

    def selet(self):
        for name, group in self.g:
            # print(f"group: {name}")

            df1 = pd.DataFrame(group)
            out_excel = Workbook()
            current_row = 0
            zdkbj = 0
            # 本金
            bj = 0
            qnlx = 0
            yqfx = 0
            dkbhs = []
            for i in df1.index:
                if df1["还本付息方式"][i] == "等额本息":
                    logger.info(str(self.dkr_name)+"-"+str(self.dkr_id)+"-"+str(self.dkr_dkzh))
                    self.dkr_name = df1["借款人姓名"][i]
                    self.dkr_id = df1["身份证号"][i]
                    self.dkr_dkzh = df1["贷款账号"][i]
                    dkbhs.append(str(self.dkr_dkzh))
                    # logger.info("开始执行", self.dkr_name)
                    self.dkr_zhlist.append(str(self.dkr_dkzh))

                    hkfs = df1["还本付息方式"][i]
                    yqlv = df1["逾期执行利率"][i]
                    ws = out_excel.active  # 选取当前sheet工作表
                    ws.merge_cells("A1:G2")
                    # 也可以用 ws.merge_cells("A2:D2")
                    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")  # 添加样式
                    border = Border(left=Side(border_style=None,
                                              color='FF000000',
                                              style='thin'),
                                    right=Side(border_style=None,
                                               color='FF000000',
                                               style='thin'),
                                    top=Side(border_style=None,
                                             color='FF000000',
                                             style='thin'),
                                    bottom=Side(border_style=None,
                                                color='FF000000',
                                                style='thin'))
                    font_ = Font(size=12)
                    ws["A1"].font = font_
                    ws["A1"].value = f"{self.dkr_name}利息清单"  # 添加内容
                    ws["A1"].border = border
                    try:
                        # 总表剩余本金
                        zbsybj = df1["剩余本金"][i]
                        # 总表剩余期内利息
                        zbsyqnlx = df1["剩余期内利息"][i]

                        print(self.dkr_name)
                        print(zbsybj)
                        print(zbsyqnlx)
                        a = self.read_ben_xi(out_excel, current_row, self.dkr_dkzh, yqlv, zbsybj, zbsyqnlx)
                        current_row = a[0]
                        zdkbj = float(zdkbj) + float(a[1])
                        zdkbj = '%.2f' % zdkbj
                        bj = float(bj) + float(a[2])
                        bj = '%.2f' % bj
                        qnlx = float(qnlx) + float(a[3])
                        qnlx = '%.2f' % qnlx
                        yqfx = float(yqfx) + float(a[4])
                        yqfx = '%.2f' % yqfx
                        current_rows = a

                    except:
                        logger.error("出现错误", self.dkr_name, "执行下个位")
                        continue
            if len(dkbhs) == 0:
                continue
            try:
                border = Border(left=Side(border_style=None,
                                          color='FF000000',
                                          style='thin'),
                                right=Side(border_style=None,
                                           color='FF000000',
                                           style='thin'),
                                top=Side(border_style=None,
                                         color='FF000000',
                                         style='thin'),
                                bottom=Side(border_style=None,
                                            color='FF000000',
                                            style='thin'))

                current_row = current_rows[0]
                num = int(current_row) + 3
                # print(num)
                ws[f"A{num}"].value = ""
                ws[f"A{num}"].border = border
                ws[f"B{num}"].value = "总贷款本金"
                ws[f"B{num}"].border = border
                ws[f"C{num}"].value = "实还本金"
                ws[f"C{num}"].border = border
                ws[f"D{num}"].value = "剩余本金"
                ws[f"D{num}"].border = border
                ws[f"E{num}"].value = "剩余期内利息"
                ws[f"E{num}"].border = border
                ws[f"F{num}"].value = "剩余逾期罚息"
                ws[f"F{num}"].border = border
                ws[f"G{num}"].value = "合计欠款"
                ws[f"G{num}"].border = border

                num = int(current_row) + 4
                # print(num)
                shbj = float(zdkbj) - float(bj)
                shbj = '%.2f' % shbj
                hjqk = float(bj) + float(qnlx) + float(yqfx)
                hjqk = '%.2f' % hjqk

                ws[f"A{num}"].value = f"客户总计\n（截止{self.select_data}）"

                ws[f"A{num}"].border = border
                ws[f"B{num}"].value = f"{zdkbj}"
                ws[f"B{num}"].border = border
                ws[f"C{num}"].value = f"{shbj}"
                ws[f"C{num}"].border = border
                ws[f"D{num}"].value = f"{bj}"
                ws[f"D{num}"].border = border
                ws[f"E{num}"].value = f"{qnlx}"
                ws[f"E{num}"].border = border
                ws[f"F{num}"].value = f"{yqfx}"
                ws[f"F{num}"].border = border
                ws[f"G{num}"].value = f"{hjqk}"
                ws[f"G{num}"].border = border
                # print(dkbhs)
                self.formatting(dkbhs, ws)
                ws[f"A{num}"].alignment = Alignment(wrapText=True, horizontal='center', vertical='center')
            except Exception as e:
                self.error.append(str(self.dkr_name)+"-"+str(self.dkr_id))
                continue
            out_excel.save(os.path.join(self.save_path, f"{self.dkr_name}-{self.dkr_id}-等额本息.xlsx"))

    def formatting(self, nums, sheet):
        # print("*************************************************************************************************整体修改")
        zhs = sheet.max_row
        for num in nums:
            lists = []
            for row in sheet.iter_rows(min_row=1, max_row=51104,
                                       min_col=1, max_col=2):
                for cell in row:
                    if cell.value == num:
                        lists.append(cell.coordinate)
            a = lists[0]
            b = lists[-1]
            sheet.merge_cells(f"{a}:{b}")

        alignment_center = Alignment(horizontal='center', vertical='center')
        ws_area = sheet[f"A3:G{zhs}"]
        for i in ws_area:
            for j in i:
                j.alignment = alignment_center
        for i in sheet[1]:
            sheet.column_dimensions[i.coordinate[0]].width = 24
            if i.coordinate[0] in ["D", 'E', "F"]:
                sheet.column_dimensions[i.coordinate[0]].width = 12
            elif i.coordinate[0] in ["G", 'H']:
                sheet.column_dimensions[i.coordinate[0]].width = 22

    def run(self):
        self.read_summary_statement()
        self.selet()
        logger.info("执行完成")
        for i in self.error:
            print(i)
            a = os.getcwd()
            path = os.path.join(a, "error.txt")
            with open(path, 'a', ) as file:
                file.write(i + f"时间为：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
            if i != "":
                logger.info(f"错误信息保存在：{path}")



export = ScriptDef(
    cls=NB_LiXi,
    group="其他",
    title="宁波银行证据合并",
    arguments=[
        FileItem(title="总表", name="summary_statement"),
        FileItem(title="对照表", name="excel_path"),
        DirectoryItem(title="保存地址", name="save_path"),
        StringItem(title="逾期时间", name="select_data"),
               ]
)

if __name__ == '__main__':
    a = NB_LiXi(
        r"C:\Users\9000\Desktop\测试\00-汉资100户清单20220607.xlsx",
        r"C:\Users\9000\Desktop\测试\等额本息-20220607.xlsx",
        r"C:\Users\9000\Desktop\测试\cc", "2022-6-7").run()