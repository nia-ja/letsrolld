from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from letsrolld import db
from letsrolld.db import models

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db.get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # do I need this?

db_ = SQLAlchemy(app)


class DirectorResource(Resource):
    def get(self):
        return {
            "directors": [
                d.name for d in db_.session.query(models.Director).all()
            ],
        }


class FilmResource(Resource):
    def get(self):
        return {
            "films": [
                d.name for d in db_.session.query(models.Film).all()
            ],
        }


def main():
    api = Api(app)
    api.add_resource(DirectorResource, '/directors')
    api.add_resource(FilmResource, '/films')

    app.run(port=8000, debug=True)
