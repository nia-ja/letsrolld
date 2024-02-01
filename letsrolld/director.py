import os.path
import random

from letsrolld.base import BaseObject
from letsrolld import film


_DEFAULT_SORT = "by/rating/"


class Director(BaseObject):

    @property
    def name(self):
        for desc in self.soup.find_all("meta", property="og:title"):
            return desc.get("content").replace("Films directed by ", "")
        return self.soup.title.string

    @property
    def base_url(self):
        return self.url.replace(_DEFAULT_SORT, "")

    @property
    def url(self):
        url = super().url
        if not url.endswith(_DEFAULT_SORT):
            return os.path.join(url, _DEFAULT_SORT)
        return url

    def films(self):
        for movie in self.soup.find_all("div", class_="film-poster"):
            yield film.Film(url=movie.get("data-target-link"))


def get_directors(watch_list, by_rating=True):
    watch_list = watch_list[:]
    random.shuffle(watch_list)

    directors = {}
    for wle in watch_list:
        movie = film.Film(wle.uri)
        for director in movie.directors:
            if director.base_url not in directors:
                directors[director.base_url] = director
                yield director
