from simplejustwatchapi import justwatch as jw
from simplejustwatchapi import query as jw_query

from letsrolld import http


_GRAPHQL_GET_TITLE_QUERY = """
query GetUrlTitleDetails($fullPath: String!, $country: Country!, $language: Language!, $platform: Platform! = WEB) {
  urlV2(fullPath: $fullPath) {
    node {
      ... on MovieOrShowOrSeason {
        objectType
        objectId
        offers(country: $country, platform: $platform) {
          monetizationType
          package {
            packageId
            clearName
            technicalName
            icon(profile: S100, format: PNG)
          }
        }
        content(country: $country, language: $language) {
          backdrops {
            backdropUrl
          }
          externalIds {
            imdbId
          }
          fullPath
          genres {
            slug(language: $language)
          }
          posterUrl
          runtime
          shortDescription
          title
          originalReleaseYear
          originalReleaseDate
        }
      }
    }
  }
}
"""


def prepare_get_title_request(url):
    return {
        "operationName": "GetUrlTitleDetails",
        "variables": {
            "fullPath": url.replace("https://www.justwatch.com", ""),
            "country": "US",
            "language": "en",
        },
        "query": _GRAPHQL_GET_TITLE_QUERY,
    }


def _parse_entry(json):
    entry_id = json.get("id")
    object_id = json.get("objectId")
    object_type = json.get("objectType")
    content = json["content"]
    title = content.get("title")
    url = jw_query._DETAILS_URL + content.get("fullPath")
    year = content.get("originalReleaseYear")
    date = content.get("originalReleaseDate")
    runtime_minutes = content.get("runtime")
    short_description = content.get("shortDescription")
    genres = [node.get("slug") for node in content.get("genres", []) if node]
    external_ids = content.get("externalIds")
    imdb_id = external_ids.get("imdbId") if external_ids else None
    poster_url_field = content.get("posterUrl")
    poster = jw_query._IMAGES_URL + poster_url_field if poster_url_field else None
    backdrops = [jw_query._IMAGES_URL + bd.get("backdropUrl") for bd in content.get("backdrops", []) if bd]
    offers = [jw_query._parse_offer(offer) for offer in json.get("offers", []) if offer]
    return jw.MediaEntry(
        entry_id,
        object_id,
        object_type,
        title,
        url,
        year,
        date,
        runtime_minutes,
        short_description,
        genres,
        imdb_id,
        poster,
        backdrops,
        offers,
    )


def is_valid_title_response(response):
    return (
        "data" in response and
        response["data"] is not None and
        "urlV2" in response["data"] and
        "node" in response["data"]["urlV2"] and
        "content" in response["data"]["urlV2"]["node"]
    )


def parse_get_title_response(json):
    if not is_valid_title_response(json):
        return None
    return _parse_entry(json["data"]["urlV2"]["node"])


def get_title(url):
    if url is None:
        return None
    json = prepare_get_title_request(url)
    response = http.get_json(jw._GRAPHQL_API_URL, json,
                             validator=is_valid_title_response)
    return parse_get_title_response(response)
