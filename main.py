from deepseek import deepseek_chat , summarize_and_rank_papers,extract_keywords
import requests
from arxiv import search_arxiv,deduplicate_papers


def main():
    # 用户输入
    question = input("请输入你的问题：")
    preference_desc = input("请输入你的问题偏好，留空为无：")
    category = input("请输入论文类别（如人工智能cs.AI，机器学习cs.LG，量子物理quant-ph，经济学econ.EM等，留空为不限）：")
    
    question = f"{question}。{preference_desc}"

    keywords = extract_keywords(question)
    print(f"\n提取的关键词：{keywords}\n")

    all_papers = []
    for kw in keywords.split(','):
        kw = kw.strip()
        print(f"正在检索关键词：{kw} ...")
        if not kw:
            continue
        papers = search_arxiv(kw, max_results=5, category=category, sort_by="relevance")
        all_papers.extend(papers)
    all_papers = deduplicate_papers(all_papers)
    if not all_papers:
        print("未检索到相关论文。")
        return

    # 3. 大模型总结与排序
    print("正在分析和排序论文，请稍候…")
    answer = summarize_and_rank_papers(question, all_papers)
    print("\n===== 排序与总结 =====\n")
    print(answer)

if __name__ == "__main__":
    main()