import argparse
import itertools as it
import os.path
import sys

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from letsrolld import db
from letsrolld.db import models
from letsrolld.directorlist import read_director_list


def create_directors(engine, directors):
    for d in directors:
        session = sessionmaker(bind=engine)()
        session.add(models.Director(name=d.name, lb_url=d.uri))
        try:
            session.commit()
            print(f"Added director {d.name} @ {d.uri}")
        except sqlalchemy.exc.IntegrityError:
            session.rollback()
            print(f"Skipping director {d.name} @ {d.uri}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--directors", help="input directors file", required=True
    )
    parser.add_argument(
        "-n", "--num", help="max number of directors to add", type=int
    )
    args = parser.parse_args()

    if not os.path.exists(args.directors):
        print(f"File {args.directors} does not exist")
        sys.exit(1)

    directors = read_director_list(args.directors)
    if args.num:
        directors = it.islice(directors, args.num)
    create_directors(db.create_engine(), directors)


if __name__ == "__main__":
    main()
