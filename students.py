import os
import shutil
import time

import fitz
import win32api
import win32print
from PIL import ImageFont, ImageDraw, Image
from openpyxl import load_workbook
from flows.flow import ScriptDef, ListDataFlow, FileItem, DirectoryItem, SelectItem
from rpalib.log import logger
from rpalib import excel


class ConfigItem(object):
    # 文件夹
    files: str
    # '文件名'
    file_name: str
    # 跳页
    jump_num: str

    def __str__(self):
        return f"{self.files}-{self.file_name}"


class Item(object):
    # '证件号'
    idcar_num: str
    # 姓名
    bsqr_name: str
    # 案号
    an_number: str

    def __str__(self):
        return f"{self.bsqr_name}-{self.idcar_num}"


class ImgFlow(ListDataFlow):

    def __init__(self, path_f, config_excel_file, item_excel_file, pdfFilePath, default_print) -> None:
        super().__init__()
        self.path_f = path_f
        self.config_excel_file = config_excel_file
        self.item_excel_file = item_excel_file
        self.save_path1 = './guidang_jpg_1/'  # 查找出要处理的数据要保存的路径
        self.pdfFilePath = pdfFilePath  # 将pdf拆分成图片并添加角标保存的文件的路径
        self.default_print = default_print

    def precheck(self):
        self.load_list()

    def printer_loading(self, filename=None, chooseDuplex=1, chooseColor=1, chooseCopies=1):
        handle = win32print.SetDefaultPrinter(self.default_print)
        printer = win32print.GetDefaultPrinter()
        PRINTER_DEFAULTS = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
        pHandle = win32print.OpenPrinter(printer, PRINTER_DEFAULTS)
        level = 2
        properties = win32print.GetPrinter(pHandle, level)
        # properties['pDevMode'].Orientation = 2  这种设置不行，会挂掉，需要搞个对象出来，如pDevModeObj = properties["pDevMode"]
        pDevModeObj = properties["pDevMode"]
        pDevModeObj.Duplex = int(chooseDuplex)  # 1单面 2长边装订双面 3短边装订双面
        pDevModeObj.Orientation = 2  # 纵向打印（暂时无法横向打印）
        pDevModeObj.Color = int(chooseColor)  # 0彩色 1黑白
        pDevModeObj.Copies = int(chooseCopies)  # 份数
        properties["pDevMode"] = pDevModeObj
        try:
            win32print.SetPrinter(pHandle, level, properties, 0)
        except Exception as e:
            raise Exception(f"设置打印机出错了.\n错误原因：{e}")
        res = win32api.ShellExecute(0, 'print', filename, None, '.', 0)  # 这里有个如果缺纸，问题怎么解决
        time.sleep(2)  # 这里不知道怎么通过程序判断物理打印机完成了打印动作，如果有合适的只能等待，把这个time.sleep换掉
        win32print.ClosePrinter(pHandle)

    def load_list(self):
        items = excel.loads(
            self.item_excel_file, Item, {
                "idcar_num": {"title": "被申请人证件号码", "required": True},
                "bsqr_name": {"title": "被申请人姓名", "required": True},
                "an_number": {"title": "财保案号", "required": True},
            })
        self.config_items = excel.loads(
            self.config_excel_file, ConfigItem, {
                "files": {"title": "文件夹", "required": True},
                "file_name": {"title": "文件名", "required": True},
                "jump_num": {"title": "跳页", "required": True},
                'page_whether': {"title": "是否标码", "required": True},
                'print_mode': {"title": "打印模式", "required": True},
            })
        error_list = []
        for item in items:
            for config in self.config_items:
                dir_name = f"{self.path_f}\\{config.files}"
                file_name = config.file_name.format(name=item.bsqr_name, idcard=item.idcar_num)
                file_list = self.find_files(dir_name, file_name)
                has_file = list(
                    filter(lambda x: x.endswith(".pdf") or x.endswith(".jpg") or x.endswith(".jpeg"), file_list))
                if not has_file:
                    error_list.append((item, config))
        if error_list:
            for item, config in error_list:
                logger.info(f"{item}的{config}文件缺失")
            raise Exception("数据校验未通过")

        return items

    # 合并PDF
    def merge_Pdf(self, temp_dir, an_jian):
        jpg_list = []
        res = []
        jpg_list_file = []
        path_file = None
        logger.info('调用合并pdf函数........')
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                path_file = root
                jpg_list.append(file)
        for x in jpg_list:
            res.append(int(x.split('.')[0]))
        res.sort()
        for f in res:
            jpg = f'{path_file}/{str(f)}.jpg'
            jpg_list_file.append(jpg)
        output = None
        sources = []
        for jpg_ff in jpg_list_file:
            pngFile = Image.open(jpg_ff)
            if pngFile.mode == "RGB":
                pngFile = pngFile.convert("RGB")
            elif pngFile.mode == "L":
                pngFile = pngFile.convert("L")
            if output is None:
                output = pngFile
            else:
                sources.append(pngFile)
        # output.save(f'{self.pdfFilePath}\\{an_jian.an_number}-{an_jian.bsqr_name}-{an_jian.idcar_num}.pdf', 'pdf',
        #             save_all=True, append_images=sources)
        output.save(f'{an_jian}', 'pdf',
                    save_all=True, append_images=sources)
        logger.info('----------------------->合并整个PDF完成！<-----------------------')
        sources = []
        output.close()

    # 添加角标并替换原图片
    def img_add_num(self, img_path, n, page_whether):
        fontpath = os.path.join(os.path.dirname(__file__), "INKDRAFT.TTF")  # "font/simhei.ttf"  # 常规黑体样式
        logger.info(f"字体文件：{fontpath}")
        font = ImageFont.truetype(fontpath, 80)
        img1 = Image.open(img_path)
        img1_x, img1_y = img1.size
        if img1_x < 2437 or img1_y < 3498:
            im1 = Image.open(img_path)
            img_deal1 = im1.resize((2437, 3489), Image.ANTIALIAS)  # 转化图片大小
        else:
            img_deal1 = Image.open(img_path)

        # 在图片上添加文字
        draw = ImageDraw.Draw(img_deal1)
        try:
            if page_whether == '否':
                draw.text((2300, 100), "", (43, 43, 43), font=font)
            else:
                draw.text((2300, 100), f"{n}", (43, 43, 43), font=font)
        except Exception:
            if page_whether == '否':
                draw.text((2300, 100), "", font=font)
            else:
                draw.text((2300, 100), f"{n}", font=font)
        # 保存
        img_deal1.save(img_path)
        if page_whether == '否':
            logger.info(f'原图片{n}正在合并')
        else:
            logger.info(f'原图片添加角标{n}')

    def find_files(self, parent, filename):
        result = []
        for root, dirs, files in os.walk(parent):
            for file in files:
                if filename in file:
                    result.append(os.path.join(root, file))
        return result

    # 处理pdf
    def process_pdf(self, pdf_file_path, temp_dir, start_page, page_whether):
        doc = fitz.open(pdf_file_path)
        page_number = start_page
        for pg in range(doc.pageCount):
            page = doc[pg]
            rotate = int(0)
            # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
            # 此处若是不做设置，默认图片大小为：792X612, dpi=96
            zoom_x = 3.0  # (1.33333333-->1056x816)   (2-->1584x1224)
            zoom_y = 3.0
            mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            pix = page.getPixmap(matrix=mat, alpha=False)
            if pix.width > pix.height:
                logger.info(f'图片旋转90度！')
                rotate = int(-90)
                mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
                pix = page.getPixmap(matrix=mat, alpha=False)
            image_path = f'{temp_dir}\\{page_number}.jpg'
            pix.writePNG(image_path)  # 将图片写入指定的文件夹内
            self.img_add_num(image_path, page_number, page_whether)
            page_number += 1
        return page_number

    # 处理jpg
    def process_jpg(self, jpg_file_path, temp_dir, start_page, page_whether):
        page = start_page
        image_path = f'{temp_dir}\\{page}.jpg'
        shutil.copy(jpg_file_path, image_path)
        if '备考表' not in jpg_file_path:
            self.img_add_num(image_path, page, page_whether)
        page += 1

        return page

    def remove_file(self, dir):
        for file in os.listdir(dir):
            if file.endswith('png') or file.endswith('jpeg') or file.endswith('jpg'):
                file = os.path.join(dir, file)
                os.remove(file)

    def create_pdf(self, file):
        doc = fitz.Document()
        doc.new_page()
        doc.save(file)

    # 小于A4纸的进行处理
    def jpg_(self, jpg_file):
        # 生成一张空白页
        img_blank = Image.new('RGB', (2437, 3498), (255, 255, 255))
        margin_x, margin_y = img_blank.size
        img1 = Image.open(jpg_file)
        img1_x, img1_y = img1.size
        if img1_x < 2437 or img1_y < 3498:
            if img1_x > img1_y:
                img1 = img1.rotate(90, expand=True)
            img1_x, img1_y = img1.size
            img1 = img1.resize((int(img1_x * 2), int(img1_y * 2)), Image.ANTIALIAS)
            img1_x, img1_y = img1.size
            position = ((round(int((margin_x - img1_x) / 2)), round(int(margin_y - img1_y) / 2)))
            img_blank.paste(img1, position)
            logger.info('小于A4纸进行粘贴！')
            # img_blank.show()
            # 替换掉原图片
            img_blank.save(f'{jpg_file}')

    def run_job(self, item):
        current_page = 1
        an_jian = item
        logger.info(f'-----{an_jian.bsqr_name}-{an_jian.idcar_num}----')
        temp_dir = f"{self.save_path1}{an_jian.an_number}"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        for item in self.config_items:
            current_page += int(item.jump_num)
            dir_name = f"{self.path_f}\\{item.files}"
            file_name = item.file_name.format(name=an_jian.bsqr_name, idcard=an_jian.idcar_num)
            file_list = self.find_files(dir_name, file_name)
            # logger.info('判断是否添加页码：', item.page_whether)
            print_mode = None
            page_whether = item.page_whether
            if item.print_mode == "单面":  # 在这里将表格里的数据转换下，传给打印机使用
                print_mode = 1
            if item.print_mode == "双面":
                print_mode = 2
            for f in file_list:  # 这个列表里村的是单个文件----不管文件夹下有几个文件，只选一个唯一匹配的文件
                if f.endswith("pdf"):
                    current_page = self.process_pdf(f, temp_dir, current_page, page_whether)
                    print_pdf_path = self.merge_Pdf(temp_dir, f)
                    self.remove_file(temp_dir)
                    self.printer_loading(filename=f, chooseDuplex=print_mode, chooseColor=1,chooseCopies=1)
                elif f.endswith("jpg") or f.endswith('jpeg'):
                    self.jpg_(f)
                    current_page = self.process_jpg(f, temp_dir, current_page, page_whether)
                    if f.endswith('jpg'):
                        f = f.replace('jpg', 'pdf')
                    if f.endswith('jpeg'):
                        f = f.replace('jpeg', 'pdf')
                    self.create_pdf(f)
                    print_pdf_path = self.merge_Pdf(temp_dir, f)
                    self.remove_file(temp_dir)
                    self.printer_loading(filename=f, chooseDuplex=print_mode, chooseColor=1,chooseCopies=1)
                else:
                    raise Exception("未知文件")


export = ScriptDef(
    cls=ImgFlow,
    group="归档",
    title="财保卷宗归档-打印机",
    arguments=[
        DirectoryItem(title="要处理文件的路径：", name="path_f"),
        # SelectItem(title="操作", name="default_print", options=["合成PDF", "直接打印"]),  这个选择放在了表格里，如果打印模式字段有值为“单面”或“双面”则打印，否则不打印。
        DirectoryItem(title="保存PDF文件的路径：", name="pdfFilePath"),
        FileItem(title="文件信息命名excel文件路径：", name="config_excel_file"),
        FileItem(title="被告人信息的excel文件路径：", name="item_excel_file"),
        SelectItem(title="打印机", name="default_print", options=[it[2] for it in win32print.EnumPrinters(2)]),  # 在这里选择打印机
    ]
)

if __name__ == '__main__':
    # 启动程序，从nas找到归档文件夹
    path_f = r'C:\Users\Administrator\Desktop\归档'
    config_excel_file = r"C:\Users\Administrator\Desktop\归档\财保归档文件夹命名&排序模板(1).xlsx"
    item_excel_file = r"C:\Users\Administrator\Desktop\归档\数据表头.xlsx"
    pdfFilePath = r'C:\Users\Administrator\Desktop\归档\pdf存储路径'
    default_print = 'EPSONB6589D (WF-C5290 Series)'
    ImgFlow(path_f, config_excel_file, item_excel_file, pdfFilePath,
            default_print,
            ).run()  # EPSONB6589D (WF-C5290 Series)这个是打印机的名字，如我的是['钉钉智能云打印机', '导出为WPS PDF', 'Microsoft XPS Document Writer', 'Microsoft Print to PDF', 'Fax', 'EPSONB6589D (WF-C5290 Series)']，选一个