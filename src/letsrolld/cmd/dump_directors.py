import argparse
import csv
import os.path
import sys

from sqlalchemy.orm import sessionmaker

from letsrolld import db
from letsrolld.db import models


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="output directors file", required=True)
    parser.add_argument("-f", "--force", help="output directors file", type=bool)
    args = parser.parse_args()

    if not args.force and os.path.exists(args.output):
        print(f"Output file {args.output} already exists, exiting...")
        sys.exit(1)

    with open(args.output, "w") as csvfile:
        writer = csv.writer(csvfile, dialect=csv.unix_dialect)
        writer.writerow(["Name", "Letterboxd URI"])
        session = sessionmaker(bind=db.create_engine())()
        for director in session.query(models.Director).order_by(models.Director.name):
            writer.writerow([director.name, director.lb_url])


if __name__ == "__main__":
    main()
