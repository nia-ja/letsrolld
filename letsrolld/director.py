from letsrolld.base import BaseObject
from letsrolld import film


class Director(BaseObject):

    @property
    def name(self):
        return self.soup.title.string

    def films(self):
        for movie in self.soup.find_all("div", class_="film-poster"):
            yield film.Film(url=movie.get("data-target-link"))
