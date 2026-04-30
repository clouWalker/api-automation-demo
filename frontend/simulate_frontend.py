#此脚本不需要真实浏览器浏览，直接发送 POST 请求，模拟了前端“点击注册按钮”时发出的网络请求,requests模拟脚本
import requests


# 普通for循环执行测试，需要在终端执行python simulate_frontend.py -v命令
BASE_URL = "http://localhost:3000"
def simulate_register(email, password):
    url = f"{BASE_URL}/users"
    payload = {"email": email, "password": password}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 201:
            print("✅ 注册成功！用户ID：", response.json()["id"])
        else:
            print("❌ 注册失败，状态码：", response.status_code)
            print("错误信息：", response.json().get("error"))
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保 mock_server.py 正在运行")

test_cases = [
    ("valid@test.com", "123456", True),
    ("invalid-email", "123456", False),
    ("valid2@test.com", "123", False),   # 密码太短
]

for email, pwd, should_succeed in test_cases:
    simulate_register(email, pwd)


if __name__ == "__main__":
    simulate_register("test@example.com", "123456")
    simulate_register("invalid-email", "123456")  # 故意错误

