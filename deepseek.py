import os
import requests

# os.environ['DEEPSEEK_API_KEY'] = 'sk-ML3aIfbBf8MFnnQFdBOVcbdqRvkZ1qoqm2ttOSofQTJFO6LO'

def deepseek_chat(query: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("请先设置环境变量 DEEPSEEK_API_KEY")
    url = "https://api.chatanywhere.tech/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-v3",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data['choices'][0]['message']['content']

def summarize_and_rank_papers(question, papers):
    # 拼接 prompt
    context = "\n\n".join(
        [f"Title: {p['title']}\nAuthors: {p['authors']}\nPublished: {p['published']}\nSummary: {p['summary']}" 
         for p in papers]
    )
    prompt = (
        f"用户问题：{question}\n\n"
        "以下是与问题相关的arXiv论文，请根据论文质量、相关性和新颖性对它们进行排序，"
        "并给出简要总结。输出每篇论文的排序、标题、总结、一句话推荐理由。\n\n"
        f"{context}"
    )
    return deepseek_chat(prompt)

# 示例用法
if __name__ == "__main__":
    # 需要先设置环境变量：export DEEPSEEK_API_KEY=sk-xxx
    print(deepseek_chat("Hello!"))