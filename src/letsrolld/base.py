from bs4 import BeautifulSoup

from letsrolld import http


class BaseObject:

    persistent_attributes = []

    def __init__(self, url):
        self._url = url
        self._soup = None
        self._db = None

    @property
    def db(self):
        return {}

    def _persist_in_db(self, key, value):
        pass

    def __getattribute__(self, item):
        persisted = item in super().__getattribute__("persistent_attributes")
        if persisted:
            val = self.db.get(item, None)
            if val is not None:
                return val
        val = super().__getattribute__(item)
        if persisted:
            self._persist_in_db(item, val)
        return val

    @property
    def url(self):
        if self._url.startswith("/"):
            self._url = "https://www.letterboxd.com" + self._url
        return self._url

    @property
    def soup(self):
        if self._soup is None:
            self._soup = BeautifulSoup(http.get_url(self.url), "html.parser")
        return self._soup

    def __str__(self):
        return self.soup.title.string

    @property
    def text(self):
        return self.soup.prettify()
