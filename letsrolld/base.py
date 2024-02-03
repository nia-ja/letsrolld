from bs4 import BeautifulSoup
import sqlitedict

from letsrolld import http


_DB = sqlitedict.SqliteDict('letsrolld.db', autocommit=True)


class BaseObject:

    persistent_attributes = []

    def __init__(self, url):
        self._url = url
        self._soup = None

    def _persist_in_db(self, key, value):
        values = _DB.get(self.url, {})
        values[key] = value
        _DB[self.url] = values

    def _get_from_db(self, key):
        return _DB.get(self.url, {}).get(key, None)

    def __getattribute__(self, item):
        persisted = item in super().__getattribute__('persistent_attributes')
        if persisted:
            val = self._get_from_db(item)
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
            self._soup = BeautifulSoup(http.get_url(self.url), 'html.parser')
        return self._soup

    def __str__(self):
        return self.soup.title.string

    @property
    def text(self):
        return self.soup.prettify()
