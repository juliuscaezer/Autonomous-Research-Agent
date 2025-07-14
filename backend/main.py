# backend/main.py
from fastapi import FastAPI, Query
from utils.scraper import get_urls_for_topic, scrape_article
from utils.llm import summarize_article
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]

)

@app.get("/research")
async def research(query: str = Query(...)):
    urls = get_urls_for_topic(query, num_results=15)
    results = []

    for url in urls:
        try:
            text = await scrape_article(url)
            if not text.strip():
                continue  # skip empty text
            summary = summarize_article(text, url)
            results.append(summary)
        except Exception as e:
            continue  # robust fail-safe

        if len(results) == 5:
            break  # stop when 5 valid results are collected

    return {"query": query, "results": results}
