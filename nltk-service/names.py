import logging
import nltk

logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)


def extract_entity_names(t):
    """ Use NLTK to find names in a tree.
    """
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names


def extract_entities(sample: str) -> list:
    """ Propose a set of entities from a sample.
    """
    # Tokenize the sample
    sentences = nltk.sent_tokenize(sample)
    tokenized_sentences = [nltk.word_tokenize(sentence)
                           for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence)
                        for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    # Detect entities
    # names = [extract_entity_names(tree) for tree in chunked_sentences]
    # Detect entities
    names = []
    for tree in chunked_sentences:
        names.extend(extract_entity_names(tree))


    # Generate Extra Options
    ents = [e.split() for e in names]
    ents = [[x[i:i + 2] for i in range(len(x) - 1)] for x in ents]
    ents = [[' '.join(x) for x in y] for y in ents]

    entities = set(names) | set([item for sublist in ents for item in sublist])
    return list(entities)
