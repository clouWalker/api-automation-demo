# 1. 导入 Flask 相关的模块
from flask import Flask, request, jsonify

# 2. 创建一个 Flask 应用实例
app = Flask(__name__)

# 3. 模拟一个数据库（用 Python 列表存储用户数据）
users = []


# 4. 定义一个路由：当客户端发送 POST 请求到 /users 时，执行下面的函数
@app.route('/users', methods=['POST'])
def register():
    # 4.1 获取客户端发送的 JSON 数据，并转换成 Python 字典
    data = request.get_json()

    # 4.2 校验：如果没有 email 字段,
    if not data.get('email'):
        # 返回 JSON 格式的错误信息，状态码 400（Bad Request）
        return jsonify({"error": "Missing email"}), 400

    # 4.3 校验：如果没有 password 字段
    if not data.get('password'):
        return jsonify({"error": "Missing password"}), 400
    
    email = data['email']
    password = data['password']

    # 4.7 校验：“邮箱格式校验（必须包含@）"
    if "@" not in email:
        return jsonify({"error": "Invalid email format"}), 400
        
    # 4.8 校验：密码长度（至少6位）
    if len(password) < 6:
        return jsonify({"error": "Password too short,minimum 6 characters"}), 400
    
    # 4.9 校验：邮箱是否已被注册
    for user in users:
        if user["email"] == email:
            return jsonify({"error": "Email already registered"}), 409

    # 4.4 校验通过，创建新用户（模拟保存到数据库）
    new_user = {
        "id": len(users) + 1,  # 自动生成 ID
        "email": email  # 只存储邮箱，不存密码（真实项目也不会存明文密码）
    }
    
    users.append(new_user)  # 添加到列表中
    # 4.5 返回新用户信息，状态码 201（Created）
    return jsonify(new_user), 201

@app.route('/reset', methods=['POST'])
def reset():
    users.clear()
    return jsonify({"message": "reset success"}), 200

@app.route('/users', methods=['GET'])
def get_users():
    # 获取查询参数 ?page=1&limit=2(可选）
    page = request.args.get('page', default=1, type=int)    #request.args.get() 获取 URL 参数，如 /users?page=2&limit=5
    limit = request.args.get('limit', default=10, type=int)

    # 计算分页起始索引
    start = (page - 1) * limit
    end = start + limit

    # 切片获取当前页数据
    pagination_users = users[start:end]

    #返回总记录数、当前页、每页条数、用户列表
    return jsonify({
        "total": len(users),
        "page" : page,
        "limit" : limit,
        "data" : pagination_users
    }),200

#<int:user_id>表示URL路径中的参数，例如DELETE/users/2 会删除id为2的用户
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # 查找用户是否存在
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return jsonify({"message": f"User {user_id} deleted"}), 200
    # 未找到用户
    return jsonify({"error": "User not found"}), 404


# 5. 启动服务器（如果直接运行这个脚本）
if __name__ == '__main__':
    app.run(port=3000)  # 监听本机的 3000 端口