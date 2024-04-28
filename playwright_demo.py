# import asyncio
# import time
# from playwright.async_api import async_playwright
#
# from mitmproxy.http import flow
#
# def responseheaders(flow: flow):
#     # 解决CORS
#     if 'https://blog.csdn.net/makesomethings/article/details/125293557' in flow.request.url:
#         flow.response.headers["Access-Control-Allow-Origin"] = "https://blog.csdn.net"
#         return
# async def main():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         page = await browser.new_page()
#         await page.goto("https://www.baidu.com")
#         await page.fill('xpath=//*[@id="kw"]', "csdn")
#         await page.click('xpath=//*[@id="su"]')
#         async with page.expect_popup() as page1_info:
#             print(await page.inner_text('xpath=//*[@id="1"]//a[text()=" - 专业开发者社区"]'))
#             print(await page.locator('xpath=//*[@id="1"]//a[text()=" - 专业开发者社区"]').inner_text())
#             # print(await page.get_by_placeholder('//*[@id="1"]//a').nth(1).inner_text())
#             await page.click('xpath=//*[@id="1"]//a[text()=" - 专业开发者社区"]')
#
#         print(111)
#         page1 = await page1_info.value
#         # await page1.reload()
#         # await page1.close()
#         await page1.click('//*[@id="csdn-toolbar"]/div/div/div[3]/div/div[1]/a')
#         await page1.frame_locator("iframe[name='passport_iframe']").get_by_text("密码登录").click()
#         await page1.frame_locator("iframe[name='passport_iframe']").get_by_placeholder("手机号/邮箱/用户名").fill("17633602179")
#         await page1.frame_locator("iframe[name='passport_iframe']").get_by_placeholder("密码").fill("mimashisha555...")
#         await page1.frame_locator("iframe[name='passport_iframe']").get_by_role("button", name="登录").click()
#         print(222)
#         time.sleep(2000)
#         await browser.close()
#
#
# asyncio.get_event_loop().run_until_complete(main())

# from playwright.sync_api import sync_playwright
#
# with sync_playwright() as p:
#     iphone_12_pro_max = p.devices['iPhone 12 Pro Max']
#     browser = p.webkit.launch(headless=False)
#     context = browser.new_context(
#         **iphone_12_pro_max,
#         locale='zh-CN',
#         geolocation={'longitude': 146, 'latitude': 40},
#         permissions=['geolocation']
#     )
#     page = context.new_page()
#     # time.sleep(2000)
#     page.goto('https://www.baidu.com')
#     page.locator('//*[@id="index-kw"]').fill("九溪十八")
#     page.click('//*[@id="index-bn"]')
#     print(1222)
#     page.pause()
#     # time.sleep(2000)
#     browser.close()
import os
from playwright.sync_api import Playwright, sync_playwright
from playwright._impl import _sync_base
_sync_base.is_print = True



page: Optional[Page] = None
context: Optional[BrowserContext] = None
browser: Optional[Browser] = None
p: Optional[Playwright] = None
js = """
            Object.defineProperties(navigator,{webdriver:{get:()=>undefined}});
        """
self.p = sync_playwright().start()
browser = self.p.chromium.launch(headless=False,
                                 executable_path=r"C:\HFTRPA\chrome90\90chrome完整版\chrome-win\chrome.exe",
                                 args=[
                                     "--disable-features=SameSiteByDefaultCookies, "
                                     "CookiesWithoutSameSiteMustBeSecure",
                                     "--start-maximized"
                                 ])
context = browser.new_context(no_viewport=True)
context.add_init_script(js)
context = context
page = context.new_page()
def parse_ah(ah):
    match_obj = re.match(r'.+(\d{4}).+[\u4e00-\u9fa5]+(\d+)([\u4e00-\u9fa5]+)(\d+)号', ah, re.M | re.I)
    nd = match_obj.group(1)
    fy = match_obj.group(2)
    lx = match_obj.group(3)
    ah = match_obj.group(4)
    # print(nd, fy, lx, ah)
    return nd, fy, lx, ah
def get_payload(self, *, case_no, case_statu, case_type, year):
    _type = {
        "在办": {"r_zb": "1", "r_bj": "0", "r_ja": "0", "r_td": "0", "r_gd": "0"},
        "报结": {"r_zb": "1", "r_bj": "0", "r_ja": "0", "r_td": "0", "r_gd": "0"},
        "结案": {"r_zb": "1", "r_bj": "0", "r_ja": "0", "r_td": "0", "r_gd": "0"},
        "提档": {"r_zb": "1", "r_bj": "0", "r_ja": "0", "r_td": "0", "r_gd": "0"},
        "归档": {"r_zb": "1", "r_bj": "0", "r_ja": "0", "r_td": "0", "r_gd": "0"},
        "全部": {"r_zb": "1", "r_bj": "1", "r_ja": "1", "r_td": "1", "r_gd": "1"}
    }
    _case_type = {
        "执保": "57",
        "执": "51",
        "执恢": "58",
    }
    _data = {
        "cxdj": "base", "ajdz": _case_type[case_type], "myjs": "ZXXT_AJCBR", "xh": case_no,
        "nndd": year,
        "start": "0", "lilit": "100"
    }
    _data.update(_type[case_statu])
    return _data
def get_fydm_ahdm(self, *, cookie, ah, case_status):
    url = 'http://142.2.248.240:8039/zxxt/webapp/ajgl/cxtj/getDzajGrid.do'
    nd, fy, lx, _ah = parse_ah(ah)
    payload = self.get_payload(case_no=_ah, case_statu=case_status, case_type=lx, year=nd)
    header = {
        'Cookie': cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/79.0.3945.117 Safari/537.36",
    }
    rep = requests.post(url, headers=header, data=payload)
    xml = rep.text
    ss = xml.replace('<?xml version="1.0" encoding="UTF-8"?>', "")
    xml = etree.fromstring(ss)
    rows = xml.xpath('//row')
    if not rows:
        raise Exception("获取接口失败")
    for row in rows:
        userdata = row.xpath("userdata")
        ahdm = userdata[0].text
        _ah = userdata[2].text
        if ah.strip() != _ah.strip():
            raise Exception("接口案号对比失败")
        ajzt = userdata[4].text
        ajlx = userdata[6].text
        xjztlx = userdata[6].text
        return ahdm, ajzt, ajlx, xjztlx



ahdm, ajzt, ajlx, xjztlx = self.get_fydm_ahdm(cookie=self.cookie, ah=self.item["执保案号"], case_status="全部")
wlck_url = f"http://142.2.248.240:8039/zxxt/redirectUrl.do?gndm=ZX397001&yydm=&ahdm={ahdm}&hdid=3531&ajlx={ajlx}&ajzt={ajzt}&xtajlx={xjztlx}&target=progressFrame&ly=ga&screenWidth=1920 "
time.sleep(3)
self.page.goto(wlck_url)




#
# with sync_playwright() as playwright:
#     browser = playwright.chromium.launch(headless=False)
#     default_context = browser.new_context()
#     # default_context = browser.contexts[0]
#     page = default_context.new_page()
#     # page = default_context.new_page()
#     page.goto("https://www.baidu.com")
#     page.locator('[value="百度一下"]').wait_for()
#     page.locator('[value="百度一下"]').wait_for()
#     page.locator('[value="百度一下"]').wait_for()
#     page.locator('[value="百度一下"]').wait_for()
#     page.locator('[value="百度一下"]').wait_for()
#     page.query_selector('[value="百度一下"]')

