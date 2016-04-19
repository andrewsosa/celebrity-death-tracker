import sys, os, praw, nltk, wikipedia, requests, dotenv
from requests.auth import HTTPBasicAuth

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(".env")

server_url = os.environ.get("SERVER_URL")
db_user = os.environ.get("DB_USER")
db_pwd = os.environ.get("DB_PWD")
auth = (db_user, db_pwd)

server_url = "http://andrewthewizard.com/wcdt/recv/"

def extract_entities(sample):
    """
    Returns a set of proposed entities
    """
    sentences = nltk.sent_tokenize(sample)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    def extract_entity_names(t):
        entity_names = []

        if hasattr(t, 'label') and t.label:
            if t.label() == 'NE':
                entity_names.append(' '.join([child[0] for child in t]))
            else:
                for child in t:
                    entity_names.extend(extract_entity_names(child))

        return entity_names

    entity_names = []
    for tree in chunked_sentences:
        # Print results per sentence
        # print extract_entity_names(tree)

        entity_names.extend(extract_entity_names(tree))

    # Print unique entity names
    return set(entity_names)

def detect(headline):
    """
    Checks input string headline for celebrities.
    """

    # Check with NLTK
    entities = extract_entities(headline)

    # Generate Extra Options from Entities
    ents = [e.split() for e in list(entities)]
    ents = [[x[i:i+2] for i in range(len(x)-1)] for x in ents]
    ents = [[' '.join(x) for x in y] for y in ents]

    entities = set([item for sublist in ents for item in sublist])

    #print ents

    # Check with name list
    #for e in list(entities):
    #    for t in e.split():
    #        if (t.upper() not in firsts and t.upper() not in lasts) or len(e.split()) is not 2:
    #            entities.discard(e)

    url = None

    # Check with Wikipedia
    for e in list(entities):
        try:
            page = wikipedia.page(str(e), auto_suggest=False)
            cats = page.categories
            url = page.url

            flag = True
            for c in cats:
                if "deaths" in c.lower() or "births" in c.lower():
                    flag = False
                    break
            if flag:
                #print "REJECTED (MISSING CATEGORY)", e
                entities.discard(e)

        except:
            #print "REJECTED (PAGE NOT FOUND)", e
            entities.discard(e)
    return entities, url

def process(t):


    if not any(ext in t.lower() for ext in ["dead", "passed away", "died", "rip", "r.i.p."]):
        #print "NO DEATHS", t
        return

    print "Processing: ",t

    names, url = list(detect(t))
    for name in names:
        #print t, s
        try:
            payload = {
                'person': name,
                'url': url
            }
            res = requests.post(server_url, data=payload, auth=auth)
            print res.status_code
        except Exception as e:
            print "ERROR", e



def main():
    user_agent = "A headline crawler by /u/jezusosaku"
    r = praw.Reddit(user_agent=user_agent)
    #headlines = r.get_front_page()
    subreddits = ["news", "worldnews", "all"]
    headlines = r.get_subreddit("news").get_hot()

    for sub in subreddits:
        headlines = r.get_subreddit(sub).get_hot()
        for t in [x.title for x in headlines]:
            process(t)

if __name__ == "__main__":
    main()
