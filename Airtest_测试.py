# ''' Airtest 基础用法'''
# # -*- encoding=utf8 -*-
# __author__ = "9000"
#
# from airtest.core.api import *
#
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from airtest_selenium.proxy import WebChrome
#
#
#
# driver = WebChrome()
# driver.implicitly_wait(5)
# driver.get("https://www.sohu.com/")
# driver.maximize_window()   # 最大化窗口
# driver.airtest_touch(Template(r'oldentrancetwo.png'))  # 点击选中的图片r
# driver.switch_to_new_tab()  # 切换页面
# driver.find_element_by_xpath().click()
# driver.airtest_touch(Template(r'img.png'))
# # text("俄乌")
# auto_setup(__file__)

#
# thisset = {"apple", "banana", "cherry"}
# for i in thisset:
#     print(i)



import shutil


shutil.copy("D:\\qq\\config.xml.txd", r'D:\qq_world\All Users')