import logging
from http.client import HTTPConnection

import requests


_CACHE_INSTALLED = False


# stolen from stackoverflow
def enable_debug():
    """Switches on logging of the requests module."""
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def get_url(url):
    return requests.get(url).text


def get_json(url, json, validator=None):
    def _get_json(url, json, entity, validator):
        res = entity.post(url, json=json).json()
        if validator is not None and not validator(res):
            raise ValueError("Invalid response")
        return res

    return _get_json(url, json, requests, validator=validator)
