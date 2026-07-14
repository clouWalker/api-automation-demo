import requests,pytest,json,os

#json-server --watch db,json.json --port 3000。 json-server并不是模拟真实服务器，有局限性，用mock服务器模拟更好
# 你的私有API就运行在 http://localhost:3000 上了。

#1.确保 mock服务器 已经在终端中启动并运行python mock_server.py
Base_url="http://localhost:3000"

# 合法手机号，用于需要注册成功的用例
VALID_PHONE = "13800138000"

# 尝试读取AI生成的测试数据，如果文件不存在则使用默认数据
test_data_file = "generated_test_data.json"
if os.path.exists(test_data_file):
    with open(test_data_file) as f:
        test_data = json.load(f)
    invalid_emails = test_data.get("invalid", [])
else:
    # 备用默认数据（与原硬编码一致）
    invalid_emails = ["abc", "abc@", "@example.com", "a@b", "user@.com"]


def test_register_success():
    """测试用例1：验证用户注册功能
    # 测试正常注册（邮箱格式正确，密码长度足够，邮箱未注册过）
    # 你应该每次使用不同的邮箱，避免冲突，例如 "test1@example.com" """
    requests.post(f"{Base_url}/reset")    #清空数据

    url = f"{Base_url}/users"
    payload = {
        "email":"test01@example.com",
        "password":"123456",
        "phone": VALID_PHONE
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

def test_register_short_password():
    """测试用例4：密码长度小于 6，期望 400，错误信息包含 "Password too short" """
    requests.post(f"{Base_url}/reset")  # 清空数据
    url = f"{Base_url}/users"
    payload = {
        #密码长度小于6
        "email": "eve.holt@reqres.in",
        "password": "pass",
        "phone": VALID_PHONE
    }
    response = requests.post(url, json=payload)

    assert response.status_code == 400, f"期望状态码400，实际为{response.status_code}"
    data = response.json()
    assert "error" in data, "响应中缺少错误信息"
    assert "Password too short" in data["error"], "错误信息不符合预期"

def test_register_missing_phone():
    """测试用例：缺少 phone 字段，期望 400，错误信息包含 "Missing phone" """
    requests.post(f"{Base_url}/reset")
    url = f"{Base_url}/users"
    payload = {
        "email": "nophone@example.com",
        "password": "123456"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 400
    assert "Missing phone" in response.json()["error"]


def test_register_invalid_phone():
    """测试用例：手机号格式非法，期望 400，错误信息包含 "Invalid phone number" """
    requests.post(f"{Base_url}/reset")
    url = f"{Base_url}/users"
    payload = {
        "email": "badphone@example.com",
        "password": "123456",
        "phone": "12345"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 400
    assert "Invalid phone number" in response.json()["error"]


def test_register_duplicate_email():
    """测试用例5：先注册一个邮箱，再用同一个邮箱再次注册，期望 409，错误信息包含 "Email already registered" """
    requests.post(f"{Base_url}/reset")
    
    url = f"{Base_url}/users"
    payload = {
        "email": "duplicate@example.com",
        "password": "password",
        "phone": VALID_PHONE
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
            "password": "123456",
            "phone": f"1380000000{i}"
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


def test_delete_user_success():
    """先创建一个用户，然后删除它，断言删除成功，且再次获取用户列表时不再包含该用户"""
    requests.post(f"{Base_url}/reset")
    # 1. 创建用户
    create_resp = requests.post(f"{Base_url}/users", json={"email": "delete@example.com", "password": "123456", "phone": VALID_PHONE})
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    # 2. 删除用户
    delete_resp = requests.delete(f"{Base_url}/users/{user_id}")
    assert delete_resp.status_code == 200
    assert "deleted" in delete_resp.json()["message"]

    # 3. 验证用户已从列表中消失
    get_resp = requests.get(f"{Base_url}/users")
    assert get_resp.status_code == 200
    data = get_resp.json()
    users_list = data.get("data", [])  # 修正点
    assert not any(u["id"] == user_id for u in users_list)


def test_delete_user_not_found():
    """删除一个不存在的用户ID，期望返回404"""
    requests.post(f"{Base_url}/reset")
    delete_resp = requests.delete(f"{Base_url}/users/999")
    assert delete_resp.status_code == 404
    assert "User not found" in delete_resp.json()["error"]


def test_update_user_success():
    """正常更新用户邮箱"""
    requests.post(f"{Base_url}/reset")
    # 创建用户
    create_resp = requests.post(f"{Base_url}/users", json={"email": "old@example.com", "password": "123456", "phone": VALID_PHONE})
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    # 更新邮箱
    new_email = "new@example.com"
    update_resp = requests.put(f"{Base_url}/users/{user_id}", json={"email": new_email})
    assert update_resp.status_code == 200
    assert update_resp.json()["email"] == new_email

    # 验证 GET 用户列表中的邮箱已更新
    get_resp = requests.get(f"{Base_url}/users")
    users_list = get_resp.json().get("data", [])
    updated_user = next((u for u in users_list if u["id"] == user_id), None)
    assert updated_user is not None
    assert updated_user["email"] == new_email


def test_update_user_not_found():
    """更新不存在的用户ID → 404"""
    requests.post(f"{Base_url}/reset")
    update_resp = requests.put(f"{Base_url}/users/999", json={"email": "any@example.com"})
    assert update_resp.status_code == 404
    assert "User not found" in update_resp.json()["error"]


def test_update_user_invalid_email():
    """新邮箱格式错误 → 400"""
    requests.post(f"{Base_url}/reset")
    create_resp = requests.post(f"{Base_url}/users", json={"email": "valid@example.com", "password": "123456", "phone": VALID_PHONE})
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    update_resp = requests.put(f"{Base_url}/users/{user_id}", json={"email": "invalid-email"})
    assert update_resp.status_code == 400
    assert "Invalid email format" in update_resp.json()["error"]


def test_update_user_email_conflict():
    """新邮箱已被其他用户占用 → 409"""
    requests.post(f"{Base_url}/reset")
    # 创建两个用户
    resp1 = requests.post(f"{Base_url}/users", json={"email": "first@example.com", "password": "123456", "phone": VALID_PHONE})
    resp2 = requests.post(f"{Base_url}/users", json={"email": "second@example.com", "password": "123456", "phone": "13900139000"})
    assert resp1.status_code == 201
    assert resp2.status_code == 201
    user1_id = resp1.json()["id"]
    user2_email = resp2.json()["email"]  # "second@example.com"

    # 尝试将 user1 的邮箱改为 user2 的邮箱
    update_resp = requests.put(f"{Base_url}/users/{user1_id}", json={"email": user2_email})
    assert update_resp.status_code == 409
    assert "Email already registered" in update_resp.json()["error"]

# def test_register_invalid_email():      #旧方法只能一个一个试，新的方法可以直接将不合法的邮箱格式写入pytest中
#     """测试用例3：邮箱不含 @，期望 400，错误信息包含 "Invalid email format" """
#     requests.post(f"{Base_url}/reset")  # 清空数据
#
#     url = f"{Base_url}/users"
#     payload = {
#         #邮箱中故意不包含@
#         "email": "eve.holtreqres.in",
#         "password": "pistol1"
#     }
#     response = requests.post(url, json=payload)
#
#     assert response.status_code == 400, f"期望状态码400，实际为{response.status_code}"
#     data = response.json()
#     assert "error" in data, "响应中缺少错误信息"
#     assert "Invalid email format" in data["error"], "错误信息不符合预期"

#原本手动写入多种无效测试用例
# @pytest.mark.parametrize("invalid_email", [
#     "abc",                # 无@
#     "abc@",               # @后无内容
#     "@example.com",       # 无用户名
#     "a@b",                # 域名无点
#     "user@.com",          # 点开头
# ])

#引入AI后，自动读取不合法的邮箱格式
@pytest.mark.parametrize("invalid_email", invalid_emails)

def test_register_invalid_email_multiple(invalid_email):
    """参数化测试多种无效邮箱格式"""
    requests.post(f"{Base_url}/reset")
    payload = {"email": invalid_email, "password": "123456"}
    response = requests.post(f"{Base_url}/users", json=payload)
    assert response.status_code == 400
    assert "Invalid email format" in response.json()["error"]


@pytest.fixture(scope="function", autouse=True)
def reset_data():
    """Reset the data before each test."""
    requests.post(f"{Base_url}/reset")


# Test POST /users
def test_post_users_success():
    """Test successful user registration."""
    payload = {"email": "test@example.com", "password": "password123", "phone": VALID_PHONE}
    response = requests.post(f"{Base_url}/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == payload["email"]


def test_post_users_missing_email():
    """Test user registration with missing email."""
    payload = {"password": "password123"}
    response = requests.post(f"{Base_url}/users", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Missing email"


def test_post_users_missing_password():
    """Test user registration with missing password."""
    payload = {"email": "test@example.com"}
    response = requests.post(f"{Base_url}/users", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Missing password"


def test_post_users_invalid_email_format():
    """Test user registration with invalid email format."""
    payload = {"email": "invalidemail", "password": "password123"}
    response = requests.post(f"{Base_url}/users", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Invalid email format"


def test_post_users_short_password():
    """Test user registration with short password."""
    payload = {"email": "test@example.com", "password": "123", "phone": VALID_PHONE}
    response = requests.post(f"{Base_url}/users", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Password too short,minimum 6 characters"


def test_post_users_email_already_registered():
    """Test user registration with an already registered email."""
    payload = {"email": "test@example.com", "password": "password123", "phone": VALID_PHONE}
    # First registration
    response = requests.post(f"{Base_url}/users", json=payload)
    assert response.status_code == 201
    # Second registration with the same email
    response = requests.post(f"{Base_url}/users", json=payload)
    assert response.status_code == 409
    data = response.json()
    assert data["error"] == "Email already registered"


# Test GET /users
def test_get_users_success():
    """Test successful retrieval of user list."""
    # Create some users
    users = [
        {"email": "user1@example.com", "password": "password123", "phone": VALID_PHONE},
        {"email": "user2@example.com", "password": "password123", "phone": "13900000001"},
    ]
    for user in users:
        requests.post(f"{Base_url}/users", json=user)

    # Retrieve users
    response = requests.get(f"{Base_url}/users")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "data" in data
    assert len(data["data"]) == len(users)
    for user in data["data"]:
        assert "id" in user
        assert "email" in user


def test_get_users_pagination():
    """Test user list pagination."""
    # Create 15 users
    for i in range(15):
        requests.post(f"{Base_url}/users", json={"email": f"user{i}@example.com", "password": "password123", "phone": f"137000000{i:02d}"})

    # Retrieve first page with default limit
    response = requests.get(f"{Base_url}/users", params={"page": 1, "limit": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["limit"] == 10
    assert len(data["data"]) == 10

    # Retrieve second page
    response = requests.get(f"{Base_url}/users", params={"page": 2, "limit": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert data["limit"] == 10
    assert len(data["data"]) == 5


