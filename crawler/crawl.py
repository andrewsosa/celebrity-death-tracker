import praw
import requests
import logging
from requests.auth import HTTPBasicAuth
# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# dotenv.load_dotenv(".env")

# server_url = os.environ.get("SERVER_URL")
# db_user = os.environ.get("DB_USER")
# db_pwd = os.environ.get("DB_PWD")
# auth = (db_user, db_pwd)

# server_url = "http://andrewthewizard.com/wcdt/recv/"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

user_agent = "A headline crawler by /u/jezusosaku"
reddit = praw.Reddit(user_agent=user_agent)
subreddits = ["news", "worldnews", "all"]


def crawl_subreddit(sub: str) -> list:
    """
    Retrieve the "hot" headlines from the sub.
    """
    try:
        logging.info("Crawling %s", sub)
        return [post.title for post in reddit.get_subreddit(sub).get_hot()]
    except Exception as e:
        logging.error("Error crawling {sub}: {error}", sub=sub, error=e)
        return []


def get_headlines() -> list:
    """
    Get all the headlines from the configured subreddits.
    """
    flatten = lambda l: [item for sublist in l for item in sublist]
    all_headlines = flatten([crawl_subreddit(sub) for sub in subreddits])
    return all_headlines


if __name__ == "__main__":
    [headline for headline in get_headlines()]
