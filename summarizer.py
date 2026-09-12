import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

SYSTEM_PROMPT = (
    "You are a concise daily briefing writer for a software developer. "
    "Given weather and tech news data, write a short, upbeat briefing: "
    "one line on weather, then a few sentences on the most interesting "
    "stories. No headers, no markdown, plain prose, under 150 words."
)

def build_prompt(weather: dict, hn_stories: list[dict], trending: list[dict]) -> str:
    lines = [
        f"Weather in {weather['city']}: {weather['current_temp_f']}F now, "
        f"high {weather['high_f']}F, low {weather['low_f']}F, "
        f"{weather['precip_chance']}% chance of rain.",
        "",
        "Hacker News top stories:",
    ]
    for story in hn_stories:
        lines.append(f"- {story['title']} ({story['points']} points)")

    lines.append("")
    lines.append("GitHub trending repos:")
    for repo in trending:
        lines.append(f"- {repo['name']}: {repo['description']}")

    return "\n".join(lines)

def summarize(weather: dict, hn_stories: list[dict], trending: list[dict]) -> str:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = build_prompt(weather, hn_stories, trending)

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )

    return response.text

if __name__ == "__main__":
    from weather import get_weather
    from tech_news import get_hacker_news, get_github_trending

    w = get_weather("Atlanta, GA")
    hn = get_hacker_news()
    gh = get_github_trending()
    print(summarize(w, hn, gh))