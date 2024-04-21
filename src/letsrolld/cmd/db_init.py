from letsrolld import db
from letsrolld.db import models


def main():
    engine = db.create_engine()
    db.create_tables(models.Base.metadata, engine)
