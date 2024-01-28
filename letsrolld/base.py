from bs4 import BeautifulSoup

from letsrolld import http


class BaseObject:
    def __init__(self, url):
        self._url = url
        self._soup = None

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
