import os
import requests
from dotenv import load_dotenv
load_dotenv()

def summarize_article(text, url):
    if not text:
        return {"url": url, "summary": "Failed to scrape content."}

    prompt = f"""Summarize the following article in 3 key points.
Include a citation link at the end.

URL: {url}
Article:
{text[:4000]}
"""

    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    headers = {
        "Authorization": f"Bearer {mistral_api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-tiny",  # or mistral-small, mistral-medium
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        summary = response.json()['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as e:
        summary = f"HTTP error: {e}"
    except Exception as e:
        summary = f"Unexpected error: {e}"

    return {"url": url, "summary": summary}
