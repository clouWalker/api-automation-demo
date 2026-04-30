import pytest,requests,time
from playwright.sync_api import sync_playwright
from pytest_playwright.pytest_playwright import browser

BASE_URL = "http://localhost:3000"


def test_register_success():
    # 先清理服务器数据，避免重复注册冲突
    requests.post(f"{BASE_URL}/reset")

    with sync_playwright() as p:     # 进入上下文
        browser = p.chromium.launch(channel="msedge", headless=False)
        # ... 执行操作 ...
        # 即使这里没有 browser.close()
        # 退出 with 块时，Playwright 会自动关闭浏览器和所有相关进程

        page = browser.new_page()
        page.goto("file:///E:/Study/Pycharm_study/api-test-practice/frontend/register.html")

        # 也可以不用清除数据，使用动态邮箱，导入time库
        # email = f"test_{int(time.time())}@playwright.com"

        page.fill("#email", "test@playwright.com")
        page.fill("#password", "123456")
        page.click("#registerBtn")

        page.wait_for_selector("#message")
        message = page.inner_text("#message")
        assert "成功" in message

        # 暂停，直到你按回车
        input("按回车键关闭浏览器...")
        # 此时浏览器会保持打开，直到你按回车
    # 退出 with 块后浏览器关闭
