""" Microservices w/ NLTK """

import json, logging
from nameko.web.handlers import http

logging.basicConfig(level=logging.DEBUG)


class NLTKService:
    """ This service accepts a string (preferable a headline) and will
        return a list of potential entities (probably names) that live
        in that headline!
    """
    name = "nltk_service"

    @http('POST', '/phonebook')
    def parse_names(self, request):
        """ Route to get names from a headline. """
        from .names import extract_entities

        try:
            data = json.loads(request.get_data(as_text=True))
            headline = data['headline']
            payload = {'possible_names': extract_entities(headline)}
            return json.dumps(payload)

        except json.JSONDecodeError:
            return 400, "You're not JSON!\n"
        except KeyError:
            return 400, "This isn't a headline."
        except Exception as e:
            logging.error("Error: %s", str(e))
            return 500, "Something went wrong"


    @http('POST', '/graveyard')
    def check_death(self, request):
        """ Check if person is dead. """
        from .wiki import check_graveyard

        try:
            data = json.loads(request.get_data(as_text=True))
            name = data['name']
            name, url = check_graveyard(name)
            if not name:
                return 404, "Famous person not found."
            else:
                return json.dumps({'name': name, 'url': url})

        except json.JSONDecodeError:
            return 400, "You're not JSON!\n"
        except KeyError:
            return 400, "This isn't a headline."
        except Exception as e:
            logging.error("Error: %s", str(e))
            return 500, "Something went wrong"
