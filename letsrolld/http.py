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


def _install_cache():
    global _CACHE_INSTALLED
    if not _CACHE_INSTALLED:
        # TODO: expire the cache after a certain time
        requests_cache.install_cache(
            'cache', allowable_methods=('GET', 'HEAD', 'POST'))
        _CACHE_INSTALLED = True


def get_url(url):
    _install_cache()
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        print(e)


def get_json(url, json):
    _install_cache()
    try:
        response = requests.post(url, json=json)
        return response.json()
    except Exception as e:
        print(e)
