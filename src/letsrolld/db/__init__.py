from letsrolld.db import models  # noqa

DB_URL = "sqlite:///movie.db"


def create_tables(metadata, engine):
    metadata.create_all(engine)


def create_engine():
    from sqlalchemy import create_engine

    return create_engine(DB_URL)
