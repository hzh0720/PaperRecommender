from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

from deepseek import summarize_and_rank_papers, extract_keywords
from arxiv import search_arxiv, deduplicate_papers

app = FastAPI(title="Paper Recommender API")


class PaperRequest(BaseModel):
    question: str = Field(..., description="用户问题，例如：大模型在自然语言处理中的最新研究进展")
    preference_desc: Optional[str] = Field("", description="问题偏好，自然语言描述，留空为无")
    category: Optional[str] = Field(
        "",
        description="论文类别，如cs.AI、cs.LG、quant-ph、econ.EM等，留空为不限"
    )


@app.post("/recommend", response_model=str)
def recommend_papers_api(req: PaperRequest):
    # 拼接完整的问题
    full_question = f"{req.question}。{req.preference_desc}" if req.preference_desc else req.question
    keywords = extract_keywords(full_question)
    all_papers = []
    for kw in keywords.split(','):
        kw = kw.strip()
        if not kw:
            continue
        papers = search_arxiv(kw, max_results=5, category=req.category, sort_by="relevance")
        all_papers.extend(papers)
    all_papers = deduplicate_papers(all_papers)
    if not all_papers:
        return "未检索到相关论文。"

    answer = summarize_and_rank_papers(full_question, all_papers)
    return answer


# 本地调试入口
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)