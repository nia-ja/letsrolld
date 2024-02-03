#!/usr/bin/env python3
import argparse
import random
from decimal import Decimal
import textwrap

from letsrolld.colors import colorize, red, green, blue, bold

from letsrolld import http
from letsrolld import director
from letsrolld import directorlist
from letsrolld import film
from letsrolld import filmlist


_DEFAULT_NUM_MOVIES = 5
_DEFAULT_NUM_MOVIES_PER_DIRECTOR = 1
_DEFAULT_MIN_LENGTH = 60
_DEFAULT_MAX_LENGTH = 240
_DEFAULT_MIN_RATING = Decimal("4.0")

_PROFILE = False


def already_seen(seen, film):
    for s in seen:
        if s.name == film.name and s.year == film.year:
            return True
    return False


def get_movies(directors, min_rating=_DEFAULT_MIN_RATING,
               max_movies=_DEFAULT_NUM_MOVIES,
               max_per_director=_DEFAULT_NUM_MOVIES_PER_DIRECTOR,
               min_length=_DEFAULT_MIN_LENGTH,
               max_length=_DEFAULT_MAX_LENGTH,
               genre=None, services=None):
    movies = []

    services = film.get_services(services)

    for i, director_ in enumerate(directors, start=1):
        if len(movies) >= max_movies:
            break

        # TODO: make this input configurable?
        file_name = 'watched.csv'
        watched_list = list(filmlist.read_film_list(file_name))

        print(f'({len(movies)}/{max_movies}) '
              f'{i}: Getting movies for {director_.name}...')
        films = (
            f for f in director_.films()
            # filter out films that I saw
            if not already_seen(watched_list, f)
        )

        # print first max films by rating
        added_for_this_director = 0
        movie_candidates = []
        for movie in films:
            if Decimal(movie.rating) < min_rating:
                break
            if any(movie == m for m in movies):
                continue
            if movie.runtime < min_length:
                continue
            if movie.runtime > max_length:
                continue
            if genre is not None and genre not in movie.genres:
                continue
            if services and not any(movie.available(s) for s in services):
                continue
            if added_for_this_director >= max_per_director * 3:
                break
            movie_candidates.append(movie)
            added_for_this_director += 1

        if movie_candidates:
            random.shuffle(movie_candidates)
            movies.append(movie_candidates[0])
            print(green(
                f'  Added {movie_candidates[0].name} by {director_.name}'
            ))

    return movies


def get_colored_service(service):
    color = blue
    if service == film.PHYSICAL:
        color = red
    elif service in film.SERVICE_ALIASES["FREE"]:
        color = green
    return color(service)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-D", "--debug", help="enable debug logging",
                        action='store_true')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', '--movies', help="input movie list file")
    group.add_argument('-d', '--directors', help="input director list file")
    parser.add_argument('-g', '--genre', help="filter by genre")
    parser.add_argument('-s', '--service', action="append",
                        help="filter by services")
    parser.add_argument('-n', '--num', type=int,
                        help="number of movies to get")
    parser.add_argument('-N', '--director-num', type=int,
                        help="number of movies per director to get")
    parser.add_argument('-l', '--min-length', type=int,
                        help="minimum length of movie in minutes")
    parser.add_argument('-L', '--max-length', type=int,
                        help="maximum length of movie in minutes")
    parser.add_argument('-R', '--min-rating', type=Decimal,
                        help="minimum movie rating")
    # TODO: add preseed option
    args = parser.parse_args()

    if args.debug:
        http.enable_debug()

    if args.movies:
        film_list = list(filmlist.read_film_list(args.movies))
        random.shuffle(film_list)
        directors = director.get_directors_by_films(film_list)
    else:
        directors = director.get_directors_by_urls(
            list(directorlist.read_director_list(args.directors)))

    movies = get_movies(
        directors,
        min_rating=args.min_rating or _DEFAULT_MIN_RATING,
        max_movies=args.num or _DEFAULT_NUM_MOVIES,
        max_per_director=args.director_num or _DEFAULT_NUM_MOVIES_PER_DIRECTOR,
        min_length=args.min_length or _DEFAULT_MIN_LENGTH,
        max_length=args.max_length or _DEFAULT_MAX_LENGTH,
        services=args.service, genre=args.genre)
    print("\n--------------------\n")

    for movie in sorted(movies,
                        key=lambda m: m.rating, reverse=True):
        print(f'{bold(movie.name)} | 📅:{movie.year} | '
              f'📽:{movie.director_names}')
        print(f'- ⌛:{movie.runtime_string} - ⭐:{movie.rating} - '
              f'📎:{movie.genre_names}')
        print(f'  Letterboxd: {movie.url or ""}')
        print(f'  QuickWatch: {movie.jw_url or ""}')
        for line in textwrap.wrap(movie.description):
            print(bold(f'  | {line}'))
        available = ", ".join(
            get_colored_service(s)
            for s in film.SERVICES
            if movie.available(s)
        )
        print(f'  Available: {available}')
        print()


if __name__ == '__main__':
    if _PROFILE:
        import cProfile
        cProfile.run('main()', sort='cumulative')
    else:
        main()
