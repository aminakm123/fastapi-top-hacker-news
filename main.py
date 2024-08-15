import requests
import logging
from fastapi import FastAPI, HTTPException
from requests_cache import CachedSession


app = FastAPI()

logging.basicConfig(level=logging.DEBUG, filename="logs/news.log", 
                    format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

session = CachedSession(
    cache_name='cache/news',
    expire_after = 600
)

@app.get("/")
def get_top_news(count: int = 10):
    logger.info(f"Top {count} hacker news")
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = session.get(top_stories_url)
    logger.debug(f"response status code : {response.status_code}")
    logger.debug(f"response.json()[:count] : {response.json()[:count]}")
    if response.status_code == 200:
        try:
            top_stories_ids = response.json()[:count]
            top_stories = []

            for top_story_id in top_stories_ids:
                top_story_url = f"https://hacker-news.firebaseio.com/v0/item/{top_story_id}.json"
                response = requests.get(top_story_url)
                if response.status_code == 200:
                    logger.debug(f"response status code : {response.status_code}")
                    logger.debug(f"top story - response.json() : {response.json()}")
                    top_story = response.json()
                    top_stories.append(top_story)
                else:
                    logger.warning(f"Failed to retrieve the stop story")
                    raise HTTPException(status_code=500, detail="Failed to retrieve the stop story")
            return {"top news":top_stories}
        except Exception as e:
            logger.critical(f"{str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        logger.error(f"Failed to retrieve top stories")
        raise HTTPException(status_code=500, detail="Failed to retrieve top stories")