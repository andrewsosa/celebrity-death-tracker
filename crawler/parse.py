import logging
import nltk
import requests
import wikipedia
from mediawiki import MediaWiki

logging.basicConfig(level=logging.DEBUG)

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

wikipedia = MediaWiki()


def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names


def extract_entities(sample):
    """
    Returns a set of proposed entities
    """
    sentences = nltk.sent_tokenize(sample)
    tokenized_sentences = [nltk.word_tokenize(sentence)
                           for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence)
                        for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    entity_names = []
    for tree in chunked_sentences:
        entity_names.extend(extract_entity_names(tree))

    return set(entity_names)


def detect_celebrities(headline):
    """
    Checks input string headline for celebrities.
    """

    # Check with NLTK
    entities = extract_entities(headline)

    # Generate Extra Options from Entities
    ents = [e.split() for e in list(entities)]
    ents = [[x[i:i + 2] for i in range(len(x) - 1)] for x in ents]
    ents = [[' '.join(x) for x in y] for y in ents]

    entities = entities | set([item for sublist in ents for item in sublist])

    logging.debug("CANDIDATE ENTITIES: %s", entities)

    results = dict()

    # Check with Wikipedia
    for ent in list(entities):
        try:
            page = wikipedia.page(str(ent), auto_suggest=False)
            cats = page.categories
            url = page.url

            if "2018 deaths" in [c.lower() for c in cats]:
                logging.debug("APPROVED: %s", ent)
                results[ent] = url
            else:
                logging.debug("REJECTED (MISSING CATEGORY) %s", ent)

        except:
            logging.debug("REJECTED (PAGE NOT FOUND) %s", ent)

    return results


def process_headline(headline):
    """
    Check if this headline has a death keyword in it.
    """

    if not any(ext in headline.lower()
               for ext in ["dead", "passed away", "died", "rip", "r.i.p."]):
        return

    logging.info("Processing: %s", headline)

    results = detect_celebrities(headline)

    for name, wikipedia_url in results.items():
        try:
            payload = {
                'person': name,
                'url': wikipedia_url
            }
            logging.debug("upload %s", payload)
            # res = requests.post(server_url, data=payload, auth=auth)
            # logging.debug("POST STATUS: %s", res.status_code)
        except Exception as e:
            logging.error("ERROR: %s", e)
