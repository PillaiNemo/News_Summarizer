
from flask import Flask, render_template
from summarizer import get_news_summaries
import time

app = Flask(__name__)

# Cache configuration
cached_articles = []
last_updated = 0
UPDATE_INTERVAL = 4 * 60 * 60  # 4 hours in seconds

@app.route('/')
def home():
    global cached_articles, last_updated

    current_time = time.time()
    if not cached_articles or current_time - last_updated > UPDATE_INTERVAL:
        print("[INFO] Fetching fresh news summaries...")
        cached_articles = get_news_summaries()
        last_updated = current_time
    else:
        print("[INFO] Using cached news summaries.")

    return render_template('index.html', articles=cached_articles)

if __name__ == '__main__':
    app.run(debug=True)
