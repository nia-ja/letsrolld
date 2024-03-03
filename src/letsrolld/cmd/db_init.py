from letsrolld import db


def main():
    engine = db.create_engine()
    db.create_tables(engine)


if __name__ == "__main__":
    main()
