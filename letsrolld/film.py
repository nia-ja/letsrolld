import re

from letsrolld import director
from letsrolld.base import BaseObject


class Film(BaseObject):

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.year == other.year and
            self.rating == other.rating
        )

    @property
    def _full_title(self):
        return (
            # TODO: extract name and year from the body?
            self.soup.title.string.split(" directed by")[0].
            strip().
            replace(u'\u200e', "")
        )

    @property
    def name(self):
        pattern = r'^(.*?)\s*\(\d{4}\)'
        match = re.search(pattern, self._full_title)
        if match:
            return match.group(1).strip()

    @property
    def year(self):
        pattern = r'\((\d{4})\)'
        match = re.search(pattern, self._full_title)
        if match:
            return match.group(1).strip()

    @property
    def directors(self):
        for crew in self.soup.find_all(id="tab-crew"):
            for h3 in crew.find_all("h3"):
                text = h3.text.strip()
                if "Director\n" in text or "Directors\n" in text:
                    text_slug = h3.next_sibling.next_sibling
                    return [
                        director.Director(url=a.get("href"))
                        for a in text_slug.find_all("a")
                    ]

    @property
    def rating(self):
        # TODO: parse as json
        for script in self.soup.find_all("script"):
            if "ratingValue" in script.text:
                return script.text.split("ratingValue")[1].split(":")[1].split(",")[0].strip()
        return "0"
