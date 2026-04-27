import requests,pytest
from playwright.sync_api import sync_playwright
#参数化测试（纯API层）

BASE_URL = "http://localhost:3000"

#测试数据：邮箱、密码、期望包含的成功/失败关键字
test_data = [
    ("success@test.com","123456","成功"),             #正常注册
    ("invalid-email","123456","Invalid email"),      #邮箱格式错误
    ("short@test.com","123","Password too short"),   #密码太短
    ("dup@test.com","123456","成功"),                 #第一次注册成功
]
@pytest.mark.parametrize("email,password,expected_msg", test_data)
def test_register(email,password,expected_msg):
    # 每个用例前清空数据，保证重复注册测试不受前面用例影响
    requests.post(f"{BASE_URL}/reset")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge",headless=False)
        page = browser.new_page()
        page.goto("file:///E:/Study/Pycharm_study/api-test-practice/frontend/register.html")

        page.fill("#email",email)
        page.fill("#password",password)
        page.click("#registerBtn")

        # 等待消息出现
        page.wait_for_selector("#message")
        message = page.inner_text("#message")

        # 断言页面消息包含预期的关键字
        assert expected_msg in message

        browser.close()

def test_register_duplicate():
    #1.先清理数据，然后注册一次
    requests.post(f"{BASE_URL}/reset")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge",headless=False)
        page = browser.new_page()
        page.goto("file:///E:/Study/Pycharm_study/api-test-practice/frontend/register.html")

        page.fill("#email","dup@test.com")
        page.fill("#password","123456")
        page.click("#registerBtn")
        page.wait_for_selector("#message")
        fist_msg = page.inner_text("#message")
        assert "成功" in fist_msg

        #2.不关闭浏览器，直接再次点击注册按钮（第二次注册）
        #但如果页面没有清空表单，需要重新填写（这里简化：重新加载页面）
        page.goto("file:///E:/Study/Pycharm_study/api-test-practice/frontend/register.html")
        page.fill("#email", "dup@test.com")
        page.fill("#password", "123456")
        page.click("#registerBtn")
        page.wait_for_selector("#message")
        second_msg = page.inner_text("#message")
        assert "already registered" in second_msg
        browser.close()

'''
#pytest参数化测试代码
@pytest.mark.parametrize("email,password,expected_msg", [
    ("param@test.com", "123456",201, None),
    ("invalid-email", "123456",400, "Invalid email format"),
    ("short@test.com", "123",400, "Password too short,minimum 6 characters"),
])
def test_register_param(email,password,expected_status,expected_error):
    #每个测试前清空数据（确保重复注册不会误判）
    requests.post(f"{BASE_URL}/reset")

    url = f"{BASE_URL}/users"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload)

    assert response.status_code == expected_status
    if expected_error:
        assert expected_error in response.json()["error"]
    else:
        assert "id" in response.json()
'''