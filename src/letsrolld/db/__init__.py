import os.path

from letsrolld.db import models  # noqa


def get_db_uri():
    return "sqlite:///" + os.path.join(os.getcwd(), "movie.db")


def create_tables(metadata, engine):
    metadata.create_all(engine)


def create_engine():
    from sqlalchemy import create_engine

    return create_engine(get_db_uri())
