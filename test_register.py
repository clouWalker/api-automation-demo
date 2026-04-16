import requests
#json-server --watch db,json.json --port 3000。 json-server并不是模拟真实服务器，有局限性，用mock服务器模拟更好
# 你的私有API就运行在 http://localhost:3000 上了。

#1.确保 mock服务器 已经在终端中启动并运行python mock_server.py
Base_url="http://localhost:3000"

def test_register_success():
    """测试用例1：验证用户注册功能
    # 测试正常注册（邮箱格式正确，密码长度足够，邮箱未注册过）
    # 你应该每次使用不同的邮箱，避免冲突，例如 "test1@example.com" """
    requests.post(f"{Base_url}/reset")    #清空数据

    url = f"{Base_url}/users"
    payload = {
        "email":"test01@example.com",
        "password":"123456"
    }

    response = requests.post(url,json=payload)

    #断言状态码为 201，Created（成功创建资源的标志）
    assert response.status_code == 201,f"期望状态码201，实际为{response.status_code}"

    #解析 JSON响应
    data = response.json()

    #断言 data 中包含id字段，并且不为空
    assert "id" in data,"响应中缺少”id“字段"
    assert data["id"] is not None,"用户ID为空"
    print(f"用户注册成功，新用户ID为:{data['id']}")

def test_register_missing_email():
    """测试用例1：缺少 email 字段，期望 400，错误信息包含 "Missing email" """
    requests.post(f"{Base_url}/reset")  # 清空数据

    url = f"{Base_url}/users"
    payload = {
        # 故意不包含 email 字段
        "password": "pistol"
    }
    response = requests.post(url, json=payload)

    # JSON Server 在这种情况下仍会创建用户，但实际项目中通常会返回 400 错误。
    # 这里我们模拟真实项目，期望返回 400 并包含错误信息。
    assert response.status_code == 400, f"期望状态码400，实际为{response.status_code}"
    data = response.json()
    assert "error" in data, "响应中缺少错误信息"
    assert "Missing email" in data["error"], "错误信息不符合预期"


def test_register_missing_password():
    """测试用例2：验证注册时缺少密码字段的错误处理"""
    requests.post(f"{Base_url}/reset")  # 清空数据

    url = f"{Base_url}/users"
    payload = {
        "email": "eve.holt@reqres.in"
        # 故意不包含 password 字段
    }
    response = requests.post(url, json=payload)

    # JSON Server 在这种情况下仍会创建用户，但实际项目中通常会返回 400 错误。
    # 这里我们模拟真实项目，期望返回 400 并包含错误信息。
    assert response.status_code == 400, f"期望状态码400，实际为{response.status_code}"
    data = response.json()
    assert "error" in data, "响应中缺少错误信息"
    assert "Missing password" in data["error"], "错误信息不符合预期"

def test_register_invalid_email():
    """测试用例3：邮箱不含 @，期望 400，错误信息包含 "Invalid email format" """
    requests.post(f"{Base_url}/reset")  # 清空数据

    url = f"{Base_url}/users"
    payload = {
        #邮箱中故意不包含@
        "email": "eve.holtreqres.in",
        "password": "pistol1"
    }
    response = requests.post(url, json=payload)

    assert response.status_code == 400, f"期望状态码400，实际为{response.status_code}"
    data = response.json()
    assert "error" in data, "响应中缺少错误信息"
    assert "Invalid email format" in data["error"], "错误信息不符合预期"

def test_register_short_password():
    """测试用例4：密码长度小于 6，期望 400，错误信息包含 "Password too short" """
    requests.post(f"{Base_url}/reset")  # 清空数据
    url = f"{Base_url}/users"
    payload = {
        #密码长度小于6
        "email": "eve.holt@reqres.in",
        "password": "pass"
    }
    response = requests.post(url, json=payload)

    assert response.status_code == 400, f"期望状态码400，实际为{response.status_code}"
    data = response.json()
    assert "error" in data, "响应中缺少错误信息"
    assert "Password too short" in data["error"], "错误信息不符合预期"

def test_register_duplicate_email():
    """测试用例5：先注册一个邮箱，再用同一个邮箱再次注册，期望 409，错误信息包含 "Email already registered" """
    requests.post(f"{Base_url}/reset")
    
    url = f"{Base_url}/users"
    payload = {
        # 密码长度小于6
        "email": "duplicate@example.com",
        "password": "password"
    }
    # 第一次注册，应该成功
    response1 = requests.post(url, json=payload)
    assert response1.status_code == 201

    # 第二次注册相同邮箱，应该失败
    response2 = requests.post(url, json=payload)
    assert response2.status_code == 409
    data = response2.json()
    assert "error" in data
    assert "Email already registered" in data["error"]

def test_get_users():
    # 先清空数据
    requests.post(f"{Base_url}/reset")

    #注册3个不同用户（准备数据）
    for i in range(1,4):
        payload = {
            "email": f"user{i}@example.com",
            "password": "123456"
        }
        resp = requests.post(f"{Base_url}/users", json=payload)
        assert resp.status_code == 201

    #测试1：获取所有用户（不分页，使用默认limit=10）
    response = requests.get(f"{Base_url}/users")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["data"]) == 3
    assert data["page"] == 1

    #测试2：分页获取，每页2条
    response = requests.get(f"{Base_url}/users?page=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["data"]) == 2
    assert data["page"] == 1
    assert data["limit"] == 2

    #测试3：超出范围的页码，应返回空列表
    response = requests.get(f"{Base_url}/users?page=10&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 0
    assert data["total"] == 3

