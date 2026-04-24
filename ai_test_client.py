# 1. 导入必要的模块
import os                     # 用于读取环境变量
from openai import OpenAI     # OpenAI 官方库，兼容 GitHub Models
from dotenv import load_dotenv # 用于加载 .env 文件

# 2. 加载 .env 文件中的变量
# 这样就能把 GITHUB_TOKEN 读到系统的环境变量中
load_dotenv()

# 3. 从环境变量中获取令牌（github自己的key，免费）
token = os.environ.get("GITHUB_TOKEN")

# 4. 检查令牌是否成功读取（如果为空，说明 .env 配置有问题）
if not token:
    raise ValueError("未找到 GITHUB_TOKEN，请检查 .env 文件")

# 5. 初始化 OpenAI 客户端，指向 GitHub Models 的端点
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",  # GitHub Models 固定地址
    api_key=token,                                     # 使用我们生成的令牌
)

# 6. 调用聊天补全接口
response = client.chat.completions.create(
    model="gpt-4o",  # 使用的模型，你也可以换成 "gpt-4o-mini" 或 "DeepSeek-R1"
    messages=[
        {
            "role": "system",
            "content": "你是一个资深的测试工程师。请生成5个有效的邮箱地址和5个无效的邮箱地址。用JSON格式返回，格式为：{\"valid\": [\"...\"], \"invalid\": [\"...\"]}。不要输出其他解释文字。"
        },
        {
            "role": "user",
            "content": "帮我生成一些用于邮箱格式校验的测试数据。"
        }
    ],
    temperature=0.7,    # 控制创造性，0.7 比较适中
    max_tokens=500,     # 限制返回的 token 数量，节约额度（虽然免费但有速率限制）
)

# 7. 获取 AI 返回的内容
result = response.choices[0].message.content

# 8. 打印结果
print("AI 返回的原始内容：")
print(result)

# 9. 可选：尝试解析 JSON，看看格式是否正确
import json
import re

result = response.choices[0].message.content
print("AI 返回的原始内容：")
print(result)

# 尝试提取 ```json ... ``` 内的内容
json_match = re.search(r'```json\s*(\{.*?\})\s*```', result, re.DOTALL)
if json_match:
    json_str = json_match.group(1)
else:
    # 如果没有代码块，尝试直接解析（防止某些模型不包装）
    json_str = result

try:
    data = json.loads(json_str)
    print("\n解析成功！有效邮箱列表：", data.get("valid", []))
    print("无效邮箱列表：", data.get("invalid", []))

    # 保存到文件，供测试使用
    with open("generated_test_data.json", "w") as f:
        json.dump(data, f, indent=2)
    print("测试数据已保存到 generated_test_data.json")

except json.JSONDecodeError as e:
    print("\n解析 JSON 失败，请检查返回内容。错误：", e)


#将结果保存到一个json文件，测试用例读取它
with open("generated_test_data.json", "w") as f:
    json.dump(data, f, indent=2)
print("测试数据已保存到 generated_test_data.json")