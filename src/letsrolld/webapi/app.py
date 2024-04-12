from flask import Flask
from flask_restful_swagger_3 import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from letsrolld import db
from letsrolld.db import models

import logging

# TODO: actually define api as per:
# https://pypi.org/project/flask-restful-swagger-3/

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
logging.getLogger("sqlalchemy").setLevel(logging.DEBUG)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db.get_db_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # do I need this?

db_ = SQLAlchemy(app)


class DirectorResource(Resource):
    def get(self):
        return {
            "directors": [
                d.name for d in db_.session.query(models.Director).limit(10)
            ],
        }


class FilmResource(Resource):
    def get(self):
        return {
            "films": [
                d.name for d in db_.session.query(models.Film).limit(10)
            ],
        }


def main():
    api = Api(app)
    api.add_resource(DirectorResource, "/directors")
    api.add_resource(FilmResource, "/films")

    app.run(port=8000, debug=True)
