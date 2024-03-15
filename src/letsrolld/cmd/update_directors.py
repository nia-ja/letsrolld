import datetime
import sys

from sqlalchemy import func, select, or_
from sqlalchemy.orm import sessionmaker

from letsrolld import db
from letsrolld.db import models
from letsrolld import director as dir_obj


_NOW = datetime.datetime.now()
_THRESHOLD = datetime.timedelta(days=1)
_BASE_THRESHOLD = _NOW - _THRESHOLD


def _get_director_to_update_query():
    return or_(
        models.Director.last_checked < _BASE_THRESHOLD,
        models.Director.last_checked == None,  # noqa
    )


def get_director_to_update(session):
    return (
        session.execute(
            select(models.Director)
            .filter(_get_director_to_update_query())
            .limit(1)
        )
        .scalars()
        .first()
    )


def get_number_of_directors_to_update(session):
    try:
        return session.scalar(
            select(func.count())
            .select_from(models.Director)
            .filter(_get_director_to_update_query())
        )
    finally:
        session.close()


def get_objs(session, model, names):
    objs = []
    for name in names:
        db_obj = session.query(model).filter_by(name=name).first()
        objs.append(db_obj)
    return objs


def get_genres(session, genres):
    return get_objs(session, models.Genre, genres)


def get_countries(session, countries):
    return get_objs(session, models.Country, countries)


def update_objs(session, model, names):
    for name in names:
        db_obj = session.query(model).filter_by(name=name).first()
        if db_obj is not None:
            continue
        session.add(model(name=name))
        print(f"Adding {model.__name__.lower()}: {name}")


def update_genres(session, genres):
    update_objs(session, models.Genre, genres)


def update_countries(session, countries):
    update_objs(session, models.Country, countries)


def add_films(session, films):
    for f in films:
        print(f"Adding film: {f.name} @ {f.url}")
        session.add(
            models.Film(
                title=f.name,
                description=f.description,
                year=f.year,
                rating=f.rating,
                runtime=f.runtime,
                lb_url=f.url,
                jw_url=f.jw_url,
                genres=get_genres(session, f.genres),
                countries=get_countries(session, f.countries),
                last_updated=_NOW,
            )
        )


def get_db_film(session, url):
    return session.query(models.Film).filter_by(lb_url=url).first()


def get_db_films(session, films):
    for f in films:
        yield get_db_film(session, f.url)


def touch_director(session, director, updated=False):
    if updated:
        director.last_updated = _NOW
    director.last_checked = _NOW
    session.add(director)


def get_refresh_threshold_multiplier(d):
    multiplier = 1
    if d is None:
        return multiplier

    films = sorted(d.films, key=lambda f: f.year, reverse=True)

    current_year = _NOW.year
    for f in films[:2]:
        multiplier *= max(1, current_year - f.year)
        current_year = f.year

    return multiplier


def skip_director(director):
    if director.last_updated is not None:
        multiplier = get_refresh_threshold_multiplier(director)
        return _NOW - director.last_updated < _THRESHOLD * multiplier


def main():
    engine = db.create_engine()
    Session = sessionmaker(bind=engine)

    n_directors = get_number_of_directors_to_update(Session())

    i = 1

    def loop_housekeeping(session, director, updated=False):
        touch_director(session, director, updated=updated)
        session.commit()
        sys.stdout.flush()
        nonlocal i
        i += 1

    while True:
        session = Session()
        d = get_director_to_update(session)
        if d is None:
            break

        if skip_director(d):
            print(
                f"{i}/{n_directors}: Skipping director: {d.name} @ {d.lb_url}",
            )
            loop_housekeeping(session, d, updated=False)
            continue

        print(
            f"{i}/{n_directors}: Updating director: {d.name} @ {d.lb_url}",
            flush=True,
        )

        director_obj = dir_obj.Director(d.lb_url)
        films = list(director_obj.films())

        # don't refresh existing films here
        new_films = [
            f for f in films
            if not get_db_film(session, f.url)
        ]
        for f in new_films:
            update_genres(session, f.genres)
            update_countries(session, f.countries)

        add_films(session, new_films)
        d.films = list(get_db_films(session, films))

        loop_housekeeping(session, d, updated=True)

    print("No more directors to update")


if __name__ == "__main__":
    main()
