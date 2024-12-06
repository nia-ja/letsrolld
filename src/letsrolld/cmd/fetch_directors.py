import argparse
import csv
import os
import sys
import time
import traceback

from letsrolld import film
from letsrolld import filmlist
from letsrolld.directorlist import read_director_list

_SEC_WAIT_ON_FAIL = 5


def get_directors_by_films(film_list):
    film_list = film_list[:]

    directors = {}
    for i, film_ in enumerate(film_list):
        movie = film.Film(film_.uri)
        while True:
            try:
                for director in movie.directors:
                    if director.base_url not in directors:
                        directors[director.base_url] = director
                        yield director
                break
            except (
                Exception
            ) as e:  # TODO: deduplicate error handling with update script
                traceback.print_exception(e)
                print(f"Retrying in {_SEC_WAIT_ON_FAIL} seconds...")
                time.sleep(_SEC_WAIT_ON_FAIL)
                continue
        print(f"Processed {i + 1}/{len(film_list)} films")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input movie list file", required=True)
    parser.add_argument(
        "-o", "--output", help="output director list file", required=True
    )
    args = parser.parse_args()

    film_list = list(filmlist.read_film_list(args.input))

    directors = set()
    if os.path.exists(args.output):
        print(f"Output file {args.output} already exists, appending to it...")
        sys.stdout.flush()

        directors = {d.uri for d in read_director_list(args.output)}

    mode = "a" if directors else "w"
    with open(args.output, mode, newline="") as csvfile:
        writer = csv.writer(csvfile, dialect=csv.unix_dialect)
        if mode == "w":
            writer.writerow(["Name", "Letterboxd URI"])
        else:
            csvfile.seek(0, os.SEEK_END)

        for i, director_ in enumerate(get_directors_by_films(film_list), start=1):
            if director_.base_url in directors:
                print(f"Skipping director #{i}: {director_.name}")
                sys.stdout.flush()
                continue
            print(f"Adding director #{i}: {director_.name}")
            sys.stdout.flush()
            writer.writerow([director_.name, director_.base_url])
            csvfile.flush()
