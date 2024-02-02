import logging
from http.client import HTTPConnection

import requests
import requests_cache


_CACHE_INSTALLED = False


# stolen from stackoverflow
def enable_debug():
    '''Switches on logging of the requests module.'''
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def get_url(url):
    global _CACHE_INSTALLED
    if not _CACHE_INSTALLED:
        requests_cache.install_cache('cache')
        _CACHE_INSTALLED = True
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        print(e)
