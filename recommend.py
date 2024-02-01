#!/usr/bin/env python3
import argparse
import random
from decimal import Decimal

from letsrolld import http
from letsrolld import filmlist
from letsrolld import film
from letsrolld import director


def already_seen(seen, film):
    for s in seen:
        if s.name == film.name and s.year == film.year:
            return True
    return False


# TODO: make parameters configurable
def get_movies(directors, min_rating=Decimal("4.0"),
               max_movies=5, max_per_director=1,
               min_length=60):
    movies = []

    for director_ in directors:
        if len(movies) >= max_movies:
            break

        file_name = 'watched.csv'
        watched_list = list(filmlist.read_film_list(file_name))

        print(f'Getting movies for {director_.name}...')
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
            if added_for_this_director >= max_per_director * 3:
                break
            movie_candidates.append(movie)
            added_for_this_director += 1

        if movie_candidates:
            random.shuffle(movie_candidates)
            movies.append(movie_candidates[0])

    return movies


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-D", "--debug", help="enable debug logging",
                        action='store_true')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', '--movies', help="input movie list file")
    group.add_argument('-d', '--directors', help="input director list file")
    args = parser.parse_args()

    if args.debug:
        http.enable_debug()

    film_list = list(filmlist.read_film_list(args.movies))
    random.shuffle(film_list)

    movies = get_movies(director.get_directors_by_films(film_list),
                        max_movies=5)
    print("\n--------------------\n")

    for movie in sorted(movies, key=lambda m: m.rating, reverse=True):
        print(f'{movie.name} | y:{movie.year} | by:{movie.director_names}')
        print(f'- time:{movie.runtime_string} - rated:{movie.rating} - '
              f'genres:{movie.genre_names}')
        print(f'  Letterboxd: {movie.url}')
        print(f'  > {movie.description}')
        available = ", ".join(s for s in film.SERVICES if movie.available(s))
        print(f'  Available: {available}')
        print()


if __name__ == '__main__':
    main()
