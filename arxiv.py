import requests
import feedparser

def search_arxiv(query, max_results=5, category=None, sort_by="relevance"):
    base_url = 'http://export.arxiv.org/api/query?'
    search_query = f'all:{query}'
    if category:
        search_query += f'+AND+cat:{category}'
    url = (
        f"{base_url}search_query={search_query}"
        f"&sortBy={sort_by}&sortOrder=descending&max_results={max_results}"
    )
    response = requests.get(url)
    feed = feedparser.parse(response.text)
    papers = []
    for entry in feed.entries:
        abs_url = entry.link
        # 提取arXiv编号
        arxiv_id = abs_url.split('/')[-1]
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        papers.append({
            'title': entry.title,
            'summary': entry.summary,
            'authors': ', '.join(author.name for author in entry.authors),
            'published': entry.published,
            'pdf_link': pdf_url   # 论文PDF下载地址
        })
    return papers

# 示例用法
if __name__ == "__main__":
    papers = search_arxiv("chatgpt", max_results=3, sort_by="relevance")
    for i, p in enumerate(papers, 1):
        print(f"{i}. {p['title']}\n   PDF: {p['pdf_link']}\n")