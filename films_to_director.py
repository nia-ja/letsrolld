#!/usr/bin/env python3
import argparse
import csv

from letsrolld import http
from letsrolld import director
from letsrolld import filmlist


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="enable debug logging",
                        action='store_true')
    parser.add_argument("-i", "--input", help="input movie list file",
                        required=True)
    parser.add_argument("-o", "--output", help="output director list file",
                        required=True)
    args = parser.parse_args()

    if args.debug:
        http.enable_debug()

    film_list = list(filmlist.read_film_list(args.input))

    with open(args.output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Letterboxd URI"])

        for director_ in director.get_directors_by_films(film_list):
            writer.writerow([director_.name, director_.base_url])


if __name__ == "__main__":
    main()
