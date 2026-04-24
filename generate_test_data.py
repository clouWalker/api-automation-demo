from openai import OpenAI
import json

# 替换成你的真实 API Key(deepseek的API，需要缴费)
API_KEY = "sk-7bb7e9534e444f5f84ee90ed3788c43b"

client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

try:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system",
             "content": "你是一个测试工程师，请生成5个有效的邮箱地址和5个无效的邮箱地址，用JSON格式返回，格式：{\"valid\": [\"...\"], \"invalid\": [\"...\"]}"},
            {"role": "user", "content": "生成测试数据"}
        ],
        temperature=0.7
    )

    result = response.choices[0].message.content
    print("原始返回：", result)

    # 尝试解析 JSON
    try:
        data = json.loads(result)
        print("有效的邮箱：", data.get("valid", []))
        print("无效的邮箱：", data.get("invalid", []))
    except json.JSONDecodeError:
        print("返回内容不是标准 JSON，请检查提示词")

except Exception as e:
    print("请求出错：", e)