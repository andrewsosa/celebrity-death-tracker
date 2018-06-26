import datetime
import logging
import requests
import wikipedia

logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)


def check_graveyard(name: str) -> (str, str):
    """ Checks Wikipedia for the input namestring to see if the name
        is both:
            - Someone important enough to have a wikipedia page.
            - Someone who died recently (today).
    """

    try:
        page = wikipedia.page(name, auto_suggest=False)
        cats = page.categories
        summary = page.summary
        url = page.url

        today = datetime.datetime.now().strftime("%B %d, %Y")

        if "2018 deaths" in [c.lower() for c in cats]: # and today in summary:
            logging.debug("APPROVED: %s", name)
            return name, str(url)
        else:
            logging.debug("REJECTED (MISSING CATEGORY) %s", name)

    except:
        logging.debug("REJECTED (PAGE NOT FOUND) %s", name)

    return None, None


# def process_headline(headline) -> list:
#     """
#     Check if this headline has a death keyword in it; if so
#     then confirm whether there is a dead celebrity.
#     """

#     if not any(ext in headline.lower()
#                for ext in ["dead", "death", "passed away",
#                            "died", "rip", "r.i.p."]):
#         return

#     logging.info("Processing: %s...", headline)
#     results = detect_celebrities(headline)

#     return [{
#             'person': name,
#             'url': wikipedia_url,
#             'reported': datetime.datetime.utcnow().isoformat()
#             } for name, wikipedia_url in results.items()]

    # for name, wikipedia_url in results.items():
    #     try:
    #         payload = {
    #             'person': name,
    #             'url': wikipedia_url
    #         }
    #         logging.debug("upload %s", payload)
    #         # res = requests.post(server_url, data=payload, auth=auth)
    #         # logging.debug("POST STATUS: %s", res.status_code)
    #     except Exception as e:
    #         logging.error("ERROR: %s", e)
