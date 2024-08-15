import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_top_news(count: int = 10):
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(top_stories_url)
    # print("response status code ",response.status_code)
    # print("response.json() ",response.json())
    # print("response.json()[:count] ",response.json()[:count])
    if response.status_code == 200:
        top_stories_ids = response.json()[:count]
        top_stories = []

        for top_story_id in top_stories_ids:
            top_story_url = f"https://hacker-news.firebaseio.com/v0/item/{top_story_id}.json"
            response = requests.get(top_story_url)
            # print("response status code ",response.status_code)
            # print("top story - response.json() ",response.json())
            top_story = response.json()
            top_stories.append(top_story)
        return {"top news":top_stories}
    else:
        return {"error": "Failed to retrieve top stories"}