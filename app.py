from flask import Flask, render_template
from weather import get_weather
from tech_news import get_hacker_news, get_github_trending
from summarizer import summarize

app = Flask(__name__)


@app.route("/")
def index():
    weather = get_weather("Atlanta, GA")
    hn_stories = get_hacker_news()
    trending = get_github_trending()
    briefing = summarize(weather, hn_stories, trending)

    return render_template(
        "index.html",
        briefing=briefing,
        weather=weather,
        hn_stories=hn_stories,
        trending=trending,
    )


if __name__ == "__main__":
    app.run(debug=True)