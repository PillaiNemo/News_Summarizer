
import requests
from transformers import pipeline
from bs4 import BeautifulSoup

NEWS_API_KEY = "8ce74c5777ef4f67aa3be70208754244"
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def fetch_news():
    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=10&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    return response.json().get("articles", [])

def clean_text(html):
    return BeautifulSoup(html, "html.parser").get_text()

def summarize_content(content):
    if not content or len(content.split()) < 30:
        return content
    length = len(content.split())
    min_len = max(30, int(length * 0.3))
    max_len = max(60, int(length * 0.6))
    try:
        summary = summarizer(content, max_length=max_len, min_length=min_len, do_sample=False)[0]["summary_text"]
        return summary
    except:
        return content

def get_news_summaries():
    articles = fetch_news()
    summarized = []
    for art in articles:
        content = clean_text(art.get("description") or art.get("content") or "")
        summarized.append({
            "title": art.get("title"),
            "url": art.get("url"),
            "image": art.get("urlToImage"),
            "summary": summarize_content(content)
        })
    return summarized
