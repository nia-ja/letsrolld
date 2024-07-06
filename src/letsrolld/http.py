import logging
from http.client import HTTPConnection

import requests


_CACHE_INSTALLED = False

# TODO: use a library to fill these in
_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.39.0",
}


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


def get_json(url, json):
    return requests.post(url, headers=_HEADERS, json=json)
