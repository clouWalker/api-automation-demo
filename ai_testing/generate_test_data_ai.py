import os,json
from xmlrpc import client

from click import prompt
from openai import OpenAI
from dotenv import load_dotenv

#加载.env中的环境变量
load_dotenv()   #读取.env文件中的token

token = os.environ.get("GITHUB_TOKEN")
if not token:
    raise ValueError("未找到 GITHUB_TOKEN，请检查 .env文件")

#初始化客户端（指向 Github Models）
#OpenAI(base_url=...,api_key=...)连接到Github Models服务
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=token,
)

#函数，接受类型和数量，返回JSON
def generate_test_data(data_type:str,count:int = 5):
    """
    调用AI生成制定类型的测试数据
    data_type: 'email','phone','address','name'
    """

    #prompt 高速AI我们要什么格式的数据
    prompt = f"""
    你是一个测试工程师。请生成{count}个有效的{data_type}和{count}个无效的{data_type}。
    用 JSON 格式返回，格式如下：
    {{
        "valid": ["值1","值2",...],
        "invalid":["值1","值2",...]
    }}
    只输出 JSON，不要有其他解释。
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system","content":"你是一个资深的测试工程师。"},
            {"role":"user","content":prompt}
        ],
        temperature=0.7,
        max_tokens=1000,
    )

    result = response.choices[0].message.content
    # 提取 JSON (处理可能被markdown包裹的情况)
    if "```json" in result:
        result = result.split("```json")[1].split("```")[0]
    elif "```" in result:
        result = result.split("```")[1].split("```")[0]

    #json.loads()把AI返回的字符串变成Python字典
    return json.loads(result.strip())

if __name__ == "__main__":
    # 生成邮箱测试数据
    email_data = generate_test_data("email",3)
    print("邮箱测试数据：")
    print(json.dumps(email_data, indent=2,ensure_ascii=False))

    #保存到文件，供测试用例使用
    with open("generated_emails.json","w",encoding="utf-8") as f:
        json.dump(email_data,f,indent=2,ensure_ascii=False)
    print("\n已保存到 generated_emails.json")

    #生成手机号测试数据
    phone_data = generate_test_data("phone",3)
    print("\n手机号测试数据：")
    print(json.dumps(phone_data, indent=2,ensure_ascii=False))
    with open("generated_phones.json","w",encoding="utf-8") as f:
        json.dump(phone_data,f,indent=2,ensure_ascii=False)
    print("\n已保存到 generated_phones.json")

