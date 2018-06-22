from tqdm import tqdm

from crawl import get_headlines
from parse import process_headline


if __name__ == '__main__':
    # headlines = tqdm(get_headlines())
    [process_headline(hl.title) for hl in get_headlines()]
