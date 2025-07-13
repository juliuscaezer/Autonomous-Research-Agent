# utils/scraper.py

import newspaper
from duckduckgo_search import ddg

def get_urls_for_topic(topic):
    results = ddg(topic, max_results=5)
    return [r['href'] for r in results if 'href' in r]

def scrape_article(url):
    try:
        article = newspaper.Article(url)
        article.download()
        article.parse()
        return article.text
    except:
        return ""
