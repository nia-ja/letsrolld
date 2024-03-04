import argparse
import os.path
import sys

from sqlalchemy.orm import sessionmaker

from letsrolld import db
from letsrolld.db import models
from letsrolld.directorlist import read_director_list


def batch(iterable, n=1):
    buffer = []
    for item in iterable:
        buffer.append(item)
        if len(buffer) >= n:
            yield buffer
            buffer = []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--directors", help="input directors file", required=True
    )
    args = parser.parse_args()

    if not os.path.exists(args.directors):
        print(f"File {args.directors} does not exist")
        sys.exit(1)

    engine = db.create_engine()
    for directors in batch(read_director_list(args.directors), n=10):
        session = sessionmaker(bind=engine)()
        session.add_all(
            models.Director(name=d.name, lb_url=d.uri) for d in directors
        )
        session.commit()

        for d in directors:
            print(f"Added director {d.name} @ {d.uri}")


if __name__ == "__main__":
    main()
