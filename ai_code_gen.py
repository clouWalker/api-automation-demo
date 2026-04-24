import os,re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("GITHUB_TOKEN")
if not token:
    raise ValueError("未找到 GITHUB_TOKEN，请检查 .env 文件")

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=token,
)

# 读取接口文档
with open("api_documentation.md", "r", encoding="utf-8") as f:
    api_doc = f.read()

# 提示词：要求 AI 生成 pytest 测试代码
prompt = f"""
根据以下 API 文档，生成完整的 pytest 测试代码。要求：
1. 使用 requests 库发送请求。
2. 每个接口至少包含一个正常场景和一个异常场景的测试函数。
3. 使用断言验证状态码和返回的 JSON 字段。
4. 测试函数命名以 test_ 开头。
5. 假设 base_url = "http://localhost:3000"。
6. 需要包含 /reset 调用来清理数据（在必要时）。
7. 输出只返回 Python 代码，不要有其他解释。

API 文档：
{api_doc}
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "你是一个资深的测试开发工程师，擅长编写高质量的 pytest 测试代码。"},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3,
    max_tokens=2000,
)

generated_code = response.choices[0].message.content

# 提取 Markdown 代码块中的 Python 代码
code_match = re.search(r'```python\n(.*?)\n```', generated_code, re.DOTALL)
if code_match:
    pure_code = code_match.group(1)
else:
    # 如果没有代码块，尝试直接使用（并去掉可能的三反引号）
    pure_code = generated_code.strip('`').strip()

# 保存纯代码
with open("auto_generated_tests.py", "w", encoding="utf-8") as f:
    f.write(pure_code)

print("纯 Python 代码已保存到 auto_generated_tests.py")
