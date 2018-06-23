from .crawl import get_headlines
from .parse import process_headline

import logging
import os
import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# logging.basicConfig(level=logging.DEBUG)


def run(event, context):
    """
    This is invoked by AWS Lambda
    """

    url = os.environ.get('API')
    auth = (
        os.environ.get('HTTP_USER'),
        os.environ.get('HTTP_PASS')
    )

    for hl in get_headlines():
        payloads = process_headline(hl)

        if payloads is None:
            continue

        for pl in payloads:
            # logger.info('Posting %s', pl['person'])
            res = requests.post(url, data=pl, auth=auth)
            if res.status_code is not 200:
                logger.error('Upload failed!')
