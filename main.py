import argparse
import random
from decimal import Decimal

from letsrolld import http
from letsrolld import watchlist
from letsrolld import film


# TODO: filter by length


def already_seen(seen, film):
    for s in seen:
        if s.name == film.name and s.year == film.year:
            return True
    return False


def get_movies(directors, min_rating=Decimal("4.0"),
               max_movies=5, max_per_director=1):
    movies = []

    for director in directors:
        if len(movies) >= max_movies:
            break

        file_name = 'watched.csv'
        watched_list = list(watchlist.read_watch_list(file_name))

        print(f'Getting movies for {director.name}...')
        films = (
            f for f in director.films()
            # filter out films that I saw
            if not already_seen(watched_list, f)
        )

        # print first max films by rating
        added_for_this_director = 0
        movie_candidates = []
        for movie in films:
            if any(movie == m for m in movies):
                continue
            if Decimal(movie.rating) < min_rating:
                break
            if added_for_this_director >= max_per_director * 3:
                break
            movie_candidates.append(movie)
            added_for_this_director += 1

        if movie_candidates:
            random.shuffle(movie_candidates)
            movies.append(movie_candidates[0])

    return movies


def get_directors(watch_list):
    watch_list = watch_list[:]
    random.shuffle(watch_list)

    directors = {}
    for wle in watch_list:
        movie = film.Film(wle.uri)
        for director in movie.directors:
            if director.url not in directors:
                directors[director.url] = director
                yield director


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="enable debug logging",
                        action='store_true')
    args = parser.parse_args()

    if args.debug:
        http.enable_debug()

    file_name = 'watchlist.csv'
    watch_list = list(watchlist.read_watch_list(file_name))
    random.shuffle(watch_list)

    movies = get_movies(get_directors(watch_list), max_movies=5)
    print("\n--------------------\n")

    for movie in sorted(movies, key=lambda m: m.rating, reverse=True):
        print(f'{movie.name} - {movie.runtime} - {movie.rating} - '
              f'{movie.director_names}')
        print(f'  Letterboxd: {movie.url}')
        available = ", ".join(s for s in film.SERVICES if movie.available(s))
        print(f'  Available: {available}')
        print()


if __name__ == '__main__':
    main()
