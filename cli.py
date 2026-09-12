from weather import get_weather
from tech_news import get_hacker_news, get_github_trending
from summarizer import summarize


def main():
    print("Gathering weather, news, and trending repos...")

    weather = get_weather("Atlanta, GA")
    hn_stories = get_hacker_news()
    trending = get_github_trending()

    briefing = summarize(weather, hn_stories, trending)

    print()
    print("=" * 50)
    print("DAILY BRIEFING")
    print("=" * 50)
    print(briefing)

    print()
    print("-" * 50)
    print("WEATHER")
    print(f"{weather['city']}: {weather['current_temp_f']}F now, "
          f"high {weather['high_f']}F / low {weather['low_f']}F, "
          f"{weather['precip_chance']}% chance of rain")

    print()
    print("HACKER NEWS")
    for story in hn_stories:
        print(f"  - {story['title']} ({story['points']} points)")

    print()
    print("GITHUB TRENDING")
    for repo in trending:
        print(f"  - {repo['name']}: {repo['description']}")


if __name__ == "__main__":
    main()