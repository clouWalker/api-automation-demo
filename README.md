# API + 前端自动化测试实战项目

本项目是一个完整的自动化测试示例，包含：
- Flask Mock 服务器（模拟用户注册 API）
- pytest 接口自动化测试（requests）
- pytest + Playwright 前端自动化测试（模拟真实用户操作）
- GitHub Actions CI 持续集成（自动运行接口测试）

## 项目结构
api-test-practice/ <br>
├── frontend/ <br>
│ ├── register.html # 前端注册页面 <br>
│ ├── test_frontend.py # 单场景前端测试<br>
│ └── test_frontend_param.py # 参数化前端测试 <br>
├── mock_server.py # Flask Mock 后端 <br>
├── test_register.py # 接口自动化测试（含参数化） <br>
├── .github/workflows/ # CI 配置 <br>
├── requirements.txt # 依赖清单 <br>
└── README.md <br>


## 环境准备

1. 安装依赖 
   ```bash
   pip install -r requirements.txt
   playwright install msedge   # 安装 Edge 浏览器驱动

2.启动后端服务（必须）<br>
    python mock_server.py 

## 运行测试

### 接口测试（API层）
    pytest test_register.py -v
    
    
### 前端测试（浏览器自动化）
    cd frontend         
    pytest test_frontend.py -v -s       # 单场景
    pytest test_frontend_param.py -v -s # 参数化+重复注册

## CI持续集成
- 每次推送代码到 GitHub，Actions 会自动运行 test_register.py
- 测试报告可下载查看

## 技术栈
- Python 3.13
- Flask（Mock 服务器） 
- pytest（测试框架） 
- requests（API 测试） 
- Playwright（前端自动化） 
- GitHub Actions（CI）


## 学习收获
- 从零搭建一个完整的测试体系（前端 + 后端） 
- 掌握接口测试、前端自动化测试、参数化测试 
- 解决跨域问题（CORS）
- 使用 Git 管理代码，GitHub Actions 实现 CI
