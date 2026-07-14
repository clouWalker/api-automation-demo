# API 接口自动化测试项目

基于 Python + Flask + pytest + requests 的用户注册接口自动化测试项目，包含本地 Mock 服务、接口测试用例与 GitHub Actions 持续集成。

## 技术栈

- Python 3.13+
- Flask / flask-cors（Mock 后端）
- pytest（测试框架）
- requests（HTTP 请求）
- GitHub Actions（CI）

## 项目结构

```
api-test-practice/
├── mock_server.py          # Flask Mock 后端
├── test_register.py        # 接口自动化测试用例
├── requirements.txt        # 依赖清单
├── .github/workflows/      # GitHub Actions CI 配置
└── README.md               # 项目说明
```

## 环境准备

```bash
pip install -r requirements.txt
```

## 运行测试

1. 启动 Mock 服务（需要保持运行）

```bash
python mock_server.py
```

2. 在另一个终端运行接口测试

```bash
pytest test_register.py -v
```

## 测试覆盖

`test_register.py` 共 27 条用例，覆盖：

- 正常注册流程
- 缺少邮箱 / 密码 / 手机号
- 邮箱格式非法（参数化）
- 手机号格式非法
- 密码长度不足
- 邮箱重复注册
- 查询用户列表与分页
- 删除用户（成功 / 用户不存在）
- 更新用户邮箱（成功 / 用户不存在 / 邮箱格式错误 / 邮箱冲突）

## 本次改进

- 修复了原仓库因新增手机号校验导致的大量用例失败
- 补充了手机号缺失、手机号格式非法的异常场景测试
- 将缺失的 `flask-cors` 依赖补入 `requirements.txt`
- CI 改为通过 `requirements.txt` 安装依赖，保证环境一致性

## CI 持续集成

每次 push 到 main 分支，GitHub Actions 会自动：

1. 安装依赖
2. 启动 Mock 服务
3. 运行 `test_register.py`
4. 生成并上传 HTML 测试报告
