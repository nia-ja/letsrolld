from flask_restful_swagger_3 import Schema


class NullableURL(Schema):
    type = "string"
    format = "url"
    nullable = True


class URL(Schema):
    type = "string"
    format = "url"


class Genre(Schema):
    type = "string"


class Country(Schema):
    type = "string"


class Offer(Schema):
    type = "string"


class DirectorInfo(Schema):
    properties = {
        "id": {
            "type": "integer",
            "format": "int64",
        },
        "name": {"type": "string"},
        "lb_url": URL,
    }
    required = ["id", "name"]


class Film(Schema):
    properties = {
        "id": {
            "type": "integer",
            "format": "int64",
        },
        "title": {"type": "string"},
        "description": {"type": "string"},
        "year": {
            "type": "integer",
            "format": "int64",
            "nullable": True,
        },
        "rating": {
            "type": "string",
        },
        "runtime": {
            "type": "integer",
            "format": "int64",
        },
        "lb_url": URL,
        "jw_url": NullableURL,
        "genres": Genre.array(),
        "countries": Country.array(),
        "offers": Offer.array(),
        "directors": DirectorInfo.array(),
    }
    required = ["title"]


class Director(Schema):
    properties = {
        "info": DirectorInfo,
        "films": Film.array(),
    }
    required = ["info"]


class ArrayOfDirectors(Schema):
    type = "array"
    properties = Director.properties
    items = Director


class ArrayOfFilms(Schema):
    type = "array"
    properties = Film.properties
    items = Film
