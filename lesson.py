
# ''' selenium 公司封装用法'''
# # import time
# #
# # from rpalib import browser
# # try:
# #     b = browser.create_chrome()
# #     b.load(r"https://www.baidu.com")
# #     b.clear_input(r'//*[@id="kw"]', '中国法院执行信息公开网查询')
# #     time.sleep(3)
# #     b.click(r'//*[@id="su"]')
# #     time.sleep(3)
# #     b.click(r'//*[@id="1"]/h3/a[1]')
# #     time.sleep(4)
# #     b.switch_to_window_by_title(title='中国执行信息公开网')
# #     b.click(r'//*[@id="cccz"]/div[1]')
# #     b.click(r'//*[@id="myDiv1"]/a[1]/div')
# #     b.switch_to_window_by_title(title='询价评估')
# #     b.click(r'//*[@id="table1"]/tbody/tr[1]/td/a')
# #     b.switch_to_window_by_title(title='司法拍卖-京东拍卖')
# #     b.click(r'//*[@id="Underway"]/div/div[2]/div[1]/div[1]/div[3]/ul/li[1]/a/div[1]/div[1]')
# #     print('ok')
# # except:
# #         pass
#
#
#
#
# ''' selenium 基础用法'''
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# driver = webdriver.Chrome('chromedriver.exe')
# driver.maximize_window()
# driver.get("https://www.baidu,com/")
# # driver.get("http://www.jrskan.com/")
# # time.sleep(5)
# # print(driver.switch_to.alert.text)  # 获取弹窗的文本信息
# # driver.switch_to.alert.accept()  # 点击弹窗确定
# # driver.switch_to.alert.dismiss()  # 点击弹窗取消
# # driver.switch_to.alert.send_keys('xxxx')  # 向弹窗中输入信息
#
# driver.maximize_window()
# driver.find_element(By.XPATH, '//*[@id="kw"]').send_keys("中国法院执行信息公开网查询")
# time.sleep(3)
# driver.find_element(By.XPATH, '//*[@id="su"]').click()
# time.sleep(3)
# driver.find_element(By.XPATH, '//*[@id="1"]/h3/a[1]').click()
# time.sleep(4)
# driver.switch_to.window(driver.window_handles[1])
#
# driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/a[1]/div').click()
#
#
#
#
# ''' selenium 控制滚动条下滑'''
# from selenium import webdriver
#
# browser = webdriver.Chrome()
# browser.get('https://www.zhihu.com/explore')
# browser.execute_script('window.scrollTo(0, 2000)')  # 控制滚动条到具体的位置
#
#
# from selenium import webdriver
# from selenium.webdriver import ActionChains
#
# browser = webdriver.Chrome()
# url = 'https://www.zhihu.com/explore'
# browser.get(url)
# logo = browser.find_elements_by_xpath('//*[@id="guestSquare"]/div[2]/div/div[2]/div[2]/div/div/div[1]/a')
# for i in logo:
#     print(i.text)
# print(logo.get_attribute('class'))
#
#
#
import os
path = r'\\172.29.9.15\技术部专用\rpa测试样例\39-律师平台立案支持一个案号推多个被告\样例\被告资料\白立立350500198309022552'
# xx = r'\\172.29.9.15\技术部专用\rpa测试样例\39-律师平台立案支持一个案号推多个被告\样例\被告资料\白立立350500198309022552'
# # print(os.path.join(path, '白立立-350500198309022552-起诉状0001-1.jpg'))
# a = os.path.join(path, '白立立-350500198309022552-起诉状.jpg')
# print(os.path.exists(a))

for i in os.listdir(r'\\172.29.9.15\技术部专用\rpa测试样例\39-律师平台立案支持一个案号推多个被告\样例\被告资料\白立立350500198309022552'):
    # print(i)

    if i.find("pdf") != -1:
        continue
    elif '起诉状' in i:
        print(i)
        # ps = os.path.join(path, i)
        # print(path)
        # print(os.path.exists(path))


# lj = self.main_path + '被告资料' + f'{self.snap[1].get("bgxm")}{self.snap[1].get("bgid")}'
#         for i in os.listdir(lj):
#             if i.find("pdf") != -1:
#                 continue
#             elif '起诉状' in i:
#                 path = os.path.join(self.main_path, "被告资料", f'{self.snap[1].get("bgxm")}{self.snap[1].get("bgid")}', i)
#                 self.upload(path, payload)


