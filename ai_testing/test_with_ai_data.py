import pytest,requests,json

BASE_URL = "http://localhost:3000"

# 读取 AI 生成的邮箱测试数据
with open("generated_emails.json","r",encoding="utf-8") as f:
    email_data = json.load(f)

#用 AI 生成的无效邮箱列表作为参数化数据
invalid_emails = email_data["invalid"]

@pytest.mark.parametrize("invalid_email", invalid_emails)
def test_register_invalid_email(invalid_email):
    """使用 AI 生成的无效邮箱进行测试"""
    requests.post(f"{BASE_URL}/reset")
    payload = {"email": invalid_email, "password": "123456"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 400
    assert "Invalid email format" in response.json()["error"]