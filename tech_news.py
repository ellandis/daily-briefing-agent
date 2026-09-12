import requests
from bs4 import BeautifulSoup


def get_hacker_news(limit: int = 5) -> list[dict]:
    ids_response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    top_ids = ids_response.json()

    stories = []
    for story_id in top_ids[:limit]:
        item_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
        item = item_response.json()

        stories.append({
            "title": item["title"],
            "url": item.get("url",f"https://news.ycombinator.com/item?id={story_id}"),
            "points": item.get("score"),
            "comments": item.get("descendants"),
        })

    return stories

def get_github_trending(limit: int = 5) -> list[dict]:
    response = requests.get(
        "https://github.com/trending",
        headers={"User-Agent": "daily-briefing-agent/1.0"},
    )
    soup = BeautifulSoup(response.text, "html.parser")

    repos = []
    for article in soup.select("article.Box-row")[:limit]:
        link = article.select_one("h2 a")
        repo_path = link["href"].strip("/")  # e.g. "torvalds/linux"

        description_el = article.select_one("p")
        description = description_el.get_text(strip=True) if description_el else ""

        repos.append({
            "name": repo_path,
            "url": f"https://github.com/{repo_path}",
            "description": description,
        })

    return repos

if __name__ == "__main__":
    print(get_hacker_news())
    print(get_github_trending())