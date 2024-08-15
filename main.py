import requests
from fastapi import FastAPI, HTTPException
from requests_cache import CachedSession

app = FastAPI()

session = CachedSession(
    cache_name='cache/news',
    expire_after = 600
)

@app.get("/")
def get_top_news(count: int = 10):
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = session.get(top_stories_url)
    # print("response status code ",response.status_code)
    # print("response.json() ",response.json())
    # print("response.json()[:count] ",response.json()[:count])
    if response.status_code == 200:
        try:
            top_stories_ids = response.json()[:count]
            top_stories = []

            for top_story_id in top_stories_ids:
                top_story_url = f"https://hacker-news.firebaseio.com/v0/item/{top_story_id}.json"
                response = requests.get(top_story_url)
                if response.status_code == 200:
                    # print("response status code ",response.status_code)
                    # print("top story - response.json() ",response.json())
                    top_story = response.json()
                    top_stories.append(top_story)
                else:
                    raise HTTPException(status_code=500, detail="Failed to retrieve the stop story")
            return {"top news":top_stories}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=500, detail="Failed to retrieve top stories")