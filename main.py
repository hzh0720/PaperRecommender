from deepseek import deepseek_chat , summarize_and_rank_papers
import requests
from arxiv import search_arxiv


def main():
    import os

    # 用户输入
    question = input("请输入你的问题：")
    preference = input("请输入你的偏好类型（如AI领域填cs.AI，留空为不限）：")

    # 检索论文
    papers = search_arxiv(question, max_results=5, category=preference.strip() or None)
    if not papers:
        print("未检索到相关论文。")
        return

    answer = summarize_and_rank_papers(question, papers)
    print("\n===== 排序与总结 =====\n")
    print(answer)


if __name__ == "__main__":
    main()