import logging
from http.client import HTTPConnection

import requests
import requests_cache as rc


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
        rc.install_cache(
            'cache', allowable_methods=('GET', 'HEAD', 'POST'))
        _CACHE_INSTALLED = True


def get_url(url):
    _install_cache()

    def _get_url(url, entity):
        return entity.get(url).text

    try:
        return _get_url(url, requests)
    except Exception as e:
        print(e)
        return _get_url(
            url, rc.CachedSession(expire_after=rc.EXPIRE_IMMEDIATELY))


def get_json(url, json, validator=None):
    _install_cache()

    def _get_json(url, json, entity, validator):
        res = entity.post(url, json=json).json()
        if validator is not None and not validator(res):
            raise ValueError("Invalid response")
        return res

    try:
        return _get_json(url, json, requests, validator=validator)
    except Exception as e:
        print(e)
        return _get_json(
            url, json,
            rc.CachedSession(expire_after=rc.EXPIRE_IMMEDIATELY),
            validator=None)
