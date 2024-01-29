import re
from bs4 import BeautifulSoup

from letsrolld import director
from letsrolld import http
from letsrolld import justwatch as jw
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
            self._jw = jw.get_title(self.jw_url)
            self._jw_fetched = True
        return self._jw

    @property
    def offers(self):
        return [] if self.jw is None else self.jw.offers

    @property
    def genre_names(self):
        return "unknown" if self.jw is None else ','.join(self.jw.genres)

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.year == other.year and
            self.rating == other.rating
        )

    @property
    def description(self):
        return "unknown" if self.jw is None else self.jw.short_description

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
    def jw_url(self):
        for x in self.avail_soup.find_all("a", class_="jw-branding"):
            link = x.get("href")
            if not link.startswith("https://www.justwatch.com/us/movie/"):
                return None
            return link

    @property
    def runtime(self):
        if self.jw is None:
            return 0
        return self.jw.runtime_minutes

    @property
    def runtime_string(self):
        if self.jw is None:
            return "unknown"
        return f"{self.jw.runtime_minutes}m"

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

    def _get_director_slugs(self):
        for crew in self.soup.find_all(id="tab-crew"):
            for h3 in crew.find_all("h3"):
                text = h3.text.strip()
                if "Director\n" in text or "Directors\n" in text:
                    text_slug = h3.next_sibling.next_sibling
                    return text_slug.find_all("a")
        return []

    @property
    def directors(self):
        return [
            director.Director(url=a.get("href"))
            for a in self._get_director_slugs()
        ]

    @property
    def director_names(self):
        return ', '.join(
            a.text.strip()
            for a in self._get_director_slugs()
        )

    @property
    def rating(self):
        # TODO: parse as json
        for script in self.soup.find_all("script"):
            if "ratingValue" in script.text:
                return script.text.split("ratingValue")[1].split(":")[1].split(",")[0].strip()
        return "0"
