import re

from letsrolld import director
from letsrolld.base import BaseObject


class Film(BaseObject):

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
    def director(self):
        for crew in self.soup.find_all(id="tab-crew"):
            for h3 in crew.find_all("h3"):
                if "Director\n" in h3.text.strip():
                    return director.Director(
                        url=h3.next_sibling.next_sibling.find("a").get("href"))

    @property
    def rating(self):
        # TODO: parse as json
        for script in self.soup.find_all("script"):
            if "ratingValue" in script.text:
                return script.text.split("ratingValue")[1].split(":")[1].split(",")[0].strip()
        return "0"
