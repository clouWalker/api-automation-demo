import pytest,requests,json

BASE_URL = "http://localhost:3000"

# 读取 AI 生成的手机号数据
with open("generated_phones.json","r",encoding="utf-8") as f:
    phone_data = json.load(f)

valid_phones = phone_data["valid"]
invalid_phones = phone_data["invalid"]

#用 AI 生成的有效手机号测试正常注册
@pytest.mark.parametrize("phone",valid_phones)
def test_register_with_valid_phone(phone):
    requests.post(f"{BASE_URL}/reset")
    payload = {
        "email": f"user_{phone}@test.com",
        "phone": phone,
        "password": "123456"
    }
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["phone"] == phone

# 用 AI 生成的无效手机号测试异常场景
@pytest.mark.parametrize("phone",invalid_phones)
def test_register_with_invalid_phone(phone):
    requests.post(f"{BASE_URL}/reset")
    payload = {
        "email": f"user_{phone}@test.com",
        "phone": phone,
        "password": "123456"
    }
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 400
    assert "Invalid phone number" in response.json()["error"]