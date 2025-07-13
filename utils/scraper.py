from newspaper import Article
from googlesearch import search
import requests
from bs4 import BeautifulSoup

def get_urls_for_topic(topic, num_results=5):
    """
    Uses Google search to find relevant article URLs for a given topic.
    """
    try:
        return list(search(topic, num_results=num_results))
    except Exception as e:
        print(f"[get_urls_for_topic] Error during search: {e}")
        return []

def scrape_article(url):
    # First try with newspaper3k
    try:
        article = Article(url)
        article.download()
        article.parse()
        text = article.text.strip()
        if len(text.split()) > 100:
            return text
    except Exception as e:
        print(f"[scrape_article] Newspaper failed: {e}")

    # Fallback: requests + BeautifulSoup with better headers
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"[scrape_article] Fallback HTTP status: {response.status_code}")
            return ""

        soup = BeautifulSoup(response.content, 'html.parser')
        for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'form']):
            tag.decompose()

        text = ' '.join(soup.stripped_strings)
        if len(text.split()) > 100:
            return text
        else:
            print(f"[scrape_article] Fallback extracted insufficient content.")
            return ""
    except Exception as e:
        print(f"[scrape_article] BeautifulSoup fallback failed: {e}")
        return ""
