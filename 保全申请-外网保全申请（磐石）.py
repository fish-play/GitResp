import time

from playwright.sync_api import Playwright, sync_playwright
playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
context = browser.new_context(no_viewport=True)
page = context.new_page()
page.goto('https://www.runoob.com/')
page.get_by_role("link", name="【学习 HTML】 html HTML，即超文本标记语言（Hyper Text Markup Language）").click()
page.get_by_role("textbox", name="搜索……").click()
page.locator('//*[@id="s"]').fill("正则")
with page.expect_popup() as page1_info:
    page.locator('//*[@id="s"]').press("Enter")
page1 = page1_info.value
with page1.expect_popup() as page2_info:
    page1.get_by_role("link", name="Python 正则表达式").click()
page2 = page2_info.value
# page.get_by_role("textbox", name="搜索……").fill("send")
# with page.expect_popup() as page1_info:
#     page.get_by_role("textbox", name="搜索……").press("Enter")
# page1 = page1_info.value
# page1.get_by_placeholder("搜索..").click()
# page1.get_by_placeholder("搜索..").press("Control+a")
# page1.get_by_placeholder("搜索..").fill("")

page.pause()