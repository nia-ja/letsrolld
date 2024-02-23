import functools
import os.path
import random

from letsrolld.base import BaseObject
from letsrolld import film


_DEFAULT_SORT = "by/rating/"


class Director(BaseObject):

    persistent_attributes = ["name", "film_urls"]

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


def get_directors_by_films(film_list):
    film_list = film_list[:]
    random.shuffle(film_list)

    directors = {}
    for film_ in film_list:
        movie = film.Film(film_.uri)
        for director in movie.directors:
            if director.base_url not in directors:
                directors[director.base_url] = director
                yield director


def get_directors_by_urls(director_list):
    director_list = director_list[:]
    random.shuffle(director_list)

    for director_ in director_list:
        # assume unique entries in the input list
        yield Director(director_.uri)
