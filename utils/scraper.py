# utils/scraper.py
import logging
from googlesearch import search
import newspaper
from newspaper.article import ArticleException
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO)

def get_urls_for_topic(topic: str, num_results: int = 20):
    try:
        return list(search(topic, num_results=num_results))
    except Exception as e:
        logging.error(f"[search] {e}")
        return []

async def scrape_article(url: str) -> str:
    """Async: Newspaper first, Playwright fallback."""
    try:
        art = newspaper.Article(url)
        art.download(); art.parse()
        if art.text.strip():
            return art.text.strip()
    except ArticleException as e:
        logging.warning(f"[Newspaper] {e}")

    # Playwright fallback
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=15000)
            await page.wait_for_load_state("networkidle")
            text = await page.inner_text("body")
            await browser.close()
            return text if len(text.split()) > 100 else ""
    except Exception as e:
        logging.error(f"[Playwright] {e}")
        return ""
