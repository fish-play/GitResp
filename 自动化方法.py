# -*- coding: utf-8 -*-
import collections
import logging
import os
import random
import time
import tkinter as tk
from functools import wraps
from tkinter import filedialog

import cv2 as cv
import pandas as pd
import win32api
import win32con
import win32gui
from PIL import ImageGrab
from playwright.sync_api import sync_playwright
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def log_info(_text):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info(_text)


def log_error(_text, stack_info: bool = True):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.error(_text, stack_info=stack_info)


class Func:
    def __init__(self, excel):
        self.excel = excel
        self.df = pd.read_excel(self.excel, dtype=str)

    # 写入表格的读表方法
    def init_data(self):
        self.df.dropna(axis=0, how='all', subset=None, inplace=True)
        self.df.dropna(axis=1, how='all', subset=None, inplace=True)
        self.df.fillna("", inplace=True)
        if "结果" not in self.df.columns:
            self.df["结果"] = ""
        for i in self.df.columns:
            self.df[i] = self.df[i].astype(str)
        try:
            self.df.to_excel(self.excel, index=False)
        except Exception as e:
            raise Exception("请关闭表格")

    def check_head(self, data: list):
        head = list(set(data) - set(self.df.columns))
        assert not head, f"{head}表头不存在"


def img_click(img_path, is_double_click: bool = False, max_time: int = 30):
    """
    :param max_time:
    :param img_path:  需要点击的图片保存的位置
    :param is_double_click: False表示单击，True表示双击
    :return:
    """
    # 加载图片和模板
    image = cv.imread(img_path, cv.IMREAD_COLOR)
    _path = f"c:/Users/{os.getlogin()}/.WindowsImg"
    if not os.path.exists(_path):
        try:
            os.makedirs(_path)  # 递归创建目录 因为有些没有用户目录 导致创建报错
        except Exception as e:
            raise Exception(f"当前用户无权限 创建{_path} 请手动创建")
    img_path_name = _path + "/" + str(time.time()).replace(".", "_") + ".png"
    screenshot = ImageGrab.grab()
    screenshot.save(img_path_name)
    matcher_mode = cv.TM_CCOEFF_NORMED
    time.sleep(1)
    template = cv.imread(img_path_name, cv.IMREAD_COLOR)
    all_time = time.time() + max_time
    while time.time() <= all_time:
        try:
            result = cv.matchTemplate(image, template, matcher_mode)
            # 找到最佳匹配位置
            _, max_val, _, max_loc = cv.minMaxLoc(result)
            # 获取匹配区域的坐标
            x, y = max_loc
            w, h, s = template.shape[1], template.shape[0], template.shape[2]  # 宽度在索引1，高度在索引0
            # 打印匹配区域的坐标
            log_info(f"匹配区域坐标：({x}, {y})，宽高：({w}, {h})")
            # 使用PyAutoGUI移动鼠标到匹配区域
            win32api.SetCursorPos((x + 20, y + 20))  # 设置鼠标位置到 (100, 100)
            time.sleep(1)  # 等待1秒钟
            if is_double_click is False:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)  # 鼠标左键按下
                time.sleep(0.1)  # 等待0.1秒
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            else:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)  # 鼠标左键按下
                time.sleep(0.1)  # 等待0.1秒
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)  # 鼠标左键按下
                time.sleep(0.1)  # 等待0.1秒
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            os.remove(img_path_name)
            return True
        except Exception as e:
            if os.path.exists(img_path_name):
                os.remove(img_path_name)
                continue
    raise Exception("寻找图片超时，请检查分辨率或图片地址是否正确！！！")


# 不写入表格的读表方法
def read_excels(excel_path, title_list, one_value):
    """
        适用于写入新表格,返回列表套字典
        excel_path: 读取表格路径
        title_list: 需要核查的表头，需要传入列表
        one_value: 每行数据的唯一值
    """
    lists = []
    df = pd.read_excel(excel_path, dtype="string")
    for title in title_list:
        if title in df.columns:
            continue
        else:
            raise Exception(f"表头缺失：{title}, 请检查excel表头数据！")
    g = df.drop_duplicates(one_value)
    for name in g.index:
        data = df.loc[name].to_dict()
        lists.append(data)
    return lists


# 读取excel并按照表格前的序号进行分组，最终返回[[{}, {}, {}], [{}, {}, {}], [{}., {}, {}]]格式
def read_group_excel(excel_path):
    df = pd.read_excel(excel_path, sheet_name=0, header=0, dtype=str)
    if "收案编号" not in df.columns:
        df["收案编号"] = ""
    if "填写被申请人信息结果" not in df.columns:
        df["填写被申请人信息结果"] = ""
    if "" not in df.columns:
        df["上传结果"] = ""
    for i in df.columns:
        df[i] = df[i].astype(str)
    log_info(df.columns)
    try:
        df.to_excel(excel_path, index=False)
    except Exception as e:
        raise Exception("请关闭表格")
    lists = [[] for i in range(len(df))]
    for index in df.index:
        dict_data = dict(df.iloc[index])
        lists[int(dict_data["序号"]) - 1].append(dict_data)
    filtered_list = [non_empty for non_empty in lists if non_empty]
    return filtered_list


# 写入表格
def wright_excel(result, save_path):
    """
        result: 必须为列表套列表格式  eg: [["案号"，"结果"],[”xxx“， ”成功“],[”xxx“， ”成功“]]
        save_path: 写入excel的地址
    """
    df = pd.DataFrame(result[1:], columns=result[0])
    df.to_excel(save_path, index=False)


# playwright关闭其他页面
def close_other_label(page, context):
    """
    :param page: 页面page
    :param context:
    """
    for i in context.pages:
        if i.title() == page:
            continue
        i.close()
    time.sleep(1)


# selenium关闭其他页面方法
def close_other_labels(driver, label_handle: str or list, switch_to=None):
    """
    :param driver:
    :param label_handle: 需要保留的页面title名称
    :param switch_to:
    """
    if isinstance(label_handle, str):
        label_handle = [label_handle]
    retain_handle = collections.OrderedDict()
    while True:
        handle: list = driver.window_handles
        for i in handle:
            driver.switch_to.window(i)
            if driver.title in label_handle:
                retain_handle[driver.title] = i
                continue
            elif i in label_handle:
                retain_handle[i] = i
                continue
            driver.close()
        if len(retain_handle) == len(label_handle):
            break
    driver.switch_to.window(
        [i for i in retain_handle.values()][0] if not switch_to else retain_handle[switch_to])


# 查找alert弹窗
def alert_win(driver, xpath, wait_time=30):
    log_info(xpath)
    all_time = time.time() + wait_time
    while time.time() <= all_time:
        try:
            return driver.switch_to.alert
        except:
            ...
    raise Exception("operate timeout!!!")


# 双击元素
def double_click(driver, xpath, wait_time=30):
    log_info(xpath)
    el = wait_time_click(driver, xpath, wait_time, style=3)
    ActionChains(driver).double_click(el).perform()


# 滑块仅限于一次滑到头的
def slider_verification(driver, slider_xpath, slider_bar_xpath, acceleration=None):
    """
    :param driver:
    :param slider_xpath: 滑块的xpath
    :param slider_bar_xpath: 滑动条Xpath
    :param acceleration:  速度调节 [min, max] 随机从其中取值 作为速度 默认[500, 800]
    """
    if acceleration is None:
        acceleration = [500, 800]
    acceleration = random.randint(acceleration[0], acceleration[1])

    def get_move_track(gap):
        """用来计算移动速度"""
        # 移动轨迹
        _track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = gap * 4 / 5  # 前4/5段加速 后1/5段减速
        t = 0.2  # 计算间隔
        v = 0  # 初速度
        while current < gap:
            if current < mid:
                a = acceleration
            else:
                a = -acceleration
            v0 = v  # 初速度v0
            v = v0 + a * t  # 当前速度
            move = v0 * t + 1 / 2 * a * t * t  # 移动距离
            current += move  # 当前位移
            _track.append(round(move))  # 加入轨迹
        return _track

    # 滑块的宽
    move_back_width = driver.execute_script("return arguments[0].clientWidth",
                                            driver.find_element(By.XPATH, slider_xpath))
    # 滑条的宽
    slide_bar_width = driver.execute_script("return arguments[0].clientWidth",
                                            driver.find_element(By.XPATH, slider_bar_xpath))
    # 滑条剩余的长度
    slide_length = slide_bar_width - move_back_width
    track = get_move_track(slide_length)
    ActionChains(driver).click_and_hold(
        driver.find_element(By.XPATH, slider_xpath)).perform()
    for x in track:
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
    # 滑动结束后随机停顿
    time.sleep(random.random())
    # 松开鼠标
    ActionChains(driver).release().perform()


# selenium点击方法
def wait_time_click(driver, xpath, wait_time=30, style: int = 1):
    """
    :param driver:
    :param xpath: 不用多说
    :param wait_time: 等待时间
    :param style: 默认为1，查找元素并点击，数值为2数值为按查找元素并等待成功True失败False，数值为3则正常查找并返回当前元素
    :return:
    """

    log_info(xpath)
    all_time = time.time() + wait_time
    if style == 1:
        while time.time() <= all_time:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed() and el.is_enabled():
                    return el.click()
            except:
                ...
        raise Exception("operate timeout")
    elif style == 2:
        while time.time() <= all_time:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed() and el.is_enabled():
                    return True
            except:
                ...
        return False
    else:
        while time.time() <= all_time:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el.is_displayed() and el.is_enabled():
                    return el
            except:
                ...
        raise Exception("元素查找超时！！！")


# selenium清除数据并输入
def clear_and_enter(driver, xpath, text, is_keyboard: bool = False):
    """
    :param driver:
    :param xpath:
    :param text: 需要输入的内容
    :param is_keyboard: 是否使用键盘清除数据
    :return:
    """
    el = wait_time_click(driver, xpath, style=3)
    if is_keyboard is False:
        el.clear()
        time.sleep(0.5)
    else:
        el.send_keys(Keys.CONTROL + 'a')
        time.sleep(0.5)
        el.send_keys(Keys.DELETE)
    el.send_keys(text)


# 切换页面title
def switch_to_title(driver, title, max_size: bool = True, wait_time=15, handle_len: int = 0):
    """
    :param driver:
    :param title: 要切换的title名称
    :param max_size: 是否需要页面最大化
    :param wait_time:
    :param handle_len:
    """
    all_time = time.time()
    while (time.time() - all_time) < wait_time:
        all_handle = driver.window_handles
        if handle_len:
            if len(all_handle) != handle_len:
                continue
        for h in all_handle:
            driver.switch_to.window(h)
            if driver.title == title:
                if max_size:
                    driver.maximize_window()
                return True  # 用来跳出双层循环
    raise Exception(f"Switch to window[{title}] timeout")


# 切入iframe
def cut_in_frame(driver, xpath: list):
    for iframe in xpath:
        wait_time_click(driver, xpath=iframe, style=3)
        driver.switch_to.frame(iframe)
        time.sleep(0.8)


# 判断元素是否消失
def element_not_exist(driver, xpath, wait_time=30):
    all_time = time.time() + wait_time
    while time.time() <= all_time:
        try:
            el = driver.find_element(By.XPATH, xpath)
            if el.is_displayed() and el.is_enabled():
                continue
            else:
                return True
        except:
            ...
    raise Exception("operate timeout")


# 获取所有子元素
def get_elements(driver, xpath, wait_time=30):
    wait_page_load(driver)
    all_time = time.time() + wait_time
    while time.time() <= all_time:
        try:
            el = driver.find_elements(By.XPATH, xpath)
            return el
        except:
            ...
    raise Exception("operate timeout!!!")


# 控制鼠标移动到指定元素
def slide_mouse(driver, xpath, is_click=True):
    """
    :param driver:
    :param xpath:
    :param is_click: 是否需要点击
    """
    target_element = wait_time_click(driver, xpath, style=3)
    actions = ActionChains(driver)
    # 移动鼠标到目标元素
    actions.move_to_element(target_element).perform()
    if is_click:
        actions.click(target_element).perform()
    return


# 使用js使页面下滑到指定元素位置
def slide_xpath(driver, xpath, wait_time=30, direction=False):
    """
    :param direction: True向上滑动，False向下滑动
    """
    all_time = time.time() + wait_time
    while time.time() <= all_time:
        try:
            el = driver.find_element(By.XPATH, xpath)
            if direction is False:
                driver.execute_script(f"arguments[0].scrollIntoView(false);", el)
            else:
                driver.execute_script(f"arguments[0].scrollIntoView(ture);", el)
            return
        except Exception:
            ...
    raise Exception("operate timeout")


# 判断xpath中对应的元素是否存在
def elements_value(driver, xpath, element_key: str, element_value: str, wait_time=30):
    """
    :param element_key: 获取的元素类型（class, id, name ......）
    :param element_value: 需要判断是否存在的内容
    """
    el = wait_time_click(driver, xpath, wait_time, style=3)
    _text = el.get_attribute(element_key)
    if element_value in _text:
        return True
    return False


# 切入上级iframe
def superior_iframe(driver, hierarchy: int):
    """
    :param hierarchy: 切出iframe的层数
    """
    for i in range(hierarchy):
        driver.switch_to.parent_frame()
        time.sleep(0.5)


# 等待页面是否加载完成
def wait_page_load(driver):
    initial_time = time.time()
    while (time.time() - initial_time) < 30:
        if driver.execute_script("return document.readyState") == "complete":
            log_info("完成！")
            return
        log_info("未完成！")
    raise Exception("页面加载超时")


# 控制下载页面执行下载操作selenium版
def chrome_down_path(file_path):
    """
    在谷歌浏览器下，点击下载会弹出下载保存位置的弹窗，不适用移动文件，直接输入要存储的路径，文件就会保存在file_path位置了。
    注意：1.使用之前，谷歌浏览器的下载弹窗要显示出来
         2.如果文件路径已经存在，会又有一个弹窗，这里没做判断，写代码自己判断下文件路径是否存在
    :param file_path: 文件保存位置
    """
    time.sleep(2)
    no1 = win32gui.FindWindow("#32770", "另存为")  # 一级窗口
    button = win32gui.FindWindowEx(no1, 0, "Button", "打开(&O)")
    a1 = win32gui.FindWindowEx(no1, 0, "DUIViewWndClassName", None)
    a2 = win32gui.FindWindowEx(a1, 0, "DirectUIHWND", None)
    a3 = win32gui.FindWindowEx(a2, 0, "FloatNotifySink", None)
    a4 = win32gui.FindWindowEx(a3, 0, "ComboBox", None)
    edit = win32gui.FindWindowEx(a4, None, "Edit", None)
    win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, file_path)
    win32gui.SendMessage(no1, win32con.WM_COMMAND, 1, button)


# 调用js方法
def js_function(driver, xpath, js_fun):
    """
    :param js_fun: 需要的方法
    """
    fun = wait_time_click(driver, xpath, style=3)
    driver.execute_script(js_fun, fun)


# 使用js方法填写数据
def js_input(driver, xpath, value):
    """
    :param value: 要输入的文本
    """
    fun = wait_time_click(driver, xpath, style=3)
    driver.execute_script(f"arguments[0].value='{value}';", fun)


# playwright滑块一次滑到低
def playwright_slider_verification(page, hk_xpath):
    """
    :param page:
    :param hk_xpath: 滑块的xpath
    """
    # 获取滑块的元素句柄
    slider = page.query_selector(hk_xpath)
    # 获取滑块的位置
    slider_box = slider.bounding_box()
    # 如果滑块有固定的移动轨迹，则可能需要计算移动距离
    # 否则，可以直接指定移动的坐标
    move_x = 1000  # 水平移动的距离
    move_y = 0  # 垂直移动的距离，通常为0
    # 模拟拖动滑块
    page.mouse.move(slider_box['x'] + slider_box['width'] / 2, slider_box['y'] + slider_box['height'] / 2)
    page.mouse.down()
    page.mouse.move(slider_box['x'] + slider_box['width'] / 2 + move_x,
                    slider_box['y'] + slider_box['height'] / 2 + move_y)
    page.mouse.up()


# playwright截图并保存
def playwright_screenshot(page, xpath, photo_name, screenshot_is_all=False):
    """
    :param page:
    :param xpath:
    :param photo_name: 保存文件的路径
    :param screenshot_is_all: 是否截取全屏默认按元素截取
    """
    if screenshot_is_all:
        page.screenshot(path=photo_name)
        log_info(f"图片保存在{photo_name}")
        return
    content_element = page.locator(xpath)
    if content_element:
        # 获取元素的边界，以便确定截图区域
        bounding_box = content_element.bounding_box()
        if bounding_box:
            page.screenshot(path=photo_name, clip=bounding_box)
            log_info(f"图片保存在{photo_name}")
            return


# 小重试方法
def unit_testing(f):
    def decorated(*args, **kwargs):
        retry = kwargs.pop('retry') if kwargs.get('retry', None) else 4
        fun = kwargs.pop('fun') if kwargs.get('fun', None) else None
        for i in range(retry):
            try:
                res = f(*args, **kwargs)
                return res
            except Exception as e:
                log_info(e)
                if i >= retry - 1:
                    raise Exception(e)
                if fun is not None:
                    fun()
            log_info(f"异常调试{i + 1}")

    return decorated


# 大重试方法
def big_retry(pre_func, retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    pre_func()
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == retries - 1:
                        raise e
                    time.sleep(delay)
        return wrapper
    return decorator


js = """
    /*!
     * Note: Auto-generated, do not update manually.
     * Generated by: https://github.com/berstend/puppeteer-extra/tree/master/packages/extract-stealth-evasions
     * Generated on: Sat, 28 Nov 2020 07:21:38 GMT
     * License: MIT
     */
    var opts;
    (({_utilsFns: _utilsFns, _mainFunction: _mainFunction, _args: _args}) => {
        const utils = Object.fromEntries(Object.entries(_utilsFns).map((([key, value]) => [key, eval(value)])));
        utils.preloadCache(), eval(_mainFunction)(utils, ..._args)
    })({
        _utilsFns: {
            stripProxyFromErrors: "(handler = {}) => {\n  const newHandler = {}\n  // We wrap each trap in the handler in a try/catch and modify the error stack if they throw\n  const traps = Object.getOwnPropertyNames(handler)\n  traps.forEach(trap => {\n    newHandler[trap] = function() {\n      try {\n        // Forward the call to the defined proxy handler\n        return handler[trap].apply(this, arguments || [])\n      } catch (err) {\n        // Stack traces differ per browser, we only support chromium based ones currently\n        if (!err || !err.stack || !err.stack.includes(`at `)) {\n          throw err\n        }\n\n        // When something throws within one of our traps the Proxy will show up in error stacks\n        // An earlier implementation of this code would simply strip lines with a blacklist,\n        // but it makes sense to be more surgical here and only remove lines related to our Proxy.\n        // We try to use a known \"anchor\" line for that and strip it with everything above it.\n        // If the anchor line cannot be found for some reason we fall back to our blacklist approach.\n\n        const stripWithBlacklist = stack => {\n          const blacklist = [\n            `at Reflect.${trap} `, // e.g. Reflect.get or Reflect.apply\n            `at Object.${trap} `, // e.g. Object.get or Object.apply\n            `at Object.newHandler.<computed> [as ${trap}] ` // caused by this very wrapper :-)\n          ]\n          return (\n            err.stack\n              .split('\\n')\n              // Always remove the first (file) line in the stack (guaranteed to be our proxy)\n              .filter((line, index) => index !== 1)\n              // Check if the line starts with one of our blacklisted strings\n              .filter(line => !blacklist.some(bl => line.trim().startsWith(bl)))\n              .join('\\n')\n          )\n        }\n\n        const stripWithAnchor = stack => {\n          const stackArr = stack.split('\\n')\n          const anchor = `at Object.newHandler.<computed> [as ${trap}] ` // Known first Proxy line in chromium\n          const anchorIndex = stackArr.findIndex(line =>\n            line.trim().startsWith(anchor)\n          )\n          if (anchorIndex === -1) {\n            return false // 404, anchor not found\n          }\n          // Strip everything from the top until we reach the anchor line\n          // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n          stackArr.splice(1, anchorIndex)\n          return stackArr.join('\\n')\n        }\n\n        // Try using the anchor method, fallback to blacklist if necessary\n        err.stack = stripWithAnchor(err.stack) || stripWithBlacklist(err.stack)\n\n        throw err // Re-throw our now sanitized error\n      }\n    }\n  })\n  return newHandler\n}",
            stripErrorWithAnchor: "(err, anchor) => {\n  const stackArr = err.stack.split('\\n')\n  const anchorIndex = stackArr.findIndex(line => line.trim().startsWith(anchor))\n  if (anchorIndex === -1) {\n    return err // 404, anchor not found\n  }\n  // Strip everything from the top until we reach the anchor line (remove anchor line as well)\n  // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n  stackArr.splice(1, anchorIndex)\n  err.stack = stackArr.join('\\n')\n  return err\n}",
            replaceProperty: "(obj, propName, descriptorOverrides = {}) => {\n  return Object.defineProperty(obj, propName, {\n    // Copy over the existing descriptors (writable, enumerable, configurable, etc)\n    ...(Object.getOwnPropertyDescriptor(obj, propName) || {}),\n    // Add our overrides (e.g. value, get())\n    ...descriptorOverrides\n  })\n}",
            preloadCache: "() => {\n  if (utils.cache) {\n    return\n  }\n  utils.cache = {\n    // Used in our proxies\n    Reflect: {\n      get: Reflect.get.bind(Reflect),\n      apply: Reflect.apply.bind(Reflect)\n    },\n    // Used in `makeNativeString`\n    nativeToStringStr: Function.toString + '' // => `function toString() { [native code] }`\n  }\n}",
            makeNativeString: "(name = '') => {\n  // Cache (per-window) the original native toString or use that if available\n  utils.preloadCache()\n  return utils.cache.nativeToStringStr.replace('toString', name || '')\n}",
            patchToString: "(obj, str = '') => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n      // `toString` targeted at our proxied Object detected\n      if (ctx === obj) {\n        // We either return the optional string verbatim or derive the most desired result automatically\n        return str || utils.makeNativeString(obj.name)\n      }\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            patchToStringNested: "(obj = {}) => {\n  return utils.execRecursively(obj, ['function'], utils.patchToString)\n}",
            redirectToString: "(proxyObj, originalObj) => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n\n      // `toString` targeted at our proxied Object detected\n      if (ctx === proxyObj) {\n        const fallback = () =>\n          originalObj && originalObj.name\n            ? utils.makeNativeString(originalObj.name)\n            : utils.makeNativeString(proxyObj.name)\n\n        // Return the toString representation of our original object if possible\n        return originalObj + '' || fallback()\n      }\n\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            replaceWithProxy: "(obj, propName, handler) => {\n  utils.preloadCache()\n  const originalObj = obj[propName]\n  const proxyObj = new Proxy(obj[propName], utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.redirectToString(proxyObj, originalObj)\n\n  return true\n}",
            mockWithProxy: "(obj, propName, pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.patchToString(proxyObj)\n\n  return true\n}",
            createProxy: "(pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n  utils.patchToString(proxyObj)\n\n  return proxyObj\n}",
            splitObjPath: "objPath => ({\n  // Remove last dot entry (property) ==> `HTMLMediaElement.prototype`\n  objName: objPath\n    .split('.')\n    .slice(0, -1)\n    .join('.'),\n  // Extract last dot entry ==> `canPlayType`\n  propName: objPath.split('.').slice(-1)[0]\n})",
            replaceObjPathWithProxy: "(objPath, handler) => {\n  const { objName, propName } = utils.splitObjPath(objPath)\n  const obj = eval(objName) // eslint-disable-line no-eval\n  return utils.replaceWithProxy(obj, propName, handler)\n}",
            execRecursively: "(obj = {}, typeFilter = [], fn) => {\n  function recurse(obj) {\n    for (const key in obj) {\n      if (obj[key] === undefined) {\n        continue\n      }\n      if (obj[key] && typeof obj[key] === 'object') {\n        recurse(obj[key])\n      } else {\n        if (obj[key] && typeFilter.includes(typeof obj[key])) {\n          fn.call(this, obj[key])\n        }\n      }\n    }\n  }\n  recurse(obj)\n  return obj\n}",
            stringifyFns: "(fnObj = { hello: () => 'world' }) => {\n  // Object.fromEntries() ponyfill (in 6 lines) - supported only in Node v12+, modern browsers are fine\n  // https://github.com/feross/fromentries\n  function fromEntries(iterable) {\n    return [...iterable].reduce((obj, [key, val]) => {\n      obj[key] = val\n      return obj\n    }, {})\n  }\n  return (Object.fromEntries || fromEntries)(\n    Object.entries(fnObj)\n      .filter(([key, value]) => typeof value === 'function')\n      .map(([key, value]) => [key, value.toString()]) // eslint-disable-line no-eval\n  )\n}",
            materializeFns: "(fnStrObj = { hello: \"() => 'world'\" }) => {\n  return Object.fromEntries(\n    Object.entries(fnStrObj).map(([key, value]) => {\n      if (value.startsWith('function')) {\n        // some trickery is needed to make oldschool functions work :-)\n        return [key, eval(`() => ${value}`)()] // eslint-disable-line no-eval\n      } else {\n        // arrow functions just work\n        return [key, eval(value)] // eslint-disable-line no-eval\n      }\n    })\n  )\n}"
        },
        _mainFunction: 'utils => {\n      if (!window.chrome) {\n        // Use the exact property descriptor found in headful Chrome\n        // fetch it via `Object.getOwnPropertyDescriptor(window, \'chrome\')`\n        Object.defineProperty(window, \'chrome\', {\n          writable: true,\n          enumerable: true,\n          configurable: false, // note!\n          value: {} // We\'ll extend that later\n        })\n      }\n\n      // That means we\'re running headful and don\'t need to mock anything\n      if (\'app\' in window.chrome) {\n        return // Nothing to do here\n      }\n\n      const makeError = {\n        ErrorInInvocation: fn => {\n          const err = new TypeError(`Error in invocation of app.${fn}()`)\n          return utils.stripErrorWithAnchor(\n            err,\n            `at ${fn} (eval at <anonymous>`\n          )\n        }\n      }\n\n      // There\'s a some static data in that property which doesn\'t seem to change,\n      // we should periodically check for updates: `JSON.stringify(window.app, null, 2)`\n      const STATIC_DATA = JSON.parse(\n        `\n{\n  "isInstalled": false,\n  "InstallState": {\n    "DISABLED": "disabled",\n    "INSTALLED": "installed",\n    "NOT_INSTALLED": "not_installed"\n  },\n  "RunningState": {\n    "CANNOT_RUN": "cannot_run",\n    "READY_TO_RUN": "ready_to_run",\n    "RUNNING": "running"\n  }\n}\n        `.trim()\n      )\n\n      window.chrome.app = {\n        ...STATIC_DATA,\n\n        get isInstalled() {\n          return false\n        },\n\n        getDetails: function getDetails() {\n          if (arguments.length) {\n            throw makeError.ErrorInInvocation(`getDetails`)\n          }\n          return null\n        },\n        getIsInstalled: function getDetails() {\n          if (arguments.length) {\n            throw makeError.ErrorInInvocation(`getIsInstalled`)\n          }\n          return false\n        },\n        runningState: function getDetails() {\n          if (arguments.length) {\n            throw makeError.ErrorInInvocation(`runningState`)\n          }\n          return \'cannot_run\'\n        }\n      }\n      utils.patchToStringNested(window.chrome.app)\n    }',
        _args: []
    }), (({_utilsFns: _utilsFns, _mainFunction: _mainFunction, _args: _args}) => {
        const utils = Object.fromEntries(Object.entries(_utilsFns).map((([key, value]) => [key, eval(value)])));
        utils.preloadCache(), eval(_mainFunction)(utils, ..._args)
    })({
        _utilsFns: {
            stripProxyFromErrors: "(handler = {}) => {\n  const newHandler = {}\n  // We wrap each trap in the handler in a try/catch and modify the error stack if they throw\n  const traps = Object.getOwnPropertyNames(handler)\n  traps.forEach(trap => {\n    newHandler[trap] = function() {\n      try {\n        // Forward the call to the defined proxy handler\n        return handler[trap].apply(this, arguments || [])\n      } catch (err) {\n        // Stack traces differ per browser, we only support chromium based ones currently\n        if (!err || !err.stack || !err.stack.includes(`at `)) {\n          throw err\n        }\n\n        // When something throws within one of our traps the Proxy will show up in error stacks\n        // An earlier implementation of this code would simply strip lines with a blacklist,\n        // but it makes sense to be more surgical here and only remove lines related to our Proxy.\n        // We try to use a known \"anchor\" line for that and strip it with everything above it.\n        // If the anchor line cannot be found for some reason we fall back to our blacklist approach.\n\n        const stripWithBlacklist = stack => {\n          const blacklist = [\n            `at Reflect.${trap} `, // e.g. Reflect.get or Reflect.apply\n            `at Object.${trap} `, // e.g. Object.get or Object.apply\n            `at Object.newHandler.<computed> [as ${trap}] ` // caused by this very wrapper :-)\n          ]\n          return (\n            err.stack\n              .split('\\n')\n              // Always remove the first (file) line in the stack (guaranteed to be our proxy)\n              .filter((line, index) => index !== 1)\n              // Check if the line starts with one of our blacklisted strings\n              .filter(line => !blacklist.some(bl => line.trim().startsWith(bl)))\n              .join('\\n')\n          )\n        }\n\n        const stripWithAnchor = stack => {\n          const stackArr = stack.split('\\n')\n          const anchor = `at Object.newHandler.<computed> [as ${trap}] ` // Known first Proxy line in chromium\n          const anchorIndex = stackArr.findIndex(line =>\n            line.trim().startsWith(anchor)\n          )\n          if (anchorIndex === -1) {\n            return false // 404, anchor not found\n          }\n          // Strip everything from the top until we reach the anchor line\n          // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n          stackArr.splice(1, anchorIndex)\n          return stackArr.join('\\n')\n        }\n\n        // Try using the anchor method, fallback to blacklist if necessary\n        err.stack = stripWithAnchor(err.stack) || stripWithBlacklist(err.stack)\n\n        throw err // Re-throw our now sanitized error\n      }\n    }\n  })\n  return newHandler\n}",
            stripErrorWithAnchor: "(err, anchor) => {\n  const stackArr = err.stack.split('\\n')\n  const anchorIndex = stackArr.findIndex(line => line.trim().startsWith(anchor))\n  if (anchorIndex === -1) {\n    return err // 404, anchor not found\n  }\n  // Strip everything from the top until we reach the anchor line (remove anchor line as well)\n  // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n  stackArr.splice(1, anchorIndex)\n  err.stack = stackArr.join('\\n')\n  return err\n}",
            replaceProperty: "(obj, propName, descriptorOverrides = {}) => {\n  return Object.defineProperty(obj, propName, {\n    // Copy over the existing descriptors (writable, enumerable, configurable, etc)\n    ...(Object.getOwnPropertyDescriptor(obj, propName) || {}),\n    // Add our overrides (e.g. value, get())\n    ...descriptorOverrides\n  })\n}",
            preloadCache: "() => {\n  if (utils.cache) {\n    return\n  }\n  utils.cache = {\n    // Used in our proxies\n    Reflect: {\n      get: Reflect.get.bind(Reflect),\n      apply: Reflect.apply.bind(Reflect)\n    },\n    // Used in `makeNativeString`\n    nativeToStringStr: Function.toString + '' // => `function toString() { [native code] }`\n  }\n}",
            makeNativeString: "(name = '') => {\n  // Cache (per-window) the original native toString or use that if available\n  utils.preloadCache()\n  return utils.cache.nativeToStringStr.replace('toString', name || '')\n}",
            patchToString: "(obj, str = '') => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n      // `toString` targeted at our proxied Object detected\n      if (ctx === obj) {\n        // We either return the optional string verbatim or derive the most desired result automatically\n        return str || utils.makeNativeString(obj.name)\n      }\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            patchToStringNested: "(obj = {}) => {\n  return utils.execRecursively(obj, ['function'], utils.patchToString)\n}",
            redirectToString: "(proxyObj, originalObj) => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n\n      // `toString` targeted at our proxied Object detected\n      if (ctx === proxyObj) {\n        const fallback = () =>\n          originalObj && originalObj.name\n            ? utils.makeNativeString(originalObj.name)\n            : utils.makeNativeString(proxyObj.name)\n\n        // Return the toString representation of our original object if possible\n        return originalObj + '' || fallback()\n      }\n\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            replaceWithProxy: "(obj, propName, handler) => {\n  utils.preloadCache()\n  const originalObj = obj[propName]\n  const proxyObj = new Proxy(obj[propName], utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.redirectToString(proxyObj, originalObj)\n\n  return true\n}",
            mockWithProxy: "(obj, propName, pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.patchToString(proxyObj)\n\n  return true\n}",
            createProxy: "(pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n  utils.patchToString(proxyObj)\n\n  return proxyObj\n}",
            splitObjPath: "objPath => ({\n  // Remove last dot entry (property) ==> `HTMLMediaElement.prototype`\n  objName: objPath\n    .split('.')\n    .slice(0, -1)\n    .join('.'),\n  // Extract last dot entry ==> `canPlayType`\n  propName: objPath.split('.').slice(-1)[0]\n})",
            replaceObjPathWithProxy: "(objPath, handler) => {\n  const { objName, propName } = utils.splitObjPath(objPath)\n  const obj = eval(objName) // eslint-disable-line no-eval\n  return utils.replaceWithProxy(obj, propName, handler)\n}",
            execRecursively: "(obj = {}, typeFilter = [], fn) => {\n  function recurse(obj) {\n    for (const key in obj) {\n      if (obj[key] === undefined) {\n        continue\n      }\n      if (obj[key] && typeof obj[key] === 'object') {\n        recurse(obj[key])\n      } else {\n        if (obj[key] && typeFilter.includes(typeof obj[key])) {\n          fn.call(this, obj[key])\n        }\n      }\n    }\n  }\n  recurse(obj)\n  return obj\n}",
            stringifyFns: "(fnObj = { hello: () => 'world' }) => {\n  // Object.fromEntries() ponyfill (in 6 lines) - supported only in Node v12+, modern browsers are fine\n  // https://github.com/feross/fromentries\n  function fromEntries(iterable) {\n    return [...iterable].reduce((obj, [key, val]) => {\n      obj[key] = val\n      return obj\n    }, {})\n  }\n  return (Object.fromEntries || fromEntries)(\n    Object.entries(fnObj)\n      .filter(([key, value]) => typeof value === 'function')\n      .map(([key, value]) => [key, value.toString()]) // eslint-disable-line no-eval\n  )\n}",
            materializeFns: "(fnStrObj = { hello: \"() => 'world'\" }) => {\n  return Object.fromEntries(\n    Object.entries(fnStrObj).map(([key, value]) => {\n      if (value.startsWith('function')) {\n        // some trickery is needed to make oldschool functions work :-)\n        return [key, eval(`() => ${value}`)()] // eslint-disable-line no-eval\n      } else {\n        // arrow functions just work\n        return [key, eval(value)] // eslint-disable-line no-eval\n      }\n    })\n  )\n}"
        },
        _mainFunction: "utils => {\n      if (!window.chrome) {\n        // Use the exact property descriptor found in headful Chrome\n        // fetch it via `Object.getOwnPropertyDescriptor(window, 'chrome')`\n        Object.defineProperty(window, 'chrome', {\n          writable: true,\n          enumerable: true,\n          configurable: false, // note!\n          value: {} // We'll extend that later\n        })\n      }\n\n      // That means we're running headful and don't need to mock anything\n      if ('csi' in window.chrome) {\n        return // Nothing to do here\n      }\n\n      // Check that the Navigation Timing API v1 is available, we need that\n      if (!window.performance || !window.performance.timing) {\n        return\n      }\n\n      const { timing } = window.performance\n\n      window.chrome.csi = function() {\n        return {\n          onloadT: timing.domContentLoadedEventEnd,\n          startE: timing.navigationStart,\n          pageT: Date.now() - timing.navigationStart,\n          tran: 15 // Transition type or something\n        }\n      }\n      utils.patchToString(window.chrome.csi)\n    }",
        _args: []
    }), (({_utilsFns: _utilsFns, _mainFunction: _mainFunction, _args: _args}) => {
        const utils = Object.fromEntries(Object.entries(_utilsFns).map((([key, value]) => [key, eval(value)])));
        utils.preloadCache(), eval(_mainFunction)(utils, ..._args)
    })({
        _utilsFns: {
            stripProxyFromErrors: "(handler = {}) => {\n  const newHandler = {}\n  // We wrap each trap in the handler in a try/catch and modify the error stack if they throw\n  const traps = Object.getOwnPropertyNames(handler)\n  traps.forEach(trap => {\n    newHandler[trap] = function() {\n      try {\n        // Forward the call to the defined proxy handler\n        return handler[trap].apply(this, arguments || [])\n      } catch (err) {\n        // Stack traces differ per browser, we only support chromium based ones currently\n        if (!err || !err.stack || !err.stack.includes(`at `)) {\n          throw err\n        }\n\n        // When something throws within one of our traps the Proxy will show up in error stacks\n        // An earlier implementation of this code would simply strip lines with a blacklist,\n        // but it makes sense to be more surgical here and only remove lines related to our Proxy.\n        // We try to use a known \"anchor\" line for that and strip it with everything above it.\n        // If the anchor line cannot be found for some reason we fall back to our blacklist approach.\n\n        const stripWithBlacklist = stack => {\n          const blacklist = [\n            `at Reflect.${trap} `, // e.g. Reflect.get or Reflect.apply\n            `at Object.${trap} `, // e.g. Object.get or Object.apply\n            `at Object.newHandler.<computed> [as ${trap}] ` // caused by this very wrapper :-)\n          ]\n          return (\n            err.stack\n              .split('\\n')\n              // Always remove the first (file) line in the stack (guaranteed to be our proxy)\n              .filter((line, index) => index !== 1)\n              // Check if the line starts with one of our blacklisted strings\n              .filter(line => !blacklist.some(bl => line.trim().startsWith(bl)))\n              .join('\\n')\n          )\n        }\n\n        const stripWithAnchor = stack => {\n          const stackArr = stack.split('\\n')\n          const anchor = `at Object.newHandler.<computed> [as ${trap}] ` // Known first Proxy line in chromium\n          const anchorIndex = stackArr.findIndex(line =>\n            line.trim().startsWith(anchor)\n          )\n          if (anchorIndex === -1) {\n            return false // 404, anchor not found\n          }\n          // Strip everything from the top until we reach the anchor line\n          // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n          stackArr.splice(1, anchorIndex)\n          return stackArr.join('\\n')\n        }\n\n        // Try using the anchor method, fallback to blacklist if necessary\n        err.stack = stripWithAnchor(err.stack) || stripWithBlacklist(err.stack)\n\n        throw err // Re-throw our now sanitized error\n      }\n    }\n  })\n  return newHandler\n}",
            stripErrorWithAnchor: "(err, anchor) => {\n  const stackArr = err.stack.split('\\n')\n  const anchorIndex = stackArr.findIndex(line => line.trim().startsWith(anchor))\n  if (anchorIndex === -1) {\n    return err // 404, anchor not found\n  }\n  // Strip everything from the top until we reach the anchor line (remove anchor line as well)\n  // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n  stackArr.splice(1, anchorIndex)\n  err.stack = stackArr.join('\\n')\n  return err\n}",
            replaceProperty: "(obj, propName, descriptorOverrides = {}) => {\n  return Object.defineProperty(obj, propName, {\n    // Copy over the existing descriptors (writable, enumerable, configurable, etc)\n    ...(Object.getOwnPropertyDescriptor(obj, propName) || {}),\n    // Add our overrides (e.g. value, get())\n    ...descriptorOverrides\n  })\n}",
            preloadCache: "() => {\n  if (utils.cache) {\n    return\n  }\n  utils.cache = {\n    // Used in our proxies\n    Reflect: {\n      get: Reflect.get.bind(Reflect),\n      apply: Reflect.apply.bind(Reflect)\n    },\n    // Used in `makeNativeString`\n    nativeToStringStr: Function.toString + '' // => `function toString() { [native code] }`\n  }\n}",
            makeNativeString: "(name = '') => {\n  // Cache (per-window) the original native toString or use that if available\n  utils.preloadCache()\n  return utils.cache.nativeToStringStr.replace('toString', name || '')\n}",
            patchToString: "(obj, str = '') => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n      // `toString` targeted at our proxied Object detected\n      if (ctx === obj) {\n        // We either return the optional string verbatim or derive the most desired result automatically\n        return str || utils.makeNativeString(obj.name)\n      }\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            patchToStringNested: "(obj = {}) => {\n  return utils.execRecursively(obj, ['function'], utils.patchToString)\n}",
            redirectToString: "(proxyObj, originalObj) => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n\n      // `toString` targeted at our proxied Object detected\n      if (ctx === proxyObj) {\n        const fallback = () =>\n          originalObj && originalObj.name\n            ? utils.makeNativeString(originalObj.name)\n            : utils.makeNativeString(proxyObj.name)\n\n        // Return the toString representation of our original object if possible\n        return originalObj + '' || fallback()\n      }\n\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            replaceWithProxy: "(obj, propName, handler) => {\n  utils.preloadCache()\n  const originalObj = obj[propName]\n  const proxyObj = new Proxy(obj[propName], utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.redirectToString(proxyObj, originalObj)\n\n  return true\n}",
            mockWithProxy: "(obj, propName, pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.patchToString(proxyObj)\n\n  return true\n}",
            createProxy: "(pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n  utils.patchToString(proxyObj)\n\n  return proxyObj\n}",
            splitObjPath: "objPath => ({\n  // Remove last dot entry (property) ==> `HTMLMediaElement.prototype`\n  objName: objPath\n    .split('.')\n    .slice(0, -1)\n    .join('.'),\n  // Extract last dot entry ==> `canPlayType`\n  propName: objPath.split('.').slice(-1)[0]\n})",
            replaceObjPathWithProxy: "(objPath, handler) => {\n  const { objName, propName } = utils.splitObjPath(objPath)\n  const obj = eval(objName) // eslint-disable-line no-eval\n  return utils.replaceWithProxy(obj, propName, handler)\n}",
            execRecursively: "(obj = {}, typeFilter = [], fn) => {\n  function recurse(obj) {\n    for (const key in obj) {\n      if (obj[key] === undefined) {\n        continue\n      }\n      if (obj[key] && typeof obj[key] === 'object') {\n        recurse(obj[key])\n      } else {\n        if (obj[key] && typeFilter.includes(typeof obj[key])) {\n          fn.call(this, obj[key])\n        }\n      }\n    }\n  }\n  recurse(obj)\n  return obj\n}",
            stringifyFns: "(fnObj = { hello: () => 'world' }) => {\n  // Object.fromEntries() ponyfill (in 6 lines) - supported only in Node v12+, modern browsers are fine\n  // https://github.com/feross/fromentries\n  function fromEntries(iterable) {\n    return [...iterable].reduce((obj, [key, val]) => {\n      obj[key] = val\n      return obj\n    }, {})\n  }\n  return (Object.fromEntries || fromEntries)(\n    Object.entries(fnObj)\n      .filter(([key, value]) => typeof value === 'function')\n      .map(([key, value]) => [key, value.toString()]) // eslint-disable-line no-eval\n  )\n}",
            materializeFns: "(fnStrObj = { hello: \"() => 'world'\" }) => {\n  return Object.fromEntries(\n    Object.entries(fnStrObj).map(([key, value]) => {\n      if (value.startsWith('function')) {\n        // some trickery is needed to make oldschool functions work :-)\n        return [key, eval(`() => ${value}`)()] // eslint-disable-line no-eval\n      } else {\n        // arrow functions just work\n        return [key, eval(value)] // eslint-disable-line no-eval\n      }\n    })\n  )\n}"
        },
        _mainFunction: "(utils, { opts }) => {\n        if (!window.chrome) {\n          // Use the exact property descriptor found in headful Chrome\n          // fetch it via `Object.getOwnPropertyDescriptor(window, 'chrome')`\n          Object.defineProperty(window, 'chrome', {\n            writable: true,\n            enumerable: true,\n            configurable: false, // note!\n            value: {} // We'll extend that later\n          })\n        }\n\n        // That means we're running headful and don't need to mock anything\n        if ('loadTimes' in window.chrome) {\n          return // Nothing to do here\n        }\n\n        // Check that the Navigation Timing API v1 + v2 is available, we need that\n        if (\n          !window.performance ||\n          !window.performance.timing ||\n          !window.PerformancePaintTiming\n        ) {\n          return\n        }\n\n        const { performance } = window\n\n        // Some stuff is not available on about:blank as it requires a navigation to occur,\n        // let's harden the code to not fail then:\n        const ntEntryFallback = {\n          nextHopProtocol: 'h2',\n          type: 'other'\n        }\n\n        // The API exposes some funky info regarding the connection\n        const protocolInfo = {\n          get connectionInfo() {\n            const ntEntry =\n              performance.getEntriesByType('navigation')[0] || ntEntryFallback\n            return ntEntry.nextHopProtocol\n          },\n          get npnNegotiatedProtocol() {\n            // NPN is deprecated in favor of ALPN, but this implementation returns the\n            // HTTP/2 or HTTP2+QUIC/39 requests negotiated via ALPN.\n            const ntEntry =\n              performance.getEntriesByType('navigation')[0] || ntEntryFallback\n            return ['h2', 'hq'].includes(ntEntry.nextHopProtocol)\n              ? ntEntry.nextHopProtocol\n              : 'unknown'\n          },\n          get navigationType() {\n            const ntEntry =\n              performance.getEntriesByType('navigation')[0] || ntEntryFallback\n            return ntEntry.type\n          },\n          get wasAlternateProtocolAvailable() {\n            // The Alternate-Protocol header is deprecated in favor of Alt-Svc\n            // (https://www.mnot.net/blog/2016/03/09/alt-svc), so technically this\n            // should always return false.\n            return false\n          },\n          get wasFetchedViaSpdy() {\n            // SPDY is deprecated in favor of HTTP/2, but this implementation returns\n            // true for HTTP/2 or HTTP2+QUIC/39 as well.\n            const ntEntry =\n              performance.getEntriesByType('navigation')[0] || ntEntryFallback\n            return ['h2', 'hq'].includes(ntEntry.nextHopProtocol)\n          },\n          get wasNpnNegotiated() {\n            // NPN is deprecated in favor of ALPN, but this implementation returns true\n            // for HTTP/2 or HTTP2+QUIC/39 requests negotiated via ALPN.\n            const ntEntry =\n              performance.getEntriesByType('navigation')[0] || ntEntryFallback\n            return ['h2', 'hq'].includes(ntEntry.nextHopProtocol)\n          }\n        }\n\n        const { timing } = window.performance\n\n        // Truncate number to specific number of decimals, most of the `loadTimes` stuff has 3\n        function toFixed(num, fixed) {\n          var re = new RegExp('^-?\\\\d+(?:.\\\\d{0,' + (fixed || -1) + '})?')\n          return num.toString().match(re)[0]\n        }\n\n        const timingInfo = {\n          get firstPaintAfterLoadTime() {\n            // This was never actually implemented and always returns 0.\n            return 0\n          },\n          get requestTime() {\n            return timing.navigationStart / 1000\n          },\n          get startLoadTime() {\n            return timing.navigationStart / 1000\n          },\n          get commitLoadTime() {\n            return timing.responseStart / 1000\n          },\n          get finishDocumentLoadTime() {\n            return timing.domContentLoadedEventEnd / 1000\n          },\n          get finishLoadTime() {\n            return timing.loadEventEnd / 1000\n          },\n          get firstPaintTime() {\n            const fpEntry = performance.getEntriesByType('paint')[0] || {\n              startTime: timing.loadEventEnd / 1000 // Fallback if no navigation occured (`about:blank`)\n            }\n            return toFixed(\n              (fpEntry.startTime + performance.timeOrigin) / 1000,\n              3\n            )\n          }\n        }\n\n        window.chrome.loadTimes = function() {\n          return {\n            ...protocolInfo,\n            ...timingInfo\n          }\n        }\n        utils.patchToString(window.chrome.loadTimes)\n      }",
        _args: [{opts: {}}]
    }), (({_utilsFns: _utilsFns, _mainFunction: _mainFunction, _args: _args}) => {
        const utils = Object.fromEntries(Object.entries(_utilsFns).map((([key, value]) => [key, eval(value)])));
        utils.preloadCache(), eval(_mainFunction)(utils, ..._args)
    })({
        _utilsFns: {
            stripProxyFromErrors: "(handler = {}) => {\n  const newHandler = {}\n  // We wrap each trap in the handler in a try/catch and modify the error stack if they throw\n  const traps = Object.getOwnPropertyNames(handler)\n  traps.forEach(trap => {\n    newHandler[trap] = function() {\n      try {\n        // Forward the call to the defined proxy handler\n        return handler[trap].apply(this, arguments || [])\n      } catch (err) {\n        // Stack traces differ per browser, we only support chromium based ones currently\n        if (!err || !err.stack || !err.stack.includes(`at `)) {\n          throw err\n        }\n\n        // When something throws within one of our traps the Proxy will show up in error stacks\n        // An earlier implementation of this code would simply strip lines with a blacklist,\n        // but it makes sense to be more surgical here and only remove lines related to our Proxy.\n        // We try to use a known \"anchor\" line for that and strip it with everything above it.\n        // If the anchor line cannot be found for some reason we fall back to our blacklist approach.\n\n        const stripWithBlacklist = stack => {\n          const blacklist = [\n            `at Reflect.${trap} `, // e.g. Reflect.get or Reflect.apply\n            `at Object.${trap} `, // e.g. Object.get or Object.apply\n            `at Object.newHandler.<computed> [as ${trap}] ` // caused by this very wrapper :-)\n          ]\n          return (\n            err.stack\n              .split('\\n')\n              // Always remove the first (file) line in the stack (guaranteed to be our proxy)\n              .filter((line, index) => index !== 1)\n              // Check if the line starts with one of our blacklisted strings\n              .filter(line => !blacklist.some(bl => line.trim().startsWith(bl)))\n              .join('\\n')\n          )\n        }\n\n        const stripWithAnchor = stack => {\n          const stackArr = stack.split('\\n')\n          const anchor = `at Object.newHandler.<computed> [as ${trap}] ` // Known first Proxy line in chromium\n          const anchorIndex = stackArr.findIndex(line =>\n            line.trim().startsWith(anchor)\n          )\n          if (anchorIndex === -1) {\n            return false // 404, anchor not found\n          }\n          // Strip everything from the top until we reach the anchor line\n          // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n          stackArr.splice(1, anchorIndex)\n          return stackArr.join('\\n')\n        }\n\n        // Try using the anchor method, fallback to blacklist if necessary\n        err.stack = stripWithAnchor(err.stack) || stripWithBlacklist(err.stack)\n\n        throw err // Re-throw our now sanitized error\n      }\n    }\n  })\n  return newHandler\n}",
            stripErrorWithAnchor: "(err, anchor) => {\n  const stackArr = err.stack.split('\\n')\n  const anchorIndex = stackArr.findIndex(line => line.trim().startsWith(anchor))\n  if (anchorIndex === -1) {\n    return err // 404, anchor not found\n  }\n  // Strip everything from the top until we reach the anchor line (remove anchor line as well)\n  // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n  stackArr.splice(1, anchorIndex)\n  err.stack = stackArr.join('\\n')\n  return err\n}",
            replaceProperty: "(obj, propName, descriptorOverrides = {}) => {\n  return Object.defineProperty(obj, propName, {\n    // Copy over the existing descriptors (writable, enumerable, configurable, etc)\n    ...(Object.getOwnPropertyDescriptor(obj, propName) || {}),\n    // Add our overrides (e.g. value, get())\n    ...descriptorOverrides\n  })\n}",
            preloadCache: "() => {\n  if (utils.cache) {\n    return\n  }\n  utils.cache = {\n    // Used in our proxies\n    Reflect: {\n      get: Reflect.get.bind(Reflect),\n      apply: Reflect.apply.bind(Reflect)\n    },\n    // Used in `makeNativeString`\n    nativeToStringStr: Function.toString + '' // => `function toString() { [native code] }`\n  }\n}",
            makeNativeString: "(name = '') => {\n  // Cache (per-window) the original native toString or use that if available\n  utils.preloadCache()\n  return utils.cache.nativeToStringStr.replace('toString', name || '')\n}",
            patchToString: "(obj, str = '') => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n      // `toString` targeted at our proxied Object detected\n      if (ctx === obj) {\n        // We either return the optional string verbatim or derive the most desired result automatically\n        return str || utils.makeNativeString(obj.name)\n      }\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            patchToStringNested: "(obj = {}) => {\n  return utils.execRecursively(obj, ['function'], utils.patchToString)\n}",
            redirectToString: "(proxyObj, originalObj) => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n\n      // `toString` targeted at our proxied Object detected\n      if (ctx === proxyObj) {\n        const fallback = () =>\n          originalObj && originalObj.name\n            ? utils.makeNativeString(originalObj.name)\n            : utils.makeNativeString(proxyObj.name)\n\n        // Return the toString representation of our original object if possible\n        return originalObj + '' || fallback()\n      }\n\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            replaceWithProxy: "(obj, propName, handler) => {\n  utils.preloadCache()\n  const originalObj = obj[propName]\n  const proxyObj = new Proxy(obj[propName], utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.redirectToString(proxyObj, originalObj)\n\n  return true\n}",
            mockWithProxy: "(obj, propName, pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.patchToString(proxyObj)\n\n  return true\n}",
            createProxy: "(pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n  utils.patchToString(proxyObj)\n\n  return proxyObj\n}",
            splitObjPath: "objPath => ({\n  // Remove last dot entry (property) ==> `HTMLMediaElement.prototype`\n  objName: objPath\n    .split('.')\n    .slice(0, -1)\n    .join('.'),\n  // Extract last dot entry ==> `canPlayType`\n  propName: objPath.split('.').slice(-1)[0]\n})",
            replaceObjPathWithProxy: "(objPath, handler) => {\n  const { objName, propName } = utils.splitObjPath(objPath)\n  const obj = eval(objName) // eslint-disable-line no-eval\n  return utils.replaceWithProxy(obj, propName, handler)\n}",
            execRecursively: "(obj = {}, typeFilter = [], fn) => {\n  function recurse(obj) {\n    for (const key in obj) {\n      if (obj[key] === undefined) {\n        continue\n      }\n      if (obj[key] && typeof obj[key] === 'object') {\n        recurse(obj[key])\n      } else {\n        if (obj[key] && typeFilter.includes(typeof obj[key])) {\n          fn.call(this, obj[key])\n        }\n      }\n    }\n  }\n  recurse(obj)\n  return obj\n}",
            stringifyFns: "(fnObj = { hello: () => 'world' }) => {\n  // Object.fromEntries() ponyfill (in 6 lines) - supported only in Node v12+, modern browsers are fine\n  // https://github.com/feross/fromentries\n  function fromEntries(iterable) {\n    return [...iterable].reduce((obj, [key, val]) => {\n      obj[key] = val\n      return obj\n    }, {})\n  }\n  return (Object.fromEntries || fromEntries)(\n    Object.entries(fnObj)\n      .filter(([key, value]) => typeof value === 'function')\n      .map(([key, value]) => [key, value.toString()]) // eslint-disable-line no-eval\n  )\n}",
            materializeFns: "(fnStrObj = { hello: \"() => 'world'\" }) => {\n  return Object.fromEntries(\n    Object.entries(fnStrObj).map(([key, value]) => {\n      if (value.startsWith('function')) {\n        // some trickery is needed to make oldschool functions work :-)\n        return [key, eval(`() => ${value}`)()] // eslint-disable-line no-eval\n      } else {\n        // arrow functions just work\n        return [key, eval(value)] // eslint-disable-line no-eval\n      }\n    })\n  )\n}"
        },
        _mainFunction: "(utils, { opts, STATIC_DATA }) => {\n        if (!window.chrome) {\n          // Use the exact property descriptor found in headful Chrome\n          // fetch it via `Object.getOwnPropertyDescriptor(window, 'chrome')`\n          Object.defineProperty(window, 'chrome', {\n            writable: true,\n            enumerable: true,\n            configurable: false, // note!\n            value: {} // We'll extend that later\n          })\n        }\n\n        // That means we're running headful and don't need to mock anything\n        const existsAlready = 'runtime' in window.chrome\n        // `chrome.runtime` is only exposed on secure origins\n        const isNotSecure = !window.location.protocol.startsWith('https')\n        if (existsAlready || (isNotSecure && !opts.runOnInsecureOrigins)) {\n          return // Nothing to do here\n        }\n\n        window.chrome.runtime = {\n          // There's a bunch of static data in that property which doesn't seem to change,\n          // we should periodically check for updates: `JSON.stringify(window.chrome.runtime, null, 2)`\n          ...STATIC_DATA,\n          // `chrome.runtime.id` is extension related and returns undefined in Chrome\n          get id() {\n            return undefined\n          },\n          // These two require more sophisticated mocks\n          connect: null,\n          sendMessage: null\n        }\n\n        const makeCustomRuntimeErrors = (preamble, method, extensionId) => ({\n          NoMatchingSignature: new TypeError(\n            preamble + `No matching signature.`\n          ),\n          MustSpecifyExtensionID: new TypeError(\n            preamble +\n              `${method} called from a webpage must specify an Extension ID (string) for its first argument.`\n          ),\n          InvalidExtensionID: new TypeError(\n            preamble + `Invalid extension id: '${extensionId}'`\n          )\n        })\n\n        // Valid Extension IDs are 32 characters in length and use the letter `a` to `p`:\n        // https://source.chromium.org/chromium/chromium/src/+/master:components/crx_file/id_util.cc;drc=14a055ccb17e8c8d5d437fe080faba4c6f07beac;l=90\n        const isValidExtensionID = str =>\n          str.length === 32 && str.toLowerCase().match(/^[a-p]+$/)\n\n        /** Mock `chrome.runtime.sendMessage` */\n        const sendMessageHandler = {\n          apply: function(target, ctx, args) {\n            const [extensionId, options, responseCallback] = args || []\n\n            // Define custom errors\n            const errorPreamble = `Error in invocation of runtime.sendMessage(optional string extensionId, any message, optional object options, optional function responseCallback): `\n            const Errors = makeCustomRuntimeErrors(\n              errorPreamble,\n              `chrome.runtime.sendMessage()`,\n              extensionId\n            )\n\n            // Check if the call signature looks ok\n            const noArguments = args.length === 0\n            const tooManyArguments = args.length > 4\n            const incorrectOptions = options && typeof options !== 'object'\n            const incorrectResponseCallback =\n              responseCallback && typeof responseCallback !== 'function'\n            if (\n              noArguments ||\n              tooManyArguments ||\n              incorrectOptions ||\n              incorrectResponseCallback\n            ) {\n              throw Errors.NoMatchingSignature\n            }\n\n            // At least 2 arguments are required before we even validate the extension ID\n            if (args.length < 2) {\n              throw Errors.MustSpecifyExtensionID\n            }\n\n            // Now let's make sure we got a string as extension ID\n            if (typeof extensionId !== 'string') {\n              throw Errors.NoMatchingSignature\n            }\n\n            if (!isValidExtensionID(extensionId)) {\n              throw Errors.InvalidExtensionID\n            }\n\n            return undefined // Normal behavior\n          }\n        }\n        utils.mockWithProxy(\n          window.chrome.runtime,\n          'sendMessage',\n          function sendMessage() {},\n          sendMessageHandler\n        )\n\n        /**\n         * Mock `chrome.runtime.connect`\n         *\n         * @see https://developer.chrome.com/apps/runtime#method-connect\n         */\n        const connectHandler = {\n          apply: function(target, ctx, args) {\n            const [extensionId, connectInfo] = args || []\n\n            // Define custom errors\n            const errorPreamble = `Error in invocation of runtime.connect(optional string extensionId, optional object connectInfo): `\n            const Errors = makeCustomRuntimeErrors(\n              errorPreamble,\n              `chrome.runtime.connect()`,\n              extensionId\n            )\n\n            // Behavior differs a bit from sendMessage:\n            const noArguments = args.length === 0\n            const emptyStringArgument = args.length === 1 && extensionId === ''\n            if (noArguments || emptyStringArgument) {\n              throw Errors.MustSpecifyExtensionID\n            }\n\n            const tooManyArguments = args.length > 2\n            const incorrectConnectInfoType =\n              connectInfo && typeof connectInfo !== 'object'\n\n            if (tooManyArguments || incorrectConnectInfoType) {\n              throw Errors.NoMatchingSignature\n            }\n\n            const extensionIdIsString = typeof extensionId === 'string'\n            if (extensionIdIsString && extensionId === '') {\n              throw Errors.MustSpecifyExtensionID\n            }\n            if (extensionIdIsString && !isValidExtensionID(extensionId)) {\n              throw Errors.InvalidExtensionID\n            }\n\n            // There's another edge-case here: extensionId is optional so we might find a connectInfo object as first param, which we need to validate\n            const validateConnectInfo = ci => {\n              // More than a first param connectInfo as been provided\n              if (args.length > 1) {\n                throw Errors.NoMatchingSignature\n              }\n              // An empty connectInfo has been provided\n              if (Object.keys(ci).length === 0) {\n                throw Errors.MustSpecifyExtensionID\n              }\n              // Loop over all connectInfo props an check them\n              Object.entries(ci).forEach(([k, v]) => {\n                const isExpected = ['name', 'includeTlsChannelId'].includes(k)\n                if (!isExpected) {\n                  throw new TypeError(\n                    errorPreamble + `Unexpected property: '${k}'.`\n                  )\n                }\n                const MismatchError = (propName, expected, found) =>\n                  TypeError(\n                    errorPreamble +\n                      `Error at property '${propName}': Invalid type: expected ${expected}, found ${found}.`\n                  )\n                if (k === 'name' && typeof v !== 'string') {\n                  throw MismatchError(k, 'string', typeof v)\n                }\n                if (k === 'includeTlsChannelId' && typeof v !== 'boolean') {\n                  throw MismatchError(k, 'boolean', typeof v)\n                }\n              })\n            }\n            if (typeof extensionId === 'object') {\n              validateConnectInfo(extensionId)\n              throw Errors.MustSpecifyExtensionID\n            }\n\n            // Unfortunately even when the connect fails Chrome will return an object with methods we need to mock as well\n            return utils.patchToStringNested(makeConnectResponse())\n          }\n        }\n        utils.mockWithProxy(\n          window.chrome.runtime,\n          'connect',\n          function connect() {},\n          connectHandler\n        )\n\n        function makeConnectResponse() {\n          const onSomething = () => ({\n            addListener: function addListener() {},\n            dispatch: function dispatch() {},\n            hasListener: function hasListener() {},\n            hasListeners: function hasListeners() {\n              return false\n            },\n            removeListener: function removeListener() {}\n          })\n\n          const response = {\n            name: '',\n            sender: undefined,\n            disconnect: function disconnect() {},\n            onDisconnect: onSomething(),\n            onMessage: onSomething(),\n            postMessage: function postMessage() {\n              if (!arguments.length) {\n                throw new TypeError(`Insufficient number of arguments.`)\n              }\n              throw new Error(`Attempting to use a disconnected port object`)\n            }\n          }\n          return response\n        }\n      }",
        _args: [{
            opts: {runOnInsecureOrigins: !1},
            STATIC_DATA: {
                OnInstalledReason: {
                    CHROME_UPDATE: "chrome_update",
                    INSTALL: "install",
                    SHARED_MODULE_UPDATE: "shared_module_update",
                    UPDATE: "update"
                },
                OnRestartRequiredReason: {APP_UPDATE: "app_update", OS_UPDATE: "os_update", PERIODIC: "periodic"},
                PlatformArch: {
                    ARM: "arm",
                    ARM64: "arm64",
                    MIPS: "mips",
                    MIPS64: "mips64",
                    X86_32: "x86-32",
                    X86_64: "x86-64"
                },
                PlatformNaclArch: {ARM: "arm", MIPS: "mips", MIPS64: "mips64", X86_32: "x86-32", X86_64: "x86-64"},
                PlatformOs: {ANDROID: "android", CROS: "cros", LINUX: "linux", MAC: "mac", OPENBSD: "openbsd", WIN: "win"},
                RequestUpdateCheckStatus: {
                    NO_UPDATE: "no_update",
                    THROTTLED: "throttled",
                    UPDATE_AVAILABLE: "update_available"
                }
            }
        }]
    }), (({_utilsFns: _utilsFns, _mainFunction: _mainFunction, _args: _args}) => {
        const utils = Object.fromEntries(Object.entries(_utilsFns).map((([key, value]) => [key, eval(value)])));
        utils.preloadCache(), eval(_mainFunction)(utils, ..._args)
    })({
        _utilsFns: {
            stripProxyFromErrors: "(handler = {}) => {\n  const newHandler = {}\n  // We wrap each trap in the handler in a try/catch and modify the error stack if they throw\n  const traps = Object.getOwnPropertyNames(handler)\n  traps.forEach(trap => {\n    newHandler[trap] = function() {\n      try {\n        // Forward the call to the defined proxy handler\n        return handler[trap].apply(this, arguments || [])\n      } catch (err) {\n        // Stack traces differ per browser, we only support chromium based ones currently\n        if (!err || !err.stack || !err.stack.includes(`at `)) {\n          throw err\n        }\n\n        // When something throws within one of our traps the Proxy will show up in error stacks\n        // An earlier implementation of this code would simply strip lines with a blacklist,\n        // but it makes sense to be more surgical here and only remove lines related to our Proxy.\n        // We try to use a known \"anchor\" line for that and strip it with everything above it.\n        // If the anchor line cannot be found for some reason we fall back to our blacklist approach.\n\n        const stripWithBlacklist = stack => {\n          const blacklist = [\n            `at Reflect.${trap} `, // e.g. Reflect.get or Reflect.apply\n            `at Object.${trap} `, // e.g. Object.get or Object.apply\n            `at Object.newHandler.<computed> [as ${trap}] ` // caused by this very wrapper :-)\n          ]\n          return (\n            err.stack\n              .split('\\n')\n              // Always remove the first (file) line in the stack (guaranteed to be our proxy)\n              .filter((line, index) => index !== 1)\n              // Check if the line starts with one of our blacklisted strings\n              .filter(line => !blacklist.some(bl => line.trim().startsWith(bl)))\n              .join('\\n')\n          )\n        }\n\n        const stripWithAnchor = stack => {\n          const stackArr = stack.split('\\n')\n          const anchor = `at Object.newHandler.<computed> [as ${trap}] ` // Known first Proxy line in chromium\n          const anchorIndex = stackArr.findIndex(line =>\n            line.trim().startsWith(anchor)\n          )\n          if (anchorIndex === -1) {\n            return false // 404, anchor not found\n          }\n          // Strip everything from the top until we reach the anchor line\n          // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n          stackArr.splice(1, anchorIndex)\n          return stackArr.join('\\n')\n        }\n\n        // Try using the anchor method, fallback to blacklist if necessary\n        err.stack = stripWithAnchor(err.stack) || stripWithBlacklist(err.stack)\n\n        throw err // Re-throw our now sanitized error\n      }\n    }\n  })\n  return newHandler\n}",
            stripErrorWithAnchor: "(err, anchor) => {\n  const stackArr = err.stack.split('\\n')\n  const anchorIndex = stackArr.findIndex(line => line.trim().startsWith(anchor))\n  if (anchorIndex === -1) {\n    return err // 404, anchor not found\n  }\n  // Strip everything from the top until we reach the anchor line (remove anchor line as well)\n  // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n  stackArr.splice(1, anchorIndex)\n  err.stack = stackArr.join('\\n')\n  return err\n}",
            replaceProperty: "(obj, propName, descriptorOverrides = {}) => {\n  return Object.defineProperty(obj, propName, {\n    // Copy over the existing descriptors (writable, enumerable, configurable, etc)\n    ...(Object.getOwnPropertyDescriptor(obj, propName) || {}),\n    // Add our overrides (e.g. value, get())\n    ...descriptorOverrides\n  })\n}",
            preloadCache: "() => {\n  if (utils.cache) {\n    return\n  }\n  utils.cache = {\n    // Used in our proxies\n    Reflect: {\n      get: Reflect.get.bind(Reflect),\n      apply: Reflect.apply.bind(Reflect)\n    },\n    // Used in `makeNativeString`\n    nativeToStringStr: Function.toString + '' // => `function toString() { [native code] }`\n  }\n}",
            makeNativeString: "(name = '') => {\n  // Cache (per-window) the original native toString or use that if available\n  utils.preloadCache()\n  return utils.cache.nativeToStringStr.replace('toString', name || '')\n}",
            patchToString: "(obj, str = '') => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n      // `toString` targeted at our proxied Object detected\n      if (ctx === obj) {\n        // We either return the optional string verbatim or derive the most desired result automatically\n        return str || utils.makeNativeString(obj.name)\n      }\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            patchToStringNested: "(obj = {}) => {\n  return utils.execRecursively(obj, ['function'], utils.patchToString)\n}",
            redirectToString: "(proxyObj, originalObj) => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n\n      // `toString` targeted at our proxied Object detected\n      if (ctx === proxyObj) {\n        const fallback = () =>\n          originalObj && originalObj.name\n            ? utils.makeNativeString(originalObj.name)\n            : utils.makeNativeString(proxyObj.name)\n\n        // Return the toString representation of our original object if possible\n        return originalObj + '' || fallback()\n      }\n\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            replaceWithProxy: "(obj, propName, handler) => {\n  utils.preloadCache()\n  const originalObj = obj[propName]\n  const proxyObj = new Proxy(obj[propName], utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.redirectToString(proxyObj, originalObj)\n\n  return true\n}",
            mockWithProxy: "(obj, propName, pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.patchToString(proxyObj)\n\n  return true\n}",
            createProxy: "(pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n  utils.patchToString(proxyObj)\n\n  return proxyObj\n}",
            splitObjPath: "objPath => ({\n  // Remove last dot entry (property) ==> `HTMLMediaElement.prototype`\n  objName: objPath\n    .split('.')\n    .slice(0, -1)\n    .join('.'),\n  // Extract last dot entry ==> `canPlayType`\n  propName: objPath.split('.').slice(-1)[0]\n})",
            replaceObjPathWithProxy: "(objPath, handler) => {\n  const { objName, propName } = utils.splitObjPath(objPath)\n  const obj = eval(objName) // eslint-disable-line no-eval\n  return utils.replaceWithProxy(obj, propName, handler)\n}",
            execRecursively: "(obj = {}, typeFilter = [], fn) => {\n  function recurse(obj) {\n    for (const key in obj) {\n      if (obj[key] === undefined) {\n        continue\n      }\n      if (obj[key] && typeof obj[key] === 'object') {\n        recurse(obj[key])\n      } else {\n        if (obj[key] && typeFilter.includes(typeof obj[key])) {\n          fn.call(this, obj[key])\n        }\n      }\n    }\n  }\n  recurse(obj)\n  return obj\n}",
            stringifyFns: "(fnObj = { hello: () => 'world' }) => {\n  // Object.fromEntries() ponyfill (in 6 lines) - supported only in Node v12+, modern browsers are fine\n  // https://github.com/feross/fromentries\n  function fromEntries(iterable) {\n    return [...iterable].reduce((obj, [key, val]) => {\n      obj[key] = val\n      return obj\n    }, {})\n  }\n  return (Object.fromEntries || fromEntries)(\n    Object.entries(fnObj)\n      .filter(([key, value]) => typeof value === 'function')\n      .map(([key, value]) => [key, value.toString()]) // eslint-disable-line no-eval\n  )\n}",
            materializeFns: "(fnStrObj = { hello: \"() => 'world'\" }) => {\n  return Object.fromEntries(\n    Object.entries(fnStrObj).map(([key, value]) => {\n      if (value.startsWith('function')) {\n        // some trickery is needed to make oldschool functions work :-)\n        return [key, eval(`() => ${value}`)()] // eslint-disable-line no-eval\n      } else {\n        // arrow functions just work\n        return [key, eval(value)] // eslint-disable-line no-eval\n      }\n    })\n  )\n}"
        },
        _mainFunction: "utils => {\n      /**\n       * Input might look funky, we need to normalize it so e.g. whitespace isn't an issue for our spoofing.\n       *\n       * @example\n       * video/webm; codecs=\"vp8, vorbis\"\n       * video/mp4; codecs=\"avc1.42E01E\"\n       * audio/x-m4a;\n       * audio/ogg; codecs=\"vorbis\"\n       * @param {String} arg\n       */\n      const parseInput = arg => {\n        const [mime, codecStr] = arg.trim().split(';')\n        let codecs = []\n        if (codecStr && codecStr.includes('codecs=\"')) {\n          codecs = codecStr\n            .trim()\n            .replace(`codecs=\"`, '')\n            .replace(`\"`, '')\n            .trim()\n            .split(',')\n            .filter(x => !!x)\n            .map(x => x.trim())\n        }\n        return {\n          mime,\n          codecStr,\n          codecs\n        }\n      }\n\n      const canPlayType = {\n        // Intercept certain requests\n        apply: function(target, ctx, args) {\n          if (!args || !args.length) {\n            return target.apply(ctx, args)\n          }\n          const { mime, codecs } = parseInput(args[0])\n          // This specific mp4 codec is missing in Chromium\n          if (mime === 'video/mp4') {\n            if (codecs.includes('avc1.42E01E')) {\n              return 'probably'\n            }\n          }\n          // This mimetype is only supported if no codecs are specified\n          if (mime === 'audio/x-m4a' && !codecs.length) {\n            return 'maybe'\n          }\n\n          // This mimetype is only supported if no codecs are specified\n          if (mime === 'audio/aac' && !codecs.length) {\n            return 'probably'\n          }\n          // Everything else as usual\n          return target.apply(ctx, args)\n        }\n      }\n\n      /* global HTMLMediaElement */\n      utils.replaceWithProxy(\n        HTMLMediaElement.prototype,\n        'canPlayType',\n        canPlayType\n      )\n    }",
        _args: []
    }), (({_utilsFns: _utilsFns, _mainFunction: _mainFunction, _args: _args}) => {
        const utils = Object.fromEntries(Object.entries(_utilsFns).map((([key, value]) => [key, eval(value)])));
        utils.preloadCache(), eval(_mainFunction)(utils, ..._args)
    })({
        _utilsFns: {
            stripProxyFromErrors: "(handler = {}) => {\n  const newHandler = {}\n  // We wrap each trap in the handler in a try/catch and modify the error stack if they throw\n  const traps = Object.getOwnPropertyNames(handler)\n  traps.forEach(trap => {\n    newHandler[trap] = function() {\n      try {\n        // Forward the call to the defined proxy handler\n        return handler[trap].apply(this, arguments || [])\n      } catch (err) {\n        // Stack traces differ per browser, we only support chromium based ones currently\n        if (!err || !err.stack || !err.stack.includes(`at `)) {\n          throw err\n        }\n\n        // When something throws within one of our traps the Proxy will show up in error stacks\n        // An earlier implementation of this code would simply strip lines with a blacklist,\n        // but it makes sense to be more surgical here and only remove lines related to our Proxy.\n        // We try to use a known \"anchor\" line for that and strip it with everything above it.\n        // If the anchor line cannot be found for some reason we fall back to our blacklist approach.\n\n        const stripWithBlacklist = stack => {\n          const blacklist = [\n            `at Reflect.${trap} `, // e.g. Reflect.get or Reflect.apply\n            `at Object.${trap} `, // e.g. Object.get or Object.apply\n            `at Object.newHandler.<computed> [as ${trap}] ` // caused by this very wrapper :-)\n          ]\n          return (\n            err.stack\n              .split('\\n')\n              // Always remove the first (file) line in the stack (guaranteed to be our proxy)\n              .filter((line, index) => index !== 1)\n              // Check if the line starts with one of our blacklisted strings\n              .filter(line => !blacklist.some(bl => line.trim().startsWith(bl)))\n              .join('\\n')\n          )\n        }\n\n        const stripWithAnchor = stack => {\n          const stackArr = stack.split('\\n')\n          const anchor = `at Object.newHandler.<computed> [as ${trap}] ` // Known first Proxy line in chromium\n          const anchorIndex = stackArr.findIndex(line =>\n            line.trim().startsWith(anchor)\n          )\n          if (anchorIndex === -1) {\n            return false // 404, anchor not found\n          }\n          // Strip everything from the top until we reach the anchor line\n          // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n          stackArr.splice(1, anchorIndex)\n          return stackArr.join('\\n')\n        }\n\n        // Try using the anchor method, fallback to blacklist if necessary\n        err.stack = stripWithAnchor(err.stack) || stripWithBlacklist(err.stack)\n\n        throw err // Re-throw our now sanitized error\n      }\n    }\n  })\n  return newHandler\n}",
            stripErrorWithAnchor: "(err, anchor) => {\n  const stackArr = err.stack.split('\\n')\n  const anchorIndex = stackArr.findIndex(line => line.trim().startsWith(anchor))\n  if (anchorIndex === -1) {\n    return err // 404, anchor not found\n  }\n  // Strip everything from the top until we reach the anchor line (remove anchor line as well)\n  // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n  stackArr.splice(1, anchorIndex)\n  err.stack = stackArr.join('\\n')\n  return err\n}",
            replaceProperty: "(obj, propName, descriptorOverrides = {}) => {\n  return Object.defineProperty(obj, propName, {\n    // Copy over the existing descriptors (writable, enumerable, configurable, etc)\n    ...(Object.getOwnPropertyDescriptor(obj, propName) || {}),\n    // Add our overrides (e.g. value, get())\n    ...descriptorOverrides\n  })\n}",
            preloadCache: "() => {\n  if (utils.cache) {\n    return\n  }\n  utils.cache = {\n    // Used in our proxies\n    Reflect: {\n      get: Reflect.get.bind(Reflect),\n      apply: Reflect.apply.bind(Reflect)\n    },\n    // Used in `makeNativeString`\n    nativeToStringStr: Function.toString + '' // => `function toString() { [native code] }`\n  }\n}",
            makeNativeString: "(name = '') => {\n  // Cache (per-window) the original native toString or use that if available\n  utils.preloadCache()\n  return utils.cache.nativeToStringStr.replace('toString', name || '')\n}",
            patchToString: "(obj, str = '') => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n      // `toString` targeted at our proxied Object detected\n      if (ctx === obj) {\n        // We either return the optional string verbatim or derive the most desired result automatically\n        return str || utils.makeNativeString(obj.name)\n      }\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            patchToStringNested: "(obj = {}) => {\n  return utils.execRecursively(obj, ['function'], utils.patchToString)\n}",
            redirectToString: "(proxyObj, originalObj) => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n\n      // `toString` targeted at our proxied Object detected\n      if (ctx === proxyObj) {\n        const fallback = () =>\n          originalObj && originalObj.name\n            ? utils.makeNativeString(originalObj.name)\n            : utils.makeNativeString(proxyObj.name)\n\n        // Return the toString representation of our original object if possible\n        return originalObj + '' || fallback()\n      }\n\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            replaceWithProxy: "(obj, propName, handler) => {\n  utils.preloadCache()\n  const originalObj = obj[propName]\n  const proxyObj = new Proxy(obj[propName], utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.redirectToString(proxyObj, originalObj)\n\n  return true\n}",
            mockWithProxy: "(obj, propName, pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.patchToString(proxyObj)\n\n  return true\n}",
            createProxy: "(pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n  utils.patchToString(proxyObj)\n\n  return proxyObj\n}",
            splitObjPath: "objPath => ({\n  // Remove last dot entry (property) ==> `HTMLMediaElement.prototype`\n  objName: objPath\n    .split('.')\n    .slice(0, -1)\n    .join('.'),\n  // Extract last dot entry ==> `canPlayType`\n  propName: objPath.split('.').slice(-1)[0]\n})",
            replaceObjPathWithProxy: "(objPath, handler) => {\n  const { objName, propName } = utils.splitObjPath(objPath)\n  const obj = eval(objName) // eslint-disable-line no-eval\n  return utils.replaceWithProxy(obj, propName, handler)\n}",
            execRecursively: "(obj = {}, typeFilter = [], fn) => {\n  function recurse(obj) {\n    for (const key in obj) {\n      if (obj[key] === undefined) {\n        continue\n      }\n      if (obj[key] && typeof obj[key] === 'object') {\n        recurse(obj[key])\n      } else {\n        if (obj[key] && typeFilter.includes(typeof obj[key])) {\n          fn.call(this, obj[key])\n        }\n      }\n    }\n  }\n  recurse(obj)\n  return obj\n}",
            stringifyFns: "(fnObj = { hello: () => 'world' }) => {\n  // Object.fromEntries() ponyfill (in 6 lines) - supported only in Node v12+, modern browsers are fine\n  // https://github.com/feross/fromentries\n  function fromEntries(iterable) {\n    return [...iterable].reduce((obj, [key, val]) => {\n      obj[key] = val\n      return obj\n    }, {})\n  }\n  return (Object.fromEntries || fromEntries)(\n    Object.entries(fnObj)\n      .filter(([key, value]) => typeof value === 'function')\n      .map(([key, value]) => [key, value.toString()]) // eslint-disable-line no-eval\n  )\n}",
            materializeFns: "(fnStrObj = { hello: \"() => 'world'\" }) => {\n  return Object.fromEntries(\n    Object.entries(fnStrObj).map(([key, value]) => {\n      if (value.startsWith('function')) {\n        // some trickery is needed to make oldschool functions work :-)\n        return [key, eval(`() => ${value}`)()] // eslint-disable-line no-eval\n      } else {\n        // arrow functions just work\n        return [key, eval(value)] // eslint-disable-line no-eval\n      }\n    })\n  )\n}"
        },
        _mainFunction: "(utils, opts) => {\n      const patchNavigator = (name, value) =>\n        utils.replaceProperty(Object.getPrototypeOf(navigator), name, {\n          get() {\n            return value\n          }\n        })\n\n      patchNavigator('hardwareConcurrency', opts.hardwareConcurrency || 4)\n    }",
        _args: [{}]
    }), opts = {}, Object.defineProperty(Object.getPrototypeOf(navigator), "languages", {get: () => opts.languages || ["en-US", "en"]}), (({_utilsFns: _utilsFns, _mainFunction: _mainFunction, _args: _args}) => {
        const utils = Object.fromEntries(Object.entries(_utilsFns).map((([key, value]) => [key, eval(value)])));
        utils.preloadCache(), eval(_mainFunction)(utils, ..._args)
    })({
        _utilsFns: {
            stripProxyFromErrors: "(handler = {}) => {\n  const newHandler = {}\n  // We wrap each trap in the handler in a try/catch and modify the error stack if they throw\n  const traps = Object.getOwnPropertyNames(handler)\n  traps.forEach(trap => {\n    newHandler[trap] = function() {\n      try {\n        // Forward the call to the defined proxy handler\n        return handler[trap].apply(this, arguments || [])\n      } catch (err) {\n        // Stack traces differ per browser, we only support chromium based ones currently\n        if (!err || !err.stack || !err.stack.includes(`at `)) {\n          throw err\n        }\n\n        // When something throws within one of our traps the Proxy will show up in error stacks\n        // An earlier implementation of this code would simply strip lines with a blacklist,\n        // but it makes sense to be more surgical here and only remove lines related to our Proxy.\n        // We try to use a known \"anchor\" line for that and strip it with everything above it.\n        // If the anchor line cannot be found for some reason we fall back to our blacklist approach.\n\n        const stripWithBlacklist = stack => {\n          const blacklist = [\n            `at Reflect.${trap} `, // e.g. Reflect.get or Reflect.apply\n            `at Object.${trap} `, // e.g. Object.get or Object.apply\n            `at Object.newHandler.<computed> [as ${trap}] ` // caused by this very wrapper :-)\n          ]\n          return (\n            err.stack\n              .split('\\n')\n              // Always remove the first (file) line in the stack (guaranteed to be our proxy)\n              .filter((line, index) => index !== 1)\n              // Check if the line starts with one of our blacklisted strings\n              .filter(line => !blacklist.some(bl => line.trim().startsWith(bl)))\n              .join('\\n')\n          )\n        }\n\n        const stripWithAnchor = stack => {\n          const stackArr = stack.split('\\n')\n          const anchor = `at Object.newHandler.<computed> [as ${trap}] ` // Known first Proxy line in chromium\n          const anchorIndex = stackArr.findIndex(line =>\n            line.trim().startsWith(anchor)\n          )\n          if (anchorIndex === -1) {\n            return false // 404, anchor not found\n          }\n          // Strip everything from the top until we reach the anchor line\n          // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n          stackArr.splice(1, anchorIndex)\n          return stackArr.join('\\n')\n        }\n\n        // Try using the anchor method, fallback to blacklist if necessary\n        err.stack = stripWithAnchor(err.stack) || stripWithBlacklist(err.stack)\n\n        throw err // Re-throw our now sanitized error\n      }\n    }\n  })\n  return newHandler\n}",
            stripErrorWithAnchor: "(err, anchor) => {\n  const stackArr = err.stack.split('\\n')\n  const anchorIndex = stackArr.findIndex(line => line.trim().startsWith(anchor))\n  if (anchorIndex === -1) {\n    return err // 404, anchor not found\n  }\n  // Strip everything from the top until we reach the anchor line (remove anchor line as well)\n  // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n  stackArr.splice(1, anchorIndex)\n  err.stack = stackArr.join('\\n')\n  return err\n}",
            replaceProperty: "(obj, propName, descriptorOverrides = {}) => {\n  return Object.defineProperty(obj, propName, {\n    // Copy over the existing descriptors (writable, enumerable, configurable, etc)\n    ...(Object.getOwnPropertyDescriptor(obj, propName) || {}),\n    // Add our overrides (e.g. value, get())\n    ...descriptorOverrides\n  })\n}",
            preloadCache: "() => {\n  if (utils.cache) {\n    return\n  }\n  utils.cache = {\n    // Used in our proxies\n    Reflect: {\n      get: Reflect.get.bind(Reflect),\n      apply: Reflect.apply.bind(Reflect)\n    },\n    // Used in `makeNativeString`\n    nativeToStringStr: Function.toString + '' // => `function toString() { [native code] }`\n  }\n}",
            makeNativeString: "(name = '') => {\n  // Cache (per-window) the original native toString or use that if available\n  utils.preloadCache()\n  return utils.cache.nativeToStringStr.replace('toString', name || '')\n}",
            patchToString: "(obj, str = '') => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n      // `toString` targeted at our proxied Object detected\n      if (ctx === obj) {\n        // We either return the optional string verbatim or derive the most desired result automatically\n        return str || utils.makeNativeString(obj.name)\n      }\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            patchToStringNested: "(obj = {}) => {\n  return utils.execRecursively(obj, ['function'], utils.patchToString)\n}",
            redirectToString: "(proxyObj, originalObj) => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n\n      // `toString` targeted at our proxied Object detected\n      if (ctx === proxyObj) {\n        const fallback = () =>\n          originalObj && originalObj.name\n            ? utils.makeNativeString(originalObj.name)\n            : utils.makeNativeString(proxyObj.name)\n\n        // Return the toString representation of our original object if possible\n        return originalObj + '' || fallback()\n      }\n\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            replaceWithProxy: "(obj, propName, handler) => {\n  utils.preloadCache()\n  const originalObj = obj[propName]\n  const proxyObj = new Proxy(obj[propName], utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.redirectToString(proxyObj, originalObj)\n\n  return true\n}",
            mockWithProxy: "(obj, propName, pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.patchToString(proxyObj)\n\n  return true\n}",
            createProxy: "(pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n  utils.patchToString(proxyObj)\n\n  return proxyObj\n}",
            splitObjPath: "objPath => ({\n  // Remove last dot entry (property) ==> `HTMLMediaElement.prototype`\n  objName: objPath\n    .split('.')\n    .slice(0, -1)\n    .join('.'),\n  // Extract last dot entry ==> `canPlayType`\n  propName: objPath.split('.').slice(-1)[0]\n})",
            replaceObjPathWithProxy: "(objPath, handler) => {\n  const { objName, propName } = utils.splitObjPath(objPath)\n  const obj = eval(objName) // eslint-disable-line no-eval\n  return utils.replaceWithProxy(obj, propName, handler)\n}",
            execRecursively: "(obj = {}, typeFilter = [], fn) => {\n  function recurse(obj) {\n    for (const key in obj) {\n      if (obj[key] === undefined) {\n        continue\n      }\n      if (obj[key] && typeof obj[key] === 'object') {\n        recurse(obj[key])\n      } else {\n        if (obj[key] && typeFilter.includes(typeof obj[key])) {\n          fn.call(this, obj[key])\n        }\n      }\n    }\n  }\n  recurse(obj)\n  return obj\n}",
            stringifyFns: "(fnObj = { hello: () => 'world' }) => {\n  // Object.fromEntries() ponyfill (in 6 lines) - supported only in Node v12+, modern browsers are fine\n  // https://github.com/feross/fromentries\n  function fromEntries(iterable) {\n    return [...iterable].reduce((obj, [key, val]) => {\n      obj[key] = val\n      return obj\n    }, {})\n  }\n  return (Object.fromEntries || fromEntries)(\n    Object.entries(fnObj)\n      .filter(([key, value]) => typeof value === 'function')\n      .map(([key, value]) => [key, value.toString()]) // eslint-disable-line no-eval\n  )\n}",
            materializeFns: "(fnStrObj = { hello: \"() => 'world'\" }) => {\n  return Object.fromEntries(\n    Object.entries(fnStrObj).map(([key, value]) => {\n      if (value.startsWith('function')) {\n        // some trickery is needed to make oldschool functions work :-)\n        return [key, eval(`() => ${value}`)()] // eslint-disable-line no-eval\n      } else {\n        // arrow functions just work\n        return [key, eval(value)] // eslint-disable-line no-eval\n      }\n    })\n  )\n}"
        },
        _mainFunction: "(utils, opts) => {\n      const handler = {\n        apply: function(target, ctx, args) {\n          const param = (args || [])[0]\n\n          if (param && param.name && param.name === 'notifications') {\n            const result = { state: Notification.permission }\n            Object.setPrototypeOf(result, PermissionStatus.prototype)\n            return Promise.resolve(result)\n          }\n\n          return utils.cache.Reflect.apply(...arguments)\n        }\n      }\n\n      utils.replaceWithProxy(\n        window.navigator.permissions.__proto__, // eslint-disable-line no-proto\n        'query',\n        handler\n      )\n    }",
        _args: [{}]
    }), (({_utilsFns: _utilsFns, _mainFunction: _mainFunction, _args: _args}) => {
        const utils = Object.fromEntries(Object.entries(_utilsFns).map((([key, value]) => [key, eval(value)])));
        utils.preloadCache(), eval(_mainFunction)(utils, ..._args)
    })({
        _utilsFns: {
            stripProxyFromErrors: "(handler = {}) => {\n  const newHandler = {}\n  // We wrap each trap in the handler in a try/catch and modify the error stack if they throw\n  const traps = Object.getOwnPropertyNames(handler)\n  traps.forEach(trap => {\n    newHandler[trap] = function() {\n      try {\n        // Forward the call to the defined proxy handler\n        return handler[trap].apply(this, arguments || [])\n      } catch (err) {\n        // Stack traces differ per browser, we only support chromium based ones currently\n        if (!err || !err.stack || !err.stack.includes(`at `)) {\n          throw err\n        }\n\n        // When something throws within one of our traps the Proxy will show up in error stacks\n        // An earlier implementation of this code would simply strip lines with a blacklist,\n        // but it makes sense to be more surgical here and only remove lines related to our Proxy.\n        // We try to use a known \"anchor\" line for that and strip it with everything above it.\n        // If the anchor line cannot be found for some reason we fall back to our blacklist approach.\n\n        const stripWithBlacklist = stack => {\n          const blacklist = [\n            `at Reflect.${trap} `, // e.g. Reflect.get or Reflect.apply\n            `at Object.${trap} `, // e.g. Object.get or Object.apply\n            `at Object.newHandler.<computed> [as ${trap}] ` // caused by this very wrapper :-)\n          ]\n          return (\n            err.stack\n              .split('\\n')\n              // Always remove the first (file) line in the stack (guaranteed to be our proxy)\n              .filter((line, index) => index !== 1)\n              // Check if the line starts with one of our blacklisted strings\n              .filter(line => !blacklist.some(bl => line.trim().startsWith(bl)))\n              .join('\\n')\n          )\n        }\n\n        const stripWithAnchor = stack => {\n          const stackArr = stack.split('\\n')\n          const anchor = `at Object.newHandler.<computed> [as ${trap}] ` // Known first Proxy line in chromium\n          const anchorIndex = stackArr.findIndex(line =>\n            line.trim().startsWith(anchor)\n          )\n          if (anchorIndex === -1) {\n            return false // 404, anchor not found\n          }\n          // Strip everything from the top until we reach the anchor line\n          // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n          stackArr.splice(1, anchorIndex)\n          return stackArr.join('\\n')\n        }\n\n        // Try using the anchor method, fallback to blacklist if necessary\n        err.stack = stripWithAnchor(err.stack) || stripWithBlacklist(err.stack)\n\n        throw err // Re-throw our now sanitized error\n      }\n    }\n  })\n  return newHandler\n}",
            stripErrorWithAnchor: "(err, anchor) => {\n  const stackArr = err.stack.split('\\n')\n  const anchorIndex = stackArr.findIndex(line => line.trim().startsWith(anchor))\n  if (anchorIndex === -1) {\n    return err // 404, anchor not found\n  }\n  // Strip everything from the top until we reach the anchor line (remove anchor line as well)\n  // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n  stackArr.splice(1, anchorIndex)\n  err.stack = stackArr.join('\\n')\n  return err\n}",
            replaceProperty: "(obj, propName, descriptorOverrides = {}) => {\n  return Object.defineProperty(obj, propName, {\n    // Copy over the existing descriptors (writable, enumerable, configurable, etc)\n    ...(Object.getOwnPropertyDescriptor(obj, propName) || {}),\n    // Add our overrides (e.g. value, get())\n    ...descriptorOverrides\n  })\n}",
            preloadCache: "() => {\n  if (utils.cache) {\n    return\n  }\n  utils.cache = {\n    // Used in our proxies\n    Reflect: {\n      get: Reflect.get.bind(Reflect),\n      apply: Reflect.apply.bind(Reflect)\n    },\n    // Used in `makeNativeString`\n    nativeToStringStr: Function.toString + '' // => `function toString() { [native code] }`\n  }\n}",
            makeNativeString: "(name = '') => {\n  // Cache (per-window) the original native toString or use that if available\n  utils.preloadCache()\n  return utils.cache.nativeToStringStr.replace('toString', name || '')\n}",
            patchToString: "(obj, str = '') => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n      // `toString` targeted at our proxied Object detected\n      if (ctx === obj) {\n        // We either return the optional string verbatim or derive the most desired result automatically\n        return str || utils.makeNativeString(obj.name)\n      }\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            patchToStringNested: "(obj = {}) => {\n  return utils.execRecursively(obj, ['function'], utils.patchToString)\n}",
            redirectToString: "(proxyObj, originalObj) => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n\n      // `toString` targeted at our proxied Object detected\n      if (ctx === proxyObj) {\n        const fallback = () =>\n          originalObj && originalObj.name\n            ? utils.makeNativeString(originalObj.name)\n            : utils.makeNativeString(proxyObj.name)\n\n        // Return the toString representation of our original object if possible\n        return originalObj + '' || fallback()\n      }\n\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            replaceWithProxy: "(obj, propName, handler) => {\n  utils.preloadCache()\n  const originalObj = obj[propName]\n  const proxyObj = new Proxy(obj[propName], utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.redirectToString(proxyObj, originalObj)\n\n  return true\n}",
            mockWithProxy: "(obj, propName, pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.patchToString(proxyObj)\n\n  return true\n}",
            createProxy: "(pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n  utils.patchToString(proxyObj)\n\n  return proxyObj\n}",
            splitObjPath: "objPath => ({\n  // Remove last dot entry (property) ==> `HTMLMediaElement.prototype`\n  objName: objPath\n    .split('.')\n    .slice(0, -1)\n    .join('.'),\n  // Extract last dot entry ==> `canPlayType`\n  propName: objPath.split('.').slice(-1)[0]\n})",
            replaceObjPathWithProxy: "(objPath, handler) => {\n  const { objName, propName } = utils.splitObjPath(objPath)\n  const obj = eval(objName) // eslint-disable-line no-eval\n  return utils.replaceWithProxy(obj, propName, handler)\n}",
            execRecursively: "(obj = {}, typeFilter = [], fn) => {\n  function recurse(obj) {\n    for (const key in obj) {\n      if (obj[key] === undefined) {\n        continue\n      }\n      if (obj[key] && typeof obj[key] === 'object') {\n        recurse(obj[key])\n      } else {\n        if (obj[key] && typeFilter.includes(typeof obj[key])) {\n          fn.call(this, obj[key])\n        }\n      }\n    }\n  }\n  recurse(obj)\n  return obj\n}",
            stringifyFns: "(fnObj = { hello: () => 'world' }) => {\n  // Object.fromEntries() ponyfill (in 6 lines) - supported only in Node v12+, modern browsers are fine\n  // https://github.com/feross/fromentries\n  function fromEntries(iterable) {\n    return [...iterable].reduce((obj, [key, val]) => {\n      obj[key] = val\n      return obj\n    }, {})\n  }\n  return (Object.fromEntries || fromEntries)(\n    Object.entries(fnObj)\n      .filter(([key, value]) => typeof value === 'function')\n      .map(([key, value]) => [key, value.toString()]) // eslint-disable-line no-eval\n  )\n}",
            materializeFns: "(fnStrObj = { hello: \"() => 'world'\" }) => {\n  return Object.fromEntries(\n    Object.entries(fnStrObj).map(([key, value]) => {\n      if (value.startsWith('function')) {\n        // some trickery is needed to make oldschool functions work :-)\n        return [key, eval(`() => ${value}`)()] // eslint-disable-line no-eval\n      } else {\n        // arrow functions just work\n        return [key, eval(value)] // eslint-disable-line no-eval\n      }\n    })\n  )\n}"
        },
        _mainFunction: "(utils, { fns, data }) => {\n        fns = utils.materializeFns(fns)\n\n        // That means we're running headful\n        const hasPlugins = 'plugins' in navigator && navigator.plugins.length\n        if (hasPlugins) {\n          return // nothing to do here\n        }\n\n        const mimeTypes = fns.generateMimeTypeArray(utils, fns)(data.mimeTypes)\n        const plugins = fns.generatePluginArray(utils, fns)(data.plugins)\n\n        // Plugin and MimeType cross-reference each other, let's do that now\n        // Note: We're looping through `data.plugins` here, not the generated `plugins`\n        for (const pluginData of data.plugins) {\n          pluginData.__mimeTypes.forEach((type, index) => {\n            plugins[pluginData.name][index] = mimeTypes[type]\n\n            Object.defineProperty(plugins[pluginData.name], type, {\n              value: mimeTypes[type],\n              writable: false,\n              enumerable: false, // Not enumerable\n              configurable: true\n            })\n            Object.defineProperty(mimeTypes[type], 'enabledPlugin', {\n              value: new Proxy(plugins[pluginData.name], {}), // Prevent circular references\n              writable: false,\n              enumerable: false, // Important: `JSON.stringify(navigator.plugins)`\n              configurable: true\n            })\n          })\n        }\n\n        const patchNavigator = (name, value) =>\n          utils.replaceProperty(Object.getPrototypeOf(navigator), name, {\n            get() {\n              return value\n            }\n          })\n\n        patchNavigator('mimeTypes', mimeTypes)\n        patchNavigator('plugins', plugins)\n\n        // All done\n      }",
        _args: [{
            fns: {
                generateMimeTypeArray: "(utils, fns) => mimeTypesData => {\n  return fns.generateMagicArray(utils, fns)(\n    mimeTypesData,\n    MimeTypeArray.prototype,\n    MimeType.prototype,\n    'type'\n  )\n}",
                generatePluginArray: "(utils, fns) => pluginsData => {\n  return fns.generateMagicArray(utils, fns)(\n    pluginsData,\n    PluginArray.prototype,\n    Plugin.prototype,\n    'name'\n  )\n}",
                generateMagicArray: "(utils, fns) =>\n  function(\n    dataArray = [],\n    proto = MimeTypeArray.prototype,\n    itemProto = MimeType.prototype,\n    itemMainProp = 'type'\n  ) {\n    // Quick helper to set props with the same descriptors vanilla is using\n    const defineProp = (obj, prop, value) =>\n      Object.defineProperty(obj, prop, {\n        value,\n        writable: false,\n        enumerable: false, // Important for mimeTypes & plugins: `JSON.stringify(navigator.mimeTypes)`\n        configurable: true\n      })\n\n    // Loop over our fake data and construct items\n    const makeItem = data => {\n      const item = {}\n      for (const prop of Object.keys(data)) {\n        if (prop.startsWith('__')) {\n          continue\n        }\n        defineProp(item, prop, data[prop])\n      }\n      return patchItem(item, data)\n    }\n\n    const patchItem = (item, data) => {\n      let descriptor = Object.getOwnPropertyDescriptors(item)\n\n      // Special case: Plugins have a magic length property which is not enumerable\n      // e.g. `navigator.plugins[i].length` should always be the length of the assigned mimeTypes\n      if (itemProto === Plugin.prototype) {\n        descriptor = {\n          ...descriptor,\n          length: {\n            value: data.__mimeTypes.length,\n            writable: false,\n            enumerable: false,\n            configurable: true // Important to be able to use the ownKeys trap in a Proxy to strip `length`\n          }\n        }\n      }\n\n      // We need to spoof a specific `MimeType` or `Plugin` object\n      const obj = Object.create(itemProto, descriptor)\n\n      // Virtually all property keys are not enumerable in vanilla\n      const blacklist = [...Object.keys(data), 'length', 'enabledPlugin']\n      return new Proxy(obj, {\n        ownKeys(target) {\n          return Reflect.ownKeys(target).filter(k => !blacklist.includes(k))\n        },\n        getOwnPropertyDescriptor(target, prop) {\n          if (blacklist.includes(prop)) {\n            return undefined\n          }\n          return Reflect.getOwnPropertyDescriptor(target, prop)\n        }\n      })\n    }\n\n    const magicArray = []\n\n    // Loop through our fake data and use that to create convincing entities\n    dataArray.forEach(data => {\n      magicArray.push(makeItem(data))\n    })\n\n    // Add direct property access  based on types (e.g. `obj['application/pdf']`) afterwards\n    magicArray.forEach(entry => {\n      defineProp(magicArray, entry[itemMainProp], entry)\n    })\n\n    // This is the best way to fake the type to make sure this is false: `Array.isArray(navigator.mimeTypes)`\n    const magicArrayObj = Object.create(proto, {\n      ...Object.getOwnPropertyDescriptors(magicArray),\n\n      // There's one ugly quirk we unfortunately need to take care of:\n      // The `MimeTypeArray` prototype has an enumerable `length` property,\n      // but headful Chrome will still skip it when running `Object.getOwnPropertyNames(navigator.mimeTypes)`.\n      // To strip it we need to make it first `configurable` and can then overlay a Proxy with an `ownKeys` trap.\n      length: {\n        value: magicArray.length,\n        writable: false,\n        enumerable: false,\n        configurable: true // Important to be able to use the ownKeys trap in a Proxy to strip `length`\n      }\n    })\n\n    // Generate our functional function mocks :-)\n    const functionMocks = fns.generateFunctionMocks(utils)(\n      proto,\n      itemMainProp,\n      magicArray\n    )\n\n    // We need to overlay our custom object with a JS Proxy\n    const magicArrayObjProxy = new Proxy(magicArrayObj, {\n      get(target, key = '') {\n        // Redirect function calls to our custom proxied versions mocking the vanilla behavior\n        if (key === 'item') {\n          return functionMocks.item\n        }\n        if (key === 'namedItem') {\n          return functionMocks.namedItem\n        }\n        if (proto === PluginArray.prototype && key === 'refresh') {\n          return functionMocks.refresh\n        }\n        // Everything else can pass through as normal\n        return utils.cache.Reflect.get(...arguments)\n      },\n      ownKeys(target) {\n        // There are a couple of quirks where the original property demonstrates \"magical\" behavior that makes no sense\n        // This can be witnessed when calling `Object.getOwnPropertyNames(navigator.mimeTypes)` and the absense of `length`\n        // My guess is that it has to do with the recent change of not allowing data enumeration and this being implemented weirdly\n        // For that reason we just completely fake the available property names based on our data to match what regular Chrome is doing\n        // Specific issues when not patching this: `length` property is available, direct `types` props (e.g. `obj['application/pdf']`) are missing\n        const keys = []\n        const typeProps = magicArray.map(mt => mt[itemMainProp])\n        typeProps.forEach((_, i) => keys.push(`${i}`))\n        typeProps.forEach(propName => keys.push(propName))\n        return keys\n      },\n      getOwnPropertyDescriptor(target, prop) {\n        if (prop === 'length') {\n          return undefined\n        }\n        return Reflect.getOwnPropertyDescriptor(target, prop)\n      }\n    })\n\n    return magicArrayObjProxy\n  }",
                generateFunctionMocks: "utils => (\n  proto,\n  itemMainProp,\n  dataArray\n) => ({\n  /** Returns the MimeType object with the specified index. */\n  item: utils.createProxy(proto.item, {\n    apply(target, ctx, args) {\n      if (!args.length) {\n        throw new TypeError(\n          `Failed to execute 'item' on '${\n            proto[Symbol.toStringTag]\n          }': 1 argument required, but only 0 present.`\n        )\n      }\n      // Special behavior alert:\n      // - Vanilla tries to cast strings to Numbers (only integers!) and use them as property index lookup\n      // - If anything else than an integer (including as string) is provided it will return the first entry\n      const isInteger = args[0] && Number.isInteger(Number(args[0])) // Cast potential string to number first, then check for integer\n      // Note: Vanilla never returns `undefined`\n      return (isInteger ? dataArray[Number(args[0])] : dataArray[0]) || null\n    }\n  }),\n  /** Returns the MimeType object with the specified name. */\n  namedItem: utils.createProxy(proto.namedItem, {\n    apply(target, ctx, args) {\n      if (!args.length) {\n        throw new TypeError(\n          `Failed to execute 'namedItem' on '${\n            proto[Symbol.toStringTag]\n          }': 1 argument required, but only 0 present.`\n        )\n      }\n      return dataArray.find(mt => mt[itemMainProp] === args[0]) || null // Not `undefined`!\n    }\n  }),\n  /** Does nothing and shall return nothing */\n  refresh: proto.refresh\n    ? utils.createProxy(proto.refresh, {\n        apply(target, ctx, args) {\n          return undefined\n        }\n      })\n    : undefined\n})"
            },
            data: {
                mimeTypes: [{
                    type: "application/pdf",
                    suffixes: "pdf",
                    description: "",
                    __pluginName: "Chrome PDF Viewer"
                }, {
                    type: "application/x-google-chrome-pdf",
                    suffixes: "pdf",
                    description: "Portable Document Format",
                    __pluginName: "Chrome PDF Plugin"
                }, {
                    type: "application/x-nacl",
                    suffixes: "",
                    description: "Native Client Executable",
                    __pluginName: "Native Client"
                }, {
                    type: "application/x-pnacl",
                    suffixes: "",
                    description: "Portable Native Client Executable",
                    __pluginName: "Native Client"
                }],
                plugins: [{
                    name: "Chrome PDF Plugin",
                    filename: "internal-pdf-viewer",
                    description: "Portable Document Format",
                    __mimeTypes: ["application/x-google-chrome-pdf"]
                }, {
                    name: "Chrome PDF Viewer",
                    filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                    description: "",
                    __mimeTypes: ["application/pdf"]
                }, {
                    name: "Native Client",
                    filename: "internal-nacl-plugin",
                    description: "",
                    __mimeTypes: ["application/x-nacl", "application/x-pnacl"]
                }]
            }
        }]
    }), delete Object.getPrototypeOf(navigator).webdriver, (({_utilsFns: _utilsFns, _mainFunction: _mainFunction, _args: _args}) => {
        const utils = Object.fromEntries(Object.entries(_utilsFns).map((([key, value]) => [key, eval(value)])));
        utils.preloadCache(), eval(_mainFunction)(utils, ..._args)
    })({
        _utilsFns: {
            stripProxyFromErrors: "(handler = {}) => {\n  const newHandler = {}\n  // We wrap each trap in the handler in a try/catch and modify the error stack if they throw\n  const traps = Object.getOwnPropertyNames(handler)\n  traps.forEach(trap => {\n    newHandler[trap] = function() {\n      try {\n        // Forward the call to the defined proxy handler\n        return handler[trap].apply(this, arguments || [])\n      } catch (err) {\n        // Stack traces differ per browser, we only support chromium based ones currently\n        if (!err || !err.stack || !err.stack.includes(`at `)) {\n          throw err\n        }\n\n        // When something throws within one of our traps the Proxy will show up in error stacks\n        // An earlier implementation of this code would simply strip lines with a blacklist,\n        // but it makes sense to be more surgical here and only remove lines related to our Proxy.\n        // We try to use a known \"anchor\" line for that and strip it with everything above it.\n        // If the anchor line cannot be found for some reason we fall back to our blacklist approach.\n\n        const stripWithBlacklist = stack => {\n          const blacklist = [\n            `at Reflect.${trap} `, // e.g. Reflect.get or Reflect.apply\n            `at Object.${trap} `, // e.g. Object.get or Object.apply\n            `at Object.newHandler.<computed> [as ${trap}] ` // caused by this very wrapper :-)\n          ]\n          return (\n            err.stack\n              .split('\\n')\n              // Always remove the first (file) line in the stack (guaranteed to be our proxy)\n              .filter((line, index) => index !== 1)\n              // Check if the line starts with one of our blacklisted strings\n              .filter(line => !blacklist.some(bl => line.trim().startsWith(bl)))\n              .join('\\n')\n          )\n        }\n\n        const stripWithAnchor = stack => {\n          const stackArr = stack.split('\\n')\n          const anchor = `at Object.newHandler.<computed> [as ${trap}] ` // Known first Proxy line in chromium\n          const anchorIndex = stackArr.findIndex(line =>\n            line.trim().startsWith(anchor)\n          )\n          if (anchorIndex === -1) {\n            return false // 404, anchor not found\n          }\n          // Strip everything from the top until we reach the anchor line\n          // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n          stackArr.splice(1, anchorIndex)\n          return stackArr.join('\\n')\n        }\n\n        // Try using the anchor method, fallback to blacklist if necessary\n        err.stack = stripWithAnchor(err.stack) || stripWithBlacklist(err.stack)\n\n        throw err // Re-throw our now sanitized error\n      }\n    }\n  })\n  return newHandler\n}",
            stripErrorWithAnchor: "(err, anchor) => {\n  const stackArr = err.stack.split('\\n')\n  const anchorIndex = stackArr.findIndex(line => line.trim().startsWith(anchor))\n  if (anchorIndex === -1) {\n    return err // 404, anchor not found\n  }\n  // Strip everything from the top until we reach the anchor line (remove anchor line as well)\n  // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n  stackArr.splice(1, anchorIndex)\n  err.stack = stackArr.join('\\n')\n  return err\n}",
            replaceProperty: "(obj, propName, descriptorOverrides = {}) => {\n  return Object.defineProperty(obj, propName, {\n    // Copy over the existing descriptors (writable, enumerable, configurable, etc)\n    ...(Object.getOwnPropertyDescriptor(obj, propName) || {}),\n    // Add our overrides (e.g. value, get())\n    ...descriptorOverrides\n  })\n}",
            preloadCache: "() => {\n  if (utils.cache) {\n    return\n  }\n  utils.cache = {\n    // Used in our proxies\n    Reflect: {\n      get: Reflect.get.bind(Reflect),\n      apply: Reflect.apply.bind(Reflect)\n    },\n    // Used in `makeNativeString`\n    nativeToStringStr: Function.toString + '' // => `function toString() { [native code] }`\n  }\n}",
            makeNativeString: "(name = '') => {\n  // Cache (per-window) the original native toString or use that if available\n  utils.preloadCache()\n  return utils.cache.nativeToStringStr.replace('toString', name || '')\n}",
            patchToString: "(obj, str = '') => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n      // `toString` targeted at our proxied Object detected\n      if (ctx === obj) {\n        // We either return the optional string verbatim or derive the most desired result automatically\n        return str || utils.makeNativeString(obj.name)\n      }\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            patchToStringNested: "(obj = {}) => {\n  return utils.execRecursively(obj, ['function'], utils.patchToString)\n}",
            redirectToString: "(proxyObj, originalObj) => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n\n      // `toString` targeted at our proxied Object detected\n      if (ctx === proxyObj) {\n        const fallback = () =>\n          originalObj && originalObj.name\n            ? utils.makeNativeString(originalObj.name)\n            : utils.makeNativeString(proxyObj.name)\n\n        // Return the toString representation of our original object if possible\n        return originalObj + '' || fallback()\n      }\n\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            replaceWithProxy: "(obj, propName, handler) => {\n  utils.preloadCache()\n  const originalObj = obj[propName]\n  const proxyObj = new Proxy(obj[propName], utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.redirectToString(proxyObj, originalObj)\n\n  return true\n}",
            mockWithProxy: "(obj, propName, pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.patchToString(proxyObj)\n\n  return true\n}",
            createProxy: "(pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n  utils.patchToString(proxyObj)\n\n  return proxyObj\n}",
            splitObjPath: "objPath => ({\n  // Remove last dot entry (property) ==> `HTMLMediaElement.prototype`\n  objName: objPath\n    .split('.')\n    .slice(0, -1)\n    .join('.'),\n  // Extract last dot entry ==> `canPlayType`\n  propName: objPath.split('.').slice(-1)[0]\n})",
            replaceObjPathWithProxy: "(objPath, handler) => {\n  const { objName, propName } = utils.splitObjPath(objPath)\n  const obj = eval(objName) // eslint-disable-line no-eval\n  return utils.replaceWithProxy(obj, propName, handler)\n}",
            execRecursively: "(obj = {}, typeFilter = [], fn) => {\n  function recurse(obj) {\n    for (const key in obj) {\n      if (obj[key] === undefined) {\n        continue\n      }\n      if (obj[key] && typeof obj[key] === 'object') {\n        recurse(obj[key])\n      } else {\n        if (obj[key] && typeFilter.includes(typeof obj[key])) {\n          fn.call(this, obj[key])\n        }\n      }\n    }\n  }\n  recurse(obj)\n  return obj\n}",
            stringifyFns: "(fnObj = { hello: () => 'world' }) => {\n  // Object.fromEntries() ponyfill (in 6 lines) - supported only in Node v12+, modern browsers are fine\n  // https://github.com/feross/fromentries\n  function fromEntries(iterable) {\n    return [...iterable].reduce((obj, [key, val]) => {\n      obj[key] = val\n      return obj\n    }, {})\n  }\n  return (Object.fromEntries || fromEntries)(\n    Object.entries(fnObj)\n      .filter(([key, value]) => typeof value === 'function')\n      .map(([key, value]) => [key, value.toString()]) // eslint-disable-line no-eval\n  )\n}",
            materializeFns: "(fnStrObj = { hello: \"() => 'world'\" }) => {\n  return Object.fromEntries(\n    Object.entries(fnStrObj).map(([key, value]) => {\n      if (value.startsWith('function')) {\n        // some trickery is needed to make oldschool functions work :-)\n        return [key, eval(`() => ${value}`)()] // eslint-disable-line no-eval\n      } else {\n        // arrow functions just work\n        return [key, eval(value)] // eslint-disable-line no-eval\n      }\n    })\n  )\n}"
        },
        _mainFunction: "(utils, opts) => {\n      const getParameterProxyHandler = {\n        apply: function(target, ctx, args) {\n          const param = (args || [])[0]\n          // UNMASKED_VENDOR_WEBGL\n          if (param === 37445) {\n            return opts.vendor || 'Intel Inc.' // default in headless: Google Inc.\n          }\n          // UNMASKED_RENDERER_WEBGL\n          if (param === 37446) {\n            return opts.renderer || 'Intel Iris OpenGL Engine' // default in headless: Google SwiftShader\n          }\n          return utils.cache.Reflect.apply(target, ctx, args)\n        }\n      }\n\n      // There's more than one WebGL rendering context\n      // https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext#Browser_compatibility\n      // To find out the original values here: Object.getOwnPropertyDescriptors(WebGLRenderingContext.prototype.getParameter)\n      const addProxy = (obj, propName) => {\n        utils.replaceWithProxy(obj, propName, getParameterProxyHandler)\n      }\n      // For whatever weird reason loops don't play nice with Object.defineProperty, here's the next best thing:\n      addProxy(WebGLRenderingContext.prototype, 'getParameter')\n      addProxy(WebGL2RenderingContext.prototype, 'getParameter')\n    }",
        _args: [{}]
    }), (() => {
        try {
            if (window.outerWidth && window.outerHeight) return;
            const n = 85;
            window.outerWidth = window.innerWidth, window.outerHeight = window.innerHeight + n
        } catch (n) {
        }
    })(), (({_utilsFns: _utilsFns, _mainFunction: _mainFunction, _args: _args}) => {
        const utils = Object.fromEntries(Object.entries(_utilsFns).map((([key, value]) => [key, eval(value)])));
        utils.preloadCache(), eval(_mainFunction)(utils, ..._args)
    })({
        _utilsFns: {
            stripProxyFromErrors: "(handler = {}) => {\n  const newHandler = {}\n  // We wrap each trap in the handler in a try/catch and modify the error stack if they throw\n  const traps = Object.getOwnPropertyNames(handler)\n  traps.forEach(trap => {\n    newHandler[trap] = function() {\n      try {\n        // Forward the call to the defined proxy handler\n        return handler[trap].apply(this, arguments || [])\n      } catch (err) {\n        // Stack traces differ per browser, we only support chromium based ones currently\n        if (!err || !err.stack || !err.stack.includes(`at `)) {\n          throw err\n        }\n\n        // When something throws within one of our traps the Proxy will show up in error stacks\n        // An earlier implementation of this code would simply strip lines with a blacklist,\n        // but it makes sense to be more surgical here and only remove lines related to our Proxy.\n        // We try to use a known \"anchor\" line for that and strip it with everything above it.\n        // If the anchor line cannot be found for some reason we fall back to our blacklist approach.\n\n        const stripWithBlacklist = stack => {\n          const blacklist = [\n            `at Reflect.${trap} `, // e.g. Reflect.get or Reflect.apply\n            `at Object.${trap} `, // e.g. Object.get or Object.apply\n            `at Object.newHandler.<computed> [as ${trap}] ` // caused by this very wrapper :-)\n          ]\n          return (\n            err.stack\n              .split('\\n')\n              // Always remove the first (file) line in the stack (guaranteed to be our proxy)\n              .filter((line, index) => index !== 1)\n              // Check if the line starts with one of our blacklisted strings\n              .filter(line => !blacklist.some(bl => line.trim().startsWith(bl)))\n              .join('\\n')\n          )\n        }\n\n        const stripWithAnchor = stack => {\n          const stackArr = stack.split('\\n')\n          const anchor = `at Object.newHandler.<computed> [as ${trap}] ` // Known first Proxy line in chromium\n          const anchorIndex = stackArr.findIndex(line =>\n            line.trim().startsWith(anchor)\n          )\n          if (anchorIndex === -1) {\n            return false // 404, anchor not found\n          }\n          // Strip everything from the top until we reach the anchor line\n          // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n          stackArr.splice(1, anchorIndex)\n          return stackArr.join('\\n')\n        }\n\n        // Try using the anchor method, fallback to blacklist if necessary\n        err.stack = stripWithAnchor(err.stack) || stripWithBlacklist(err.stack)\n\n        throw err // Re-throw our now sanitized error\n      }\n    }\n  })\n  return newHandler\n}",
            stripErrorWithAnchor: "(err, anchor) => {\n  const stackArr = err.stack.split('\\n')\n  const anchorIndex = stackArr.findIndex(line => line.trim().startsWith(anchor))\n  if (anchorIndex === -1) {\n    return err // 404, anchor not found\n  }\n  // Strip everything from the top until we reach the anchor line (remove anchor line as well)\n  // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)\n  stackArr.splice(1, anchorIndex)\n  err.stack = stackArr.join('\\n')\n  return err\n}",
            replaceProperty: "(obj, propName, descriptorOverrides = {}) => {\n  return Object.defineProperty(obj, propName, {\n    // Copy over the existing descriptors (writable, enumerable, configurable, etc)\n    ...(Object.getOwnPropertyDescriptor(obj, propName) || {}),\n    // Add our overrides (e.g. value, get())\n    ...descriptorOverrides\n  })\n}",
            preloadCache: "() => {\n  if (utils.cache) {\n    return\n  }\n  utils.cache = {\n    // Used in our proxies\n    Reflect: {\n      get: Reflect.get.bind(Reflect),\n      apply: Reflect.apply.bind(Reflect)\n    },\n    // Used in `makeNativeString`\n    nativeToStringStr: Function.toString + '' // => `function toString() { [native code] }`\n  }\n}",
            makeNativeString: "(name = '') => {\n  // Cache (per-window) the original native toString or use that if available\n  utils.preloadCache()\n  return utils.cache.nativeToStringStr.replace('toString', name || '')\n}",
            patchToString: "(obj, str = '') => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n      // `toString` targeted at our proxied Object detected\n      if (ctx === obj) {\n        // We either return the optional string verbatim or derive the most desired result automatically\n        return str || utils.makeNativeString(obj.name)\n      }\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            patchToStringNested: "(obj = {}) => {\n  return utils.execRecursively(obj, ['function'], utils.patchToString)\n}",
            redirectToString: "(proxyObj, originalObj) => {\n  utils.preloadCache()\n\n  const toStringProxy = new Proxy(Function.prototype.toString, {\n    apply: function(target, ctx) {\n      // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + \"\"`\n      if (ctx === Function.prototype.toString) {\n        return utils.makeNativeString('toString')\n      }\n\n      // `toString` targeted at our proxied Object detected\n      if (ctx === proxyObj) {\n        const fallback = () =>\n          originalObj && originalObj.name\n            ? utils.makeNativeString(originalObj.name)\n            : utils.makeNativeString(proxyObj.name)\n\n        // Return the toString representation of our original object if possible\n        return originalObj + '' || fallback()\n      }\n\n      // Check if the toString protype of the context is the same as the global prototype,\n      // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case\n      const hasSameProto = Object.getPrototypeOf(\n        Function.prototype.toString\n      ).isPrototypeOf(ctx.toString) // eslint-disable-line no-prototype-builtins\n      if (!hasSameProto) {\n        // Pass the call on to the local Function.prototype.toString instead\n        return ctx.toString()\n      }\n\n      return target.call(ctx)\n    }\n  })\n  utils.replaceProperty(Function.prototype, 'toString', {\n    value: toStringProxy\n  })\n}",
            replaceWithProxy: "(obj, propName, handler) => {\n  utils.preloadCache()\n  const originalObj = obj[propName]\n  const proxyObj = new Proxy(obj[propName], utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.redirectToString(proxyObj, originalObj)\n\n  return true\n}",
            mockWithProxy: "(obj, propName, pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n\n  utils.replaceProperty(obj, propName, { value: proxyObj })\n  utils.patchToString(proxyObj)\n\n  return true\n}",
            createProxy: "(pseudoTarget, handler) => {\n  utils.preloadCache()\n  const proxyObj = new Proxy(pseudoTarget, utils.stripProxyFromErrors(handler))\n  utils.patchToString(proxyObj)\n\n  return proxyObj\n}",
            splitObjPath: "objPath => ({\n  // Remove last dot entry (property) ==> `HTMLMediaElement.prototype`\n  objName: objPath\n    .split('.')\n    .slice(0, -1)\n    .join('.'),\n  // Extract last dot entry ==> `canPlayType`\n  propName: objPath.split('.').slice(-1)[0]\n})",
            replaceObjPathWithProxy: "(objPath, handler) => {\n  const { objName, propName } = utils.splitObjPath(objPath)\n  const obj = eval(objName) // eslint-disable-line no-eval\n  return utils.replaceWithProxy(obj, propName, handler)\n}",
            execRecursively: "(obj = {}, typeFilter = [], fn) => {\n  function recurse(obj) {\n    for (const key in obj) {\n      if (obj[key] === undefined) {\n        continue\n      }\n      if (obj[key] && typeof obj[key] === 'object') {\n        recurse(obj[key])\n      } else {\n        if (obj[key] && typeFilter.includes(typeof obj[key])) {\n          fn.call(this, obj[key])\n        }\n      }\n    }\n  }\n  recurse(obj)\n  return obj\n}",
            stringifyFns: "(fnObj = { hello: () => 'world' }) => {\n  // Object.fromEntries() ponyfill (in 6 lines) - supported only in Node v12+, modern browsers are fine\n  // https://github.com/feross/fromentries\n  function fromEntries(iterable) {\n    return [...iterable].reduce((obj, [key, val]) => {\n      obj[key] = val\n      return obj\n    }, {})\n  }\n  return (Object.fromEntries || fromEntries)(\n    Object.entries(fnObj)\n      .filter(([key, value]) => typeof value === 'function')\n      .map(([key, value]) => [key, value.toString()]) // eslint-disable-line no-eval\n  )\n}",
            materializeFns: "(fnStrObj = { hello: \"() => 'world'\" }) => {\n  return Object.fromEntries(\n    Object.entries(fnStrObj).map(([key, value]) => {\n      if (value.startsWith('function')) {\n        // some trickery is needed to make oldschool functions work :-)\n        return [key, eval(`() => ${value}`)()] // eslint-disable-line no-eval\n      } else {\n        // arrow functions just work\n        return [key, eval(value)] // eslint-disable-line no-eval\n      }\n    })\n  )\n}"
        },
        _mainFunction: "(utils, opts) => {\n      try {\n        // Adds a contentWindow proxy to the provided iframe element\n        const addContentWindowProxy = iframe => {\n          const contentWindowProxy = {\n            get(target, key) {\n              // Now to the interesting part:\n              // We actually make this thing behave like a regular iframe window,\n              // by intercepting calls to e.g. `.self` and redirect it to the correct thing. :)\n              // That makes it possible for these assertions to be correct:\n              // iframe.contentWindow.self === window.top // must be false\n              if (key === 'self') {\n                return this\n              }\n              // iframe.contentWindow.frameElement === iframe // must be true\n              if (key === 'frameElement') {\n                return iframe\n              }\n              return Reflect.get(target, key)\n            }\n          }\n\n          if (!iframe.contentWindow) {\n            const proxy = new Proxy(window, contentWindowProxy)\n            Object.defineProperty(iframe, 'contentWindow', {\n              get() {\n                return proxy\n              },\n              set(newValue) {\n                return newValue // contentWindow is immutable\n              },\n              enumerable: true,\n              configurable: false\n            })\n          }\n        }\n\n        // Handles iframe element creation, augments `srcdoc` property so we can intercept further\n        const handleIframeCreation = (target, thisArg, args) => {\n          const iframe = target.apply(thisArg, args)\n\n          // We need to keep the originals around\n          const _iframe = iframe\n          const _srcdoc = _iframe.srcdoc\n\n          // Add hook for the srcdoc property\n          // We need to be very surgical here to not break other iframes by accident\n          Object.defineProperty(iframe, 'srcdoc', {\n            configurable: true, // Important, so we can reset this later\n            get: function() {\n              return _iframe.srcdoc\n            },\n            set: function(newValue) {\n              addContentWindowProxy(this)\n              // Reset property, the hook is only needed once\n              Object.defineProperty(iframe, 'srcdoc', {\n                configurable: false,\n                writable: false,\n                value: _srcdoc\n              })\n              _iframe.srcdoc = newValue\n            }\n          })\n          return iframe\n        }\n\n        // Adds a hook to intercept iframe creation events\n        const addIframeCreationSniffer = () => {\n          /* global document */\n          const createElementHandler = {\n            // Make toString() native\n            get(target, key) {\n              return Reflect.get(target, key)\n            },\n            apply: function(target, thisArg, args) {\n              const isIframe =\n                args && args.length && `${args[0]}`.toLowerCase() === 'iframe'\n              if (!isIframe) {\n                // Everything as usual\n                return target.apply(thisArg, args)\n              } else {\n                return handleIframeCreation(target, thisArg, args)\n              }\n            }\n          }\n          // All this just due to iframes with srcdoc bug\n          utils.replaceWithProxy(\n            document,\n            'createElement',\n            createElementHandler\n          )\n        }\n\n        // Let's go\n        addIframeCreationSniffer()\n      } catch (err) {\n        // console.warn(err)\n      }\n    }",
        _args: []
    });
    """


# selenium启动方法
class AC(object):
    def __init__(self, **kwargs):
        _option = kwargs.get("_option", None)
        if not _option:
            _option = webdriver.ChromeOptions()
            _pre_fs = dict()
            _pre_fs["credentials_enable_service"] = False
            _pre_fs["profile.password_manager_enabled"] = False
            if kwargs.get('download_path', False):
                _pre_fs['profile.default_content_settings.popups'] = 0
                _pre_fs['download.default_directory'] = kwargs['download_path']
                _pre_fs['profile.default_content_setting_values.automatic_downloads'] = 1
            else:
                # 下载前询问每个文件的保存位置   True是开启，False是关闭 ,与chrome_down_path搭配使用
                _pre_fs["download.prompt_for_download"] = True
            _option.add_experimental_option("prefs", _pre_fs)  # 关掉是否记住密码弹窗
            if proxy := kwargs.get("proxy", None):
                _option.add_argument('--proxy-server=%s' % proxy)
            if kwargs.get("_headless", False):
                logging.info("开启无头")
                # 无头模式
                _option.add_argument('--headless')
            if kwargs.get("incognito", None):
                _option.add_argument('--incognito')  # 无痕模式
            # _option.add_experimental_option('w3c', False)
            _option.add_experimental_option('useAutomationExtension', False)  # 关闭“chrome正受到自动测试软件的控制”
            _option.add_experimental_option("excludeSwitches", ['enable-automation'])
            _option.add_argument("--disable-blink-features=AutomationControlled")
            _option.add_experimental_option("detach", True)  # 不自动关闭浏览器
            _option.add_argument('--disable-gpu')  # 禁用GPU加速
            _option.add_argument("disable-web-security")  # 允许谷歌浏览器重定向网址
            # cookie 新特性 禁用可以支持跨域访问
            _option.add_argument('--disable-features=SameSiteByDefaultCookies,CookiesWithoutSameSiteMustBeSecure')
            _option.add_argument('-–no-sandbox')
            if user_data := kwargs.get("user_data", None):
                _option.add_argument(f'user-data-dir={user_data}')
            if binary_location := kwargs.get("binary_location", None):
                _option.binary_location = binary_location
        self.driver = webdriver.Chrome(options=_option, executable_path=kwargs.get("exec_path", "chromedriver"))
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
        if kwargs.get("max_size", True):
            self.driver.maximize_window()


# playwright启动方法
class Page(object):
    def __init__(self, **kwargs):
        js = """
                Object.defineProperties(navigator,{webdriver:{get:()=>undefined}});
            """
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=False,
                                              executable_path=kwargs.get("exec_path", "chromedriver"),
                                              args=[
                                                  ""
                                                  "--disable-features=SameSiteByDefaultCookies, "
                                                  "CookiesWithoutSameSiteMustBeSecure"
                                                  "--start-maximized"
                                              ])
        context = self.browser.new_context(no_viewport=True)
        context.add_init_script(js)
        self.context = context
        self.page = self.context.new_page()


# 创建tk登录页面
class TkFunction:
    def __init__(self, cx_name, need_paper_path):
        self.cx_name = cx_name  # 程序名称
        self.need_paper_path = need_paper_path  # 用户输入的选择文件夹名称
        self.content_data = {}  # 记录用户输入的账号密码及选择的文件路径

    # 添加账号方法
    def zh_fun(self, root):
        # 创建两个密码输入框
        label1 = tk.Label(root, text="请输入账号：")
        self.font_ground(label1)
        entry1 = tk.Entry(root)  # 第一个密码输入框
        self.enter_ground(entry1)
        las1 = tk.Label(root, text=" ")
        label2 = tk.Label(root, text="请输入密码：")
        self.font_ground(label2)
        entry2 = tk.Entry(root, show="*")  # 第二个密码输入框
        self.enter_ground(entry2)
        las2 = tk.Label(root, text=" ")
        # 添加到布局
        label1.pack()
        entry1.pack()
        las1.pack()
        label2.pack()
        entry2.pack()
        las2.pack()
        return entry1, entry2

    # 记录输入的账号密码，写入字典
    def handle_input(self, entry1, entry2, root):
        username = entry1.get()
        password = entry2.get()
        self.content_data["账号"] = username
        self.content_data["密码"] = password
        # 关闭窗口
        root.destroy()

    # 创建一个文件选择对话框
    def select_file(self, root, index, paper_entry):
        filename = filedialog.askdirectory()
        if filename:
            paper_entry.delete(0, tk.END)  # 清空输入框内容
            paper_entry.insert(0, filename)
            self.content_data[index] = filename

    # 创建一个文件选择对话框
    def excel_file(self, parent, folder_entry):
        filename = filedialog.askopenfilename(
            parent=parent,  # 指定父窗口
            filetypes=[("Excel 文件", "*.xlsx *.xls")],
            title="选择文件"
        )
        if filename:
            folder_entry.delete(0, tk.END)  # 清空输入框内容
            folder_entry.insert(0, filename)
        self.content_data["excel地址"] = filename

    # 设置输入框样式
    def enter_ground(self, enter):
        enter.config(
            font=("Arial", 14, "bold"),  # 设置字体样式
            borderwidth=2,  # 设置边框宽度
            relief="sunken",  # 设置边框的凹陷效果
            bg="white",  # 设置背景颜色
            fg="black",  # 设置文本颜色
            selectbackground="blue",  # 设置选中文本的背景颜色
            selectforeground="white"  # 设置选中文本的文本颜色
        )

    # 设置按钮样式
    def button_ground(self, button):
        button.config(
            font=("Arial", 14, "bold"),  # 设置字体样式
            borderwidth=2,  # 设置边框宽度
            relief="groove",  # 设置边框的凹陷效果
            bg="lightgrey",  # 设置背景颜色
            fg="black",  # 设置文本颜色
            highlightbackground="red",  # 设置鼠标悬停时的背景颜色
            highlightcolor="black",  # 设置鼠标悬停时的文本颜色
        )

    # 设置字体样式
    def font_ground(self, font):
        font.config(
            font=("Arial", 14, "bold")  # 设置字体大小和颜色
        )

    # 主函数
    def tk_fun(self):
        # 创建tk窗口
        root = tk.Tk()
        # 设置tk窗口的标题
        root.title(self.cx_name)
        # 设置窗口大小
        if len(self.need_paper_path) < 1:
            root.geometry("400x450")
        else:
            height = (len(self.need_paper_path) + 1) * 150
            root.geometry(f"400x{height}")
        # 显示输入账号密码
        entry1, entry2 = self.zh_fun(root)
        # 显示excel选择的输入框
        label0 = tk.Label(root, text="请选择excel表格")
        self.font_ground(label0)
        label0.pack()
        folder_entry = tk.Entry(root)
        self.enter_ground(folder_entry)
        folder_entry.pack()
        browse_button0 = tk.Button(root, text="选择文件", command=lambda: self.excel_file(root, folder_entry))
        self.button_ground(browse_button0)
        las0 = tk.Label(root, text=" ")
        browse_button0.pack()
        las0.pack()
        # 选择文件夹的
        label3 = tk.Label(root, text="请选择文件位置")
        self.font_ground(label3)
        paper_entry = tk.Entry(root)
        self.enter_ground(paper_entry)
        browse_button = tk.Button(root, text="选择文件",
                                  command=lambda: self.select_file(root, self.need_paper_path, paper_entry))
        self.button_ground(browse_button)
        las3 = tk.Label(root, text=" ")
        label3.pack()
        paper_entry.pack()
        browse_button.pack()
        las3.pack()
        # 提交方法
        submit_button = tk.Button(root, text="提交", command=lambda: self.handle_input(entry1, entry2, root))
        self.button_ground(submit_button)
        submit_button.pack()
        root.mainloop()
        return self.content_data


# 1.15.3版本playwright切入iframe
def playwright_frame(page, xpath:list):
    frame = None
    for i in xpath:
        frame = page.query_selector(i).content_frame()
    return frame