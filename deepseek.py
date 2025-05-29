import os
import requests
#$env:DEEPSEEK_API_KEY="sk-ML3aIfbBf8MFnnQFdBOVcbdqRvkZ1qoqm2ttOSofQTJFO6LO"
os.environ['DEEPSEEK_API_KEY'] = 'sk-ML3aIfbBf8MFnnQFdBOVcbdqRvkZ1qoqm2ttOSofQTJFO6LO'

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
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data['choices'][0]['message']['content']

def extract_keywords(natural_question):
    prompt = (
        f"请根据以下用户问题，提取适合在arXiv上检索的英文关键词或短语（每个关键词尽量简短、准确、用逗号分隔，不要有多余的解释，关键词限制5个以内）：\n\n"
        f"用户问题：{natural_question}\n\n"
        f"输出格式：keyword1, keyword2, ..."
    )
    keywords = deepseek_chat(prompt)
    # 只保留关键词部分（去掉模型可能加的解释）
    keywords = keywords.strip().split('\n')[0].replace('，', ',').replace(';', ',')
    keywords = ','.join([kw.strip() for kw in keywords.split(',') if kw.strip()])
    return keywords

def summarize_and_rank_papers(question, papers):
    # 拼接 prompt
    context = "\n\n".join(
        [f"Title: {p['title']}\nAuthors: {p['authors']}\nPublished: {p['published']}\nSummary: {p['summary']}\nPdf_link: {p['pdf_link']}" 
         for p in papers]
    )
    prompt = (
        f"用户问题：{question}\n\n"
        "以下是与问题相关的arXiv论文，请为相关性和新颖性分别打分，并通过总分对它们进行排序，"
        "输出总分最高的5篇论文的相关性分，新颖性分，总分、标题、PDF地址(根据pdf_link一致)、简要总结和这篇文章为啥可以回答用户相关问题。输出为中文\n\n"
        f"{context}"
    )
    print(prompt[:10000])  # 打印前1000个字符，避免过长
    return deepseek_chat(prompt[:10000])  # 限制最大长度，避免过长的请求

# 示例用法
if __name__ == "__main__":
    # 需要先设置环境变量：export DEEPSEEK_API_KEY=sk-xxx
    print(deepseek_chat("Hello!"))