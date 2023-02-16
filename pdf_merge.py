"""
-*- coding: utf-8 -*-
@Time : 2023/2/16 10:39
"""
import os
import shutil
import fitz
from PIL import ImageFont, ImageDraw, Image, ImageFile
from log import logger


class ConfigItem(object):
    # 文件夹
    files: str
    # '文件名'
    file_name: str
    # 跳页
    jump_num: str

    def __str__(self):
        return f"{self.files}-{self.file_name}"


class ImgFlow(object):

    def __init__(self, path_f, demand) -> None:
        super().__init__()
        self.path_f = path_f
        self.demand = demand
        self.save_path1 = './guidang_jpg_1/'  # 查找出要处理的数据要保存的路径
        self.pdfFilePath = None  # 将pdf拆分成图片并添加角标保存的文件的路径
        self.path = None
        self.merger = None

    # 合并PDF
    def merge_pdf(self, temp_dir, an_jian):
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
        output.save(f'{self.path}\\{an_jian}.pdf', 'pdf',
                    save_all=True, append_images=sources)
        logger.info('----------------------->合并整个PDF完成！<-----------------------')

    # 添加角标并替换原图片
    def img_add_num(self, jpg_file_path, img_path, n, photo_type):
        fontpath = "font/simhei.ttf"  # 常规黑体样式
        font = ImageFont.truetype(fontpath, 80)
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        Image.MAX_IMAGE_PIXELS = None
        img1 = Image.open(img_path)
        img1_x, img1_y = img1.size
        height = int(2437 * img1_y / img1_x)
        img_deal1 = img1.resize((2437, height), Image.ANTIALIAS)
        # 在图片上添加文字
        draw = ImageDraw.Draw(img_deal1)
        try:
            if photo_type == 1:
                draw.text((1216, 1600), f"{n}", (43, 43, 43), font=font)
            else:
                draw.text((1216, 3300), f"{n}", (43, 43, 43), font=font)
        except Exception:
            if photo_type == 1:
                draw.text((1216, 1600), f"{n}", font=font)
            else:
                draw.text((1216, 3300), f"{n}", font=font)
        # 保存
        img_deal1.save(img_path)
        logger.info(f'原图片添加角标{n}')

    # 处理pdf
    def process_pdf(self, pdf_file_path, temp_dir, start_page):
        doc = fitz.Document(pdf_file_path)
        page_number = start_page
        for pg in range(doc.page_count):
            x = str(page_number)
            page = doc[pg]
            # time.sleep(2000)
            rotate = int(0)
            # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
            # 此处若是不做设置，默认图片大小为：792X612, dpi=96
            zoom_x = 3.0  # (1.33333333-->1056x816)   (2-->1584x1224)
            zoom_y = 3.0
            mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            photo_type = 0
            if pix.width > pix.height:
                mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                photo_type = 1
            image_path = f'{temp_dir}\\{page_number}.jpg'
            pix.save(image_path)  # 将图片写入指定的文件夹内
            if self.demand == "是":
                self.img_add_num(pdf_file_path, image_path, x, photo_type)
            page_number += 1
        return page_number

    def run(self):

        temp_dir = f"{self.save_path1}\\合并"
        for i in os.listdir(self.path_f):
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            self.path = os.path.join(self.path_f, i)
            an_jian = i.split("-")[0] + "-证据材料"
            if not os.path.isdir(self.path):
                continue
            for e in os.listdir(self.path):
                p = []
                if ".pdf" in e or "证据材料" not in e:
                    continue
                self.pdfFilePath = os.path.join(self.path, e)
                qqq = os.listdir(self.pdfFilePath)
                for v in qqq:
                    if ".pdf" in v:
                        p.append(v)
                p.sort(key=lambda x: int(x.replace("-", '.').split(".")[0]))
                current_page = 1
                for x in p:
                    pdf = os.path.join(self.pdfFilePath, x)
                    if pdf.endswith("pdf"):
                        current_page = self.process_pdf(pdf, temp_dir, current_page)
            # 合并成pdf
            self.merge_pdf(temp_dir, an_jian)
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    path_f = r'C:\Users\9000\Desktop\新建文件夹 (3)(1)'
    ImgFlow(path_f, "是").run()
