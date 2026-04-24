# 用户管理 API 文档

## POST /users
- 功能：注册新用户
- 请求体 JSON：{"email": string, "password": string}
- 成功响应：201, {"id": int, "email": string}
- 异常响应：
  - 缺少 email：400, {"error": "Missing email"}
  - 缺少 password：400, {"error": "Missing password"}
  - 邮箱格式无效（不含@或连续点）：400, {"error": "Invalid email format"}
  - 密码长度<6：400, {"error": "Password too short, minimum 6 characters"}
  - 邮箱已存在：409, {"error": "Email already registered"}

## GET /users
- 功能：获取用户列表（分页）
- 查询参数：page (默认1), limit (默认10)
- 成功响应：200, {"total": int, "page": int, "limit": int, "data": [{"id": int, "email": string}]}