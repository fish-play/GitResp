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




with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    default_context = browser.new_context()
    # default_context = browser.contexts[0]
    page = default_context.new_page()
    # page = default_context.new_page()
    page.goto("https://www.baidu.com")
    page.locator('[value="百度一下"]').wait_for()
    page.locator('[value="百度一下"]').wait_for()
    page.locator('[value="百度一下"]').wait_for()
    page.locator('[value="百度一下"]').wait_for()
    page.locator('[value="百度一下"]').wait_for()
    page.query_selector('[value="百度一下"]')

