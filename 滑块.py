import time, random
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2
import os, base64
from urllib import request

# 账号密码随便输，多试几次会跳出验证码
id_v = '17777777777'  # 京东账号
password_v = '13049267664'  # 京东密码
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 3)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver",{get:() => undefined})'
})
driver.get('https://www.jd.com/')
driver.maximize_window()

# 界面点击账号登录
enter = driver.find_element(By.XPATH, '//*[@id="ttbar-login"]/a[1]').click()  # //*[@id="msShortcutLogin"]/span
# 点击账号登录
login = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div/div[3]/a').click()

# 获取用户名和密码
id = driver.find_element(By.XPATH, '//*[@id="loginname"]')
id.send_keys(id_v)

password = driver.find_element(By.XPATH, '//*[@id="nloginpwd"]')
password.send_keys(password_v)
# 获取登录按钮
btn = driver.find_element(By.XPATH, '//*[@id="loginsubmit"]').click()
y = 0
while True:

    # 验证码原图
    jd_bj = driver.find_element(By.XPATH, '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[1]/img')
    # 滑块图
    jd_hk = driver.find_element(By.XPATH, '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[2]/img')
    # 滑块
    ele_hk = driver.find_element(By.XPATH, '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[2]/div[3]')
    # 提取src属性
    jd_img = jd_bj.get_attribute('src')
    hk_img = jd_hk.get_attribute('src')
    # print(jd_img)
    # print(hk_img)

    request.urlretrieve(jd_img, "jd_bj_img.png")
    request.urlretrieve(hk_img, "hk_bj_img.png")


    def juli():

        bj_rgb = cv2.imread('jd_bj_img.png')
        bj_gray = cv2.cvtColor(bj_rgb, cv2.COLOR_BGR2GRAY)
        hk_rgb = cv2.imread('hk_bj_img.png')
        res = cv2.matchTemplate(bj_rgb, hk_rgb, cv2.TM_CCOEFF_NORMED)
        lo = cv2.minMaxLoc(res)
        # print(lo[2][0])
        return lo[2][0]  # 识别返回滑动距离


    print("下载成功！")
    x = juli()
    print(x)
    # 278:网页原图像素
    # 360:下载后尺寸
    x = int(x * 278 / 360)

    # 滑动滑块
    # seleniu滑动
    action = ActionChains(driver)
    # 按住滑块元素
    action.click_and_hold(ele_hk).perform()


    # def randomNumVaccinePersonTotal(maxValue):
    #     '''生成总和固定的整数序列
    #     maxValue: 序列总和
    #     num：要生成的整数个数
    #
    #     return
    #     per_all_persons:list,指定 num个接种点各自待接种的人数
    #     '''
    #     maxValue = int(maxValue)
    #     suiji_ser = random.sample(range(1, maxValue), k=4 - 1)  # 在1~maxValue之间，采集20个数据
    #     suiji_ser.append(0)  # 加上数据开头
    #     suiji_ser.append(maxValue)
    #     suiji_ser = sorted(suiji_ser)
    #     per_all_persons = [suiji_ser[i] - suiji_ser[i - 1] for i in range(1, len(suiji_ser))]  # 列表推导式，计算列表中每两个数之间的间隔
    #
    #     return per_all_persons
    #
    #
    # track_list = randomNumVaccinePersonTotal(x)
    def get_track(distance):
        """在第三步里：滑块移动轨迹"""
        track = []
        current = 0
        # 阈值
        mid = distance * 2 / 4
        t = 8
        v = 0
        while current < distance:
            if current < mid:
                a = 1
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 2 / 4 * a * t * t
            current += move
            track.append(round(move))
        return track


    # action.move_by_offset(x-50, 0).perform()
    track_list = get_track(x)
    # print(track_list)

    for track in track_list:
        # print(track)
        action.move_by_offset(xoffset=track, yoffset=0).perform()
    # action.move_by_offset(x, 0).perform()
    # time.sleep(1)

    # 松开滑块
    action.release(ele_hk).perform()
    time.sleep(2)
    y = y + x
    if y == x:
        break
    else:
        y = 0
        try:
            driver.find_element(By.XPATH, '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[1]/div[2]').click()
            time.sleep(1)
        except Exception as e:
            break
# import os
#
#
# def run(file_5, file_nlp):
#     list1 = []
#     list2 = []
#     for i in os.listdir(file_5):
#         list1.append(i)
#
#     for e in os.listdir(file_nlp):
#         list2.append(e)
#
#     same, diff = [], []
#     seq = list(set(list2))
#     for i in list(set(list1)):
#         if i not in list2:
#             diff.append(i)
#         else:
#             same.append(i)
#     for j in same:
#         seq.remove(j)
#     print("same is {},xxxxxxxxxxx {}".format(same, diff + seq))
#
#
#
# run(file_5=r"C:\Users\9000\Desktop\新建文件夹 (5)", file_nlp=r"C:\Users\9000\Desktop\nlp\The_picture")
