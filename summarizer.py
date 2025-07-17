import nltk
nltk.download('punkt')

import requests
from transformers import pipeline
from newspaper import Article

NEWS_API_KEY = "8ce74c5777ef4f67aa3be70208754244"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines?language=en&pageSize=10"

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_article_text(url):
    try:
        headers = { "User-Agent": "Mozilla/5.0" }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        article = Article(url)
        article.download(input_html=response.text)
        article.parse()

        return article.text.strip()
    except Exception as e:
        print(f"[ERROR] Failed to extract article from {url}: {e}")
        return ""

def summarize_article(content):
    if not content or len(content.split()) < 80:
        return "Summary unavailable."
    try:
        result = summarizer(
            content,
            max_length=200,
            min_length=80,
            do_sample=False
        )
        return result[0]['summary_text']
    except Exception as e:
        print(f"[ERROR] Failed to summarize article: {e}")
        return "Summary unavailable."

def fetch_news():
    try:
        response = requests.get(NEWS_API_URL + f"&apiKey={NEWS_API_KEY}")
        data = response.json()
        articles = []
        for article in data.get("articles", []):
            url = article["url"]
            full_text = extract_article_text(url)
            summary = summarize_article(full_text)

            articles.append({
                "title": article["title"],
                "summary": summary,
                "url": article["url"],
                "image": article["urlToImage"] or "/static/fallback.jpg"
            })
        return articles
    except Exception as e:
        print(f"[ERROR] Failed to fetch news: {e}")
        return []
