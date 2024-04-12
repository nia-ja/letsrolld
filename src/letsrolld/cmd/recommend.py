#!/usr/bin/env python3
import argparse
import random
from decimal import Decimal
import textwrap

from letsrolld import config
from letsrolld import director
from letsrolld import directorlist
from letsrolld import film
from letsrolld import filmlist


# TODO: make it a command line option
_PROFILE = False

# TODO: make this input configurable?
_WATCHED_FILE = "data/watched.csv"
_DIRECTORS_FILE = "directors.csv"


def is_good_candidate(movie, cfg):
    services = film.get_services(cfg.services)

    # TODO: reimplement filters as 1st class functions
    if cfg.min_rating or cfg.max_rating:
        rating = Decimal(movie.rating)
        if cfg.min_rating and rating < cfg.min_rating:
            return False
        if cfg.max_rating and rating > cfg.max_rating:
            return False
    if cfg.min_year or cfg.max_year:
        year = int(movie.year)
        if cfg.min_year and year < cfg.min_year:
            return False
        if cfg.max_year and year > cfg.max_year:
            return False
    if movie.runtime < cfg.min_length:
        return False
    if movie.runtime > cfg.max_length:
        return False
    if cfg.genre is not None and cfg.genre not in movie.genres:
        return False
    if cfg.exclude_genre is not None:
        if set(cfg.exclude_genre).intersection(movie.genres):
            return False
    if cfg.country is not None and cfg.country not in movie.countries:
        return False
    if cfg.exclude_country is not None:
        if set(cfg.exclude_country).intersection(movie.countries):
            return False
    if services:
        if not any(movie.available(s) for s in services):
            return False
    if cfg.text:
        if not (
            cfg.text in movie.description.lower()
            or cfg.text in movie.name.lower()
        ):
            return False
    return True


def get_movies(directors, cfg, exclude_movies):
    movies = []

    movies_to_find = cfg.max_movies_per_director * 10
    for i, director_ in enumerate(directors, start=1):
        # found enough movies
        if len(movies) >= cfg.max_movies:
            break

        films = (
            f
            for f in director_.films()
            # filter out films that I saw
            if f.name not in exclude_movies
            or f.year not in exclude_movies[f.name]
        )

        # print first max films by rating
        added_for_this_director = 0
        movie_candidates = []
        for movie in films:
            rating = Decimal(movie.rating)
            if cfg.min_rating and rating < cfg.min_rating:
                break
            if any(movie == m for m in movies):
                continue
            if not is_good_candidate(movie, cfg):
                continue
            if added_for_this_director >= movies_to_find:
                break
            movie_candidates.append(movie)
            added_for_this_director += 1

        random.shuffle(movie_candidates)
        for _ in range(
            min(
                cfg.max_movies_per_director,
                len(movie_candidates),
                cfg.max_movies - len(movies),
            )
        ):
            movies.append(movie_candidates.pop())

    return movies


def get_directors(movies, directors):
    if movies:
        film_list = list(filmlist.read_film_list(movies))
        random.shuffle(film_list)
        return list(director.get_directors_by_films(film_list))
    else:
        return list(
            director.get_directors_by_urls(
                list(directorlist.read_director_list(directors))
            )
        )


def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="config file to use")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-m", "--movies", help="input movie list file")
    group.add_argument("-d", "--directors", help="input director list file")

    parser.add_argument("-g", "--genre", help="filter by genre")
    parser.add_argument(
        "-G", "--exclude-genre", action="append", help="exclude genre"
    )

    parser.add_argument("-c", "--country", help="filter by country")
    parser.add_argument(
        "-C", "--exclude-country", action="append", help="exclude country"
    )

    parser.add_argument(
        "-s", "--service", action="append", help="filter by services"
    )

    parser.add_argument(
        "-n", "--max-movies", type=int, help="number of movies to get"
    )
    parser.add_argument(
        "-N",
        "--max-movies-per-director",
        type=int,
        help="number of movies per director to get",
    )

    parser.add_argument(
        "-l",
        "--min-length",
        type=int,
        help="minimum length of movie in minutes",
    )
    parser.add_argument(
        "-L",
        "--max-length",
        type=int,
        help="maximum length of movie in minutes",
    )

    parser.add_argument(
        "-r", "--min-rating", type=Decimal, help="minimum movie rating"
    )
    parser.add_argument(
        "-R", "--max-rating", type=Decimal, help="maximum movie rating"
    )

    parser.add_argument(
        "-y", "--min-year", type=int, help="minimum movie year"
    )
    parser.add_argument(
        "-Y", "--max-year", type=int, help="maximum movie year"
    )

    parser.add_argument("-t", "--text", help="search for text")
    # TODO: add preseed option
    args = parser.parse_args()

    if args.min_year and args.max_year and args.min_year > args.max_year:
        parser.error("min year must be less than or equal to max year")

    if (
        args.min_rating
        and args.max_rating
        and args.min_rating > args.max_rating
    ):
        parser.error("min rating must be less than or equal to max rating")

    if args.config:
        try:
            cfgs = list(config.Config.from_file(args.config))
        except FileNotFoundError:
            parser.error(f"config file {args.config} not found")
        except ValueError as e:
            parser.error(f"config file {args.config} is invalid: {e}")
    else:
        cfgs = [
            config.Config(
                name="cli",
                max_movies=args.max_movies,
                max_movies_per_director=args.max_movies_per_director,
                min_length=args.min_length,
                max_length=args.max_length,
                min_rating=args.min_rating,
                max_rating=args.max_rating,
                min_year=args.min_year,
                max_year=args.max_year,
                genre=args.genre,
                exclude_genre=args.exclude_genre,
                country=args.country,
                exclude_country=args.exclude_country,
                services=args.service,
                text=args.text,
            ),
        ]

    directors = args.directors or _DIRECTORS_FILE
    return args.movies, directors, cfgs


def report_movie(i, movie):
    print(f"{i}: {movie.name} | 📅:{movie.year} | 📽:{movie.director_names}")
    print(
        f"- ⌛:{movie.runtime_string} - ⭐:{movie.rating} - "
        f"📎:{movie.genre_names}"
    )
    if movie.countries:
        print(f'  Countries: {", ".join(movie.countries)}')
    if movie.url:
        print(f"  Letterboxd: {movie.url}")
    if movie.jw_url:
        print(f"  QuickWatch: {movie.jw_url}")
    if movie.trailer_url:
        print(f"  Trailer: {movie.trailer_url}")
    if movie.description:
        for line in textwrap.wrap(movie.description):
            print(f"  | {line}")
    available = ", ".join(s for s in film.SERVICES if movie.available(s))
    print(f"  Available: {available}")
    print()


def report(directors, cfg, exclude_movies):
    print(cfg.name)

    movies = get_movies(directors, cfg, exclude_movies)
    for i, movie in enumerate(
        sorted(movies, key=lambda m: m.rating, reverse=True), start=1
    ):
        report_movie(i, movie)
    return movies


def main():
    if _PROFILE:
        import cProfile

        cProfile.run("main()", sort="cumulative")

    movies, directors, cfgs = get_config()

    # one would think that this could be done with a set,
    # but it seems that performance is better with a dict.
    # Using a frozenset is better than a regular set,
    # but still slower.
    exclude_list = {}

    def _add_movie_to_exclude_list(movie):
        if movie.name not in exclude_list:
            exclude_list[movie.name] = [movie.year]
        else:
            exclude_list[movie.name].append(movie.year)

    for f in filmlist.read_film_list(_WATCHED_FILE):
        _add_movie_to_exclude_list(f)

    directors = get_directors(movies, directors)
    for cfg in cfgs:
        random.shuffle(directors)
        for movie in report(directors, cfg, exclude_movies=exclude_list):
            _add_movie_to_exclude_list(movie)


if __name__ == "__main__":
    main()
