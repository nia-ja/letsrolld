import os.path

from letsrolld.base import BaseObject
from letsrolld import film


class Director(BaseObject):

    @property
    def name(self):
        return self.soup.title.string

    @property
    def url(self):
        url = super().url
        print("ihar", url)
        if not url.endswith("/by/rating/"):
            return os.path.join(url, "by/rating/")
        return url

    def films(self):
        for movie in self.soup.find_all("div", class_="film-poster"):
            yield film.Film(url=movie.get("data-target-link"))
