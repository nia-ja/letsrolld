import argparse
import csv

from letsrolld import http
from letsrolld import director
from letsrolld import filmlist


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-D", "--debug", help="enable debug logging", action="store_true"
    )
    parser.add_argument(
        "-i", "--input", help="input movie list file", required=True
    )
    parser.add_argument(
        "-o", "--output", help="output director list file", required=True
    )
    parser.add_argument(
        "-a", "--append", action="store_true", help="append to output file"
    )
    args = parser.parse_args()

    if args.debug:
        http.enable_debug()

    film_list = list(filmlist.read_film_list(args.input))

    director_list = []
    if args.append is not None:
        with open(args.output, "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            director_list = [row[0] for row in reader]

    mode = "w" if args.append is None else "a"
    with open(args.output, mode, newline="") as csvfile:
        writer = csv.writer(csvfile)
        if args.append is None:
            writer.writerow(["Name", "Letterboxd URI"])

        for i, director_ in enumerate(
            director.get_directors_by_films(film_list), start=1
        ):
            if director_.name in director_list:
                continue
            print(f"Processing director #{i}: {director_.name}")
            writer.writerow([director_.name, director_.base_url])
            csvfile.flush()
