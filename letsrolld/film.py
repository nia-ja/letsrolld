import re
from bs4 import BeautifulSoup

from simplejustwatchapi import justwatch as jw

from letsrolld import director
from letsrolld import http
from letsrolld.base import BaseObject


KANOPY = "kanopy"
HOOPLA = "hoopla"
AMAZONPRIME = "amazonprime"
AMAZON = "amazon"
YOUTUBE = "youtube"
CRITERION = "criterionchannel"

PHYSICAL = "physical"

SERVICES = [
    KANOPY,
    HOOPLA,
    AMAZONPRIME,
    AMAZON,
    YOUTUBE,
    CRITERION,
    PHYSICAL,
]


class Film(BaseObject):

    def __init__(self, url=None):
        super().__init__(url)
        self._jw = None
        self._jw_fetched = False
        self._avail_soup = None

    @property
    def jw(self):
        if not self._jw_fetched:
            # TODO: fetch justwatch link from letterboxd instead of fuzzy search
            result = jw.search(f"{self.name}", "US", "en", 1, False)
            self._jw = None if len(result) == 0 else result[0]
            self._jw_fetched = True
        return self._jw

    @property
    def offers(self):
        return [] if self.jw is None else self.jw.offers

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.year == other.year and
            self.rating == other.ratin
        )

    @property
    def avail_soup(self):
        if self._avail_soup is None:
            url = self.url.replace("letterboxd.com", "letterboxd.com/csi") + "availability/"
            self._avail_soup = BeautifulSoup(http.get_url(url), 'html.parser')
        return self._avail_soup

    def available_physical(self):
        for x in self.avail_soup.find_all("p", class_="service -amazon"):
            return True
        return False

    def available(self, service):
        if service == PHYSICAL:
            return self.available_physical()
        for offer in self.offers:
            if offer.technical_name == service:
                return True
        return False

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
