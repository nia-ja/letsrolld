from letsrolld import db


def main():
    engine = db.create_engine()
    db.create_tables(engine)
