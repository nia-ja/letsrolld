import functools
import os.path

from letsrolld.base import BaseObject
from letsrolld import film


_DEFAULT_SORT = "by/rating/"


class Director(BaseObject):
    @functools.cached_property
    def name(self):
        for desc in self.soup.find_all("meta", property="og:title"):
            return desc.get("content").replace("Films directed by ", "")
        return self.soup.title.string

    @functools.cached_property
    def base_url(self):
        return self.url.replace(_DEFAULT_SORT, "")

    @functools.cached_property
    def url(self):
        url = super().url
        if not url.endswith(_DEFAULT_SORT):
            return os.path.join(url, _DEFAULT_SORT)
        return url

    @property
    def film_urls(self):
        urls = []
        for movie in self.soup.find_all("div", class_="film-poster"):
            urls.append(movie.get("data-target-link"))
        return urls

    def films(self):
        for url in self.film_urls:
            yield film.Film(url)
