from flask import Flask, render_template
from summarizer import fetch_news
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
articles = []

def update_news():
    global articles
    articles = fetch_news()

# Schedule updates every 4 hours
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_news, trigger="interval", hours=4)
scheduler.start()

@app.route("/")
def index():
    return render_template("index.html", articles=articles)

if __name__ == "__main__":
    update_news()  # Initial fetch
    app.run(debug=True)
