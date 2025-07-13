import os
import requests

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")  # Or hardcode temporarily: "your-mistral-key"
MISTRAL_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-medium"  # Or "mistral-small", "mistral-large" depending on your plan

def summarize_article(text, url):
    if not text:
        return {"url": url, "summary": "Failed to scrape content."}

    prompt = f"""Summarize the following article in 3 key points.
Include a citation link at the end.

URL: {url}
Article:
{text[:4000]}
"""

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(MISTRAL_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        summary = response.json()['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as e:
        summary = f"HTTP error: {str(e)}"
    except Exception as e:
        summary = f"An error occurred: {str(e)}"

    return {"url": url, "summary": summary}
