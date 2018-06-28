
import logging
import os
import requests
import praw
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)

# Load endpoint urls
phonebook_url = os.environ.get('PHONEBOOK')
graveyard_url = os.environ.get('GRAVEYARD')

# Reddit Config
user_agent = "A headline crawler by /u/jezusosaku"
reddit = praw.Reddit(user_agent=user_agent)
subreddits = ["news", "worldnews", "all"]


def crawl_subreddit(sub: str) -> list:
    """ Retrieve the "hot" headlines from the sub. """
    try:
        logging.info("Crawling %s", sub)
        return [post.title for post in reddit.get_subreddit(sub).get_hot()]
    except Exception as e:
        logging.error("Error crawling {}: {}", sub, e)
        return []


def get_headlines() -> list:
    """ Get all the headlines from the configured subreddits. """
    flatten = lambda l: [item for sublist in l for item in sublist]
    all_headlines = flatten([crawl_subreddit(sub) for sub in subreddits])
    return all_headlines


def run(event, context):
    """ This is invoked by AWS Lambda """

    url = os.environ.get('API')
    auth = (
        os.environ.get('HTTP_USER'),
        os.environ.get('HTTP_PASS')
    )

    hl = get_headlines().pop()
    logging.debug(hl)

    res = requests.post(phonebook_url, json=json.dumps({'headline': hl}))

    logging.debug("%s : %s", res.status_code, res.text)
