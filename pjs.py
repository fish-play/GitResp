"""
-*- coding: utf-8 -*-
@Time : 2022/9/23 11:37
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Phantomjs(executable_path="./phantomjs")
driver.get("http://www.baidu.com/")
