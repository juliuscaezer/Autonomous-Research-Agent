# backend/main.py

from fastapi import FastAPI, Query
from utils.scraper import get_urls_for_topic, scrape_article
from utils.llm import summarize_article
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.get("/research")
async def research(query: str = Query(...)):
    urls = get_urls_for_topic(query)
    results = []

    for url in urls[:3]:  # Limit to 3 URLs
        text = scrape_article(url)
        summary = summarize_article(text, url)
        results.append(summary)

    return {"query": query, "results": results}
