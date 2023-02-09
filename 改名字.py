# # -*- coding: utf-8 -*-
# import os
# import re
# import shutil
#
# from flows.flow import ScriptDef, DirectoryItem
# from rpalib.log import logger
#
# global old_floder
# new_floder = r'\\172.29.9.15\资料管理prod\进件材料\挖财'
#
#
# class Item:
#     ah: str
#
#
# def GetIdCardAndName(floder_name: str):
#     match_obj = re.match(r'([\u4e00-\u9fa5]+)(\d+)', floder_name)
#     name = match_obj.group(1)
#     id_card = match_obj.group(2)
#     return name, id_card
#
#
# def GetJinJianId(name: str, IdCard: str):
#     JinJianId = ""
#     base_floder = os.path.join(old_floder, f'{name}{IdCard}')
#     for file in os.listdir(base_floder):
#         if file.startswith(f'{name}-{IdCard}') and file.endswith('代偿凭证.pdf'):
#             JinJianId = file.split("-")[2]
#             break
#     return JinJianId, base_floder
#
#
# def Process(name: str, IdCard: str, JinJianId: str, base_floder: str):
#     floder = os.path.join(new_floder, JinJianId)
#     if not os.path.exists(floder):
#         os.makedirs(floder)
#     try:
#         for file in os.listdir(base_floder):
#             if file.endswith("OCR人脸识别照片.png"):
#                 shutil.copyfile(os.path.join(base_floder, file), os.path.join(floder, f'人脸识别-{name}-{IdCard}.png'))
#             if file.endswith("出借人列表.pdf"):
#                 shutil.copyfile(os.path.join(base_floder, file), os.path.join(floder, f'出借人列表-{name}-{IdCard}.pdf'))
#             if file.endswith("代偿凭证.pdf"):
#                 shutil.copyfile(os.path.join(base_floder, file), os.path.join(floder, f'代偿凭证-{name}-{IdCard}.pdf'))
#             if file.endswith("贷款标的债转情况说明函.pdf"):
#                 shutil.copyfile(os.path.join(base_floder, file),
#                                 os.path.join(floder, f'贷款标的债转情况说明函-{name}-{IdCard}.pdf'))
#             if file.endswith("短信凭证.pdf"):
#                 shutil.copyfile(os.path.join(base_floder, file), os.path.join(floder, f'债转通知-001-{name}-{IdCard}.pdf'))
#             if file.endswith("放款凭证.pdf"):
#                 shutil.copyfile(os.path.join(base_floder, file), os.path.join(floder, f'放款凭证-{name}-{IdCard}.pdf'))
#             if file.endswith("风险保障金.pdf"):
#                 shutil.copyfile(os.path.join(base_floder, file), os.path.join(floder, f'风险保障协议-{name}-{IdCard}.pdf'))
#             if file.endswith("还款计划.pdf"):
#                 shutil.copyfile(os.path.join(base_floder, file), os.path.join(floder, f'还款及代偿明细表-{name}-{IdCard}.pdf'))
#             if file.endswith("借款协议.pdf"):
#                 shutil.copyfile(os.path.join(base_floder, file), os.path.join(floder, f'借款协议-{name}-{IdCard}.pdf'))
#             if "出借人vs挖财" and "债转通知情况说明" in file:
#                 shutil.copyfile(os.path.join(base_floder, file),
#                                 os.path.join(floder, f'债转通知-002-（出借人vs挖财）-{name}-{IdCard}.pdf'))
#             if "聚宝vs汉资" and "债转通知情况说明" in file:
#                 shutil.copyfile(os.path.join(base_floder, file),
#                                 os.path.join(floder, f'债转通知-005-（聚宝vs汉资）-{name}-{IdCard}.pdf'))
#             if "挖财vs聚宝" and "债转通知情况说明" in file:
#                 shutil.copyfile(os.path.join(base_floder, file),
#                                 os.path.join(floder, f'债转通知-003-（挖财vs聚宝）-{name}-{IdCard}.pdf'))
#             if "祥丰vs聚宝" and "债转通知情况说明" in file:
#                 shutil.copyfile(os.path.join(base_floder, file),
#                                 os.path.join(floder, f'债转通知-004-（祥丰vs聚宝）-{name}-{IdCard}.pdf'))
#             if "聚宝vs汉资" and "债转协议" in file:
#                 shutil.copyfile(os.path.join(base_floder, file),
#                                 os.path.join(floder, f'债转协议-005-（聚宝vs汉资）-{name}-{IdCard}.pdf'))
#             if "挖网vs聚宝" and "债转协议" in file:
#                 shutil.copyfile(os.path.join(base_floder, file),
#                                 os.path.join(floder, f'债转协议-003-（挖网vs聚宝）-{name}-{IdCard}.pdf'))
#
#             if "祥丰vs聚宝" and "债转协议" in file:
#                 shutil.copyfile(os.path.join(base_floder, file),
#                                 os.path.join(floder, f'债转协议-004-（祥丰vs聚宝）-{name}-{IdCard}.pdf'))
#
#             if file.endswith("被告身份证反面.png"):
#                 shutil.copyfile(os.path.join(base_floder, file),
#                                 os.path.join(floder, f'被告身份证-反面-{name}-{IdCard}.png'))
#
#             if file.endswith("被告身份证正面.png"):
#                 shutil.copyfile(os.path.join(base_floder, file),
#                                 os.path.join(floder, f'被告身份证-正面-{name}-{IdCard}.png'))
#     except Exception as e:
#         logger.error(f"文件处理失败,失败原因--{e}")
#
#
# def run(oldfloder):
#     global old_floder
#     old_floder = oldfloder
#     logger.info("程序开始执行----->")
#     floder_name_list = os.listdir(old_floder)
#     for index, floder_name in enumerate(floder_name_list):
#         logger.info(f"正在处理第{index + 1}个文件夹")
#         name, IdCard = GetIdCardAndName(floder_name)
#         JinJianId, base_floder = GetJinJianId(name, IdCard)
#         Process(name, IdCard, JinJianId, base_floder)
#     logger.info("文件整理完毕")
#
#
# export = ScriptDef(
#     func=run,
#     group='挖财资料导入nas',
#     title="挖财资料导入nas",
#     description="挖财资料导入nas",  # 描述
#     arguments=[
#         DirectoryItem(title="请选择要上传的文件夹路径", name="oldfloder"),
#     ]
# )
#
# if __name__ == '__main__':
#     run(r'C:\Users\9000\Documents\WeChat Files\wxid_5y9jy4201wkc21\FileStorage\File\2022-04\案件样例-维信-挖财-东岸\案件样例-维信-挖财-东岸\案件样例-整理前\挖财')


# import os
# import shutil
# import time
# import fire
# from flows.flow import ScriptDef, DirectoryItem, ListDataFlow
# from rpalib.log import logger
#
# name_dict = {
#     "5%代偿": "代偿凭证-5%代偿",
#     "95%受让+原状分配": "受让凭证-95%受让+原状分配",
#     "一次债转通知（维信）": "债转通知-（维信）",
#     "一次债转通知（维仕）": "债转通知-（维仕）",
#     "一次债转协议（维仕）": "债转协议-（维仕）",
#     "一次债转协议（维信）": "债转协议-（维信）",
#     "OCR人脸识别照片": "人脸识别",
#     "被告身份证正面": "被告身份证-正面",
#     "被告身份证反面": "被告身份证-反面",
# }
#
#
# class Weixin(ListDataFlow):
#
#     def __init__(self, dir_path):
#         super().__init__()
#         self.dir_path = dir_path
#         self.out_path = r"\\172.29.9.15\资料管理prod\进件材料\维信"
#
#     def check_path(self, path):
#         if not os.path.exists(path):
#             os.mkdir(path)
#
#     def run(self):
#         # self.check_path(self.out_path)
#         # shutil.copytree(self.dir_path, self.out_path)
#         # logger.info(f'复制文件到nas中')
#         dir_list = os.listdir(self.dir_path)
#         try:
#             for old_dir_name in dir_list:
#                 logger.info(f'复制文件到nas中')
#                 shutil.copytree(os.path.join(self.dir_path, old_dir_name), os.path.join(self.out_path, old_dir_name))
#                 file_list = os.listdir(os.path.join(self.out_path, old_dir_name))
#                 for file_name in file_list:
#                     logger.info(f'正在重命名文件{file_name}')
#                     filename, extension = os.path.splitext(file_name)
#                     if extension == '.pdf':
#                         name, id_card, part_id, other = filename.split('-')
#                         name_dict['进件号'] = part_id
#                         if other in name_dict.keys():
#                             new_filename = name_dict[other] + '-' + name + '-' + id_card + extension
#                         else:
#                             new_filename = other + '-' + name + '-' + id_card + extension
#                         os.rename(os.path.join(self.out_path, old_dir_name, file_name),
#                                   os.path.join(self.out_path, old_dir_name, new_filename))
#                     elif extension == '.jpg':
#                         if len(filename.split('-')) > 3:
#                             name, id_card, part_id, other = filename.split('-')
#                             if part_id in name_dict.keys():
#                                 new_filename = name_dict[part_id] + '-' + name + '-' + id_card + extension
#                             elif other in name_dict.keys():
#                                 new_filename = name_dict[other] + '-' + name + '-' + id_card + extension
#                             else:
#                                 new_filename = part_id + '-' + other + '-' + name + '-' + id_card + extension
#                         else:
#                             name, id_card, other = filename.split('-')
#                             if other in name_dict.keys():
#                                 new_filename = name_dict[other] + '-' + name + '-' + id_card + extension
#                             else:
#                                 new_filename = other + '-' + name + '-' + id_card + extension
#                         os.rename(os.path.join(self.out_path, old_dir_name, file_name),
#                                   os.path.join(self.out_path, old_dir_name, new_filename))
#                     else:
#                         print(1)
#                     # if not os.path.exists(os.path.join(self.out_path, name_dict['进件号'])):
#                     #     os.mkdir(os.path.join(self.out_path, name_dict['进件号']))
#                     # file_name = os.path.join(self.dir_path, old_dir_name, file_name)
#                     # new_filename = os.path.join(self.out_path, name_dict['进件号'], new_filename)
#                     # cmd = f'copy "{file_name}" "{new_filename}"'
#                     # os.system(cmd)
#                 time.sleep(1)
#                 os.rename(os.path.join(self.out_path, old_dir_name), os.path.join(self.out_path, name_dict['进件号']))
#                 logger.info(f'重命名文件夹')
#         except Exception as e:
#             logger.error(f'程序报错{e}')
#
#
# export = ScriptDef(
#     cls=Weixin,
#     group='维信nas文件导入',
#     title="维信nas文件导入",
#     description="维信nas文件导入",
#     arguments=[
#         DirectoryItem(title="需要导入的文件夹", name="dir_path"),
#     ]
# )
#
# if __name__ == '__main__':
#     Weixin(r"C:\Users\9000\Desktop\下载管理\案件样例-维信-挖财-东岸\案件样例-维信-挖财-东岸\案件样例-整理前\维信").run()




"""
    输入东岸要处理的文件夹路径
    将文件夹下的文件重命名,并导入到nas进件/东岸文件夹下
"""

import os
import re
from flows.flow import FlowDefinition, SelectItem, UserSelectItem, StringItem, ListDataFlow, ScriptDef, DirectoryItem
from rpalib.log import logger


class UploadNas(ListDataFlow):
    def __init__(self, path11):
        super().__init__()
        self.path = path11
        self.nas_path = r"\\172.29.9.15\资料管理prod\进件材料\东岸"
        self.number = {"中世普惠vs数禾": "001", "数禾vs顺亿": "002", "顺亿vs丽水": "003", "丽水vs新满业": "004"}

    def run(self):
        try:
            for _dir in os.listdir(self.path):
                data = {}
                logger.info(f"文件夹{_dir}开始导入")

                for file in os.listdir(os.path.join(self.path, _dir)):
                    file_name, end_file = os.path.splitext(file)
                    data["姓名"] = file_name.split("-")[0]
                    data["身份证号"] = file_name.split("-")[1]
                    if len(file_name.split("-")) > 3:
                        data["进件号"] = file_name.split("-")[2]
                    data["材料名"] = file_name.split("-")[-1]

                    # 材料名 编号处理
                    temp = re.findall("\w+vs\w+", data.get("材料名"))
                    temp = temp[0] if bool(temp) else None
                    data["材料名"] = data.get("材料名").replace("（", f"-{self.number.get(temp)}-（") if self.number.get(
                        temp) else data.get("材料名")

                    # 身份证 正反面 加-2
                    if "被告身份证" in data["材料名"]:
                        data["材料名"] = data["材料名"].replace("被告身份证", "被告身份证-")

                    # 债转确认函 改成 债转协议
                    data["材料名"] = "债转协议-001-（中世普惠vs数禾）" if data.get("材料名") == "债转确认函" else data.get("材料名")

                    # 新建进件号文件
                    if not os.path.exists(os.path.join(self.nas_path, data.get("进件号"))):
                        os.mkdir(os.path.join(self.nas_path, data.get("进件号")))

                    # 导入nas
                    file_path = os.path.join(self.path, _dir, file)

                    copy_path = os.path.join(self.nas_path, data["进件号"],
                                             fr"{data.get('材料名')}-{data.get('姓名')}-{data.get('身份证号')}{end_file}")

                    cmd = f'copy "{file_path}" "{copy_path}"'
                    os.system(cmd)
                logger.info(f"文件夹{_dir}开始完成 ")
        except Exception as e:
            logger.error(e)
            logger.error(e.__traceback__.tb_lineno)


export = ScriptDef(
    cls=UploadNas,
    group='东岸资料导入nas',
    title="东岸资料导入nas",
    description="东岸资料导入nas",  # 描述
    arguments=[
        DirectoryItem(title="请选择要上传的文件夹路径", name="path11"),
    ]
)

if __name__ == '__main__':
    UploadNas(r"D:\temp\案件样例-维信-挖财-东岸\案件样例-整理前\东岸").run()
