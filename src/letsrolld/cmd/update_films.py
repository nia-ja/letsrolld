import datetime
import sys

from sqlalchemy import func, select, or_
from sqlalchemy.orm import sessionmaker

from letsrolld import db
from letsrolld.db import models
from letsrolld import director as dir_obj


_THRESHOLD = datetime.timedelta(days=30)


def _get_director_to_update_query():
    time_threshold = datetime.datetime.now() - _THRESHOLD
    return or_(
        models.Director.last_updated < time_threshold,
        models.Director.last_updated == None,  # noqa
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


def update_films(session, films):
    now = datetime.datetime.now()
    for f in films:
        db_obj = session.query(models.Film).filter_by(lb_url=f.url).first()
        if db_obj is not None:
            continue
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
                last_updated=now,
            )
        )


def touch_director(session, director):
    director.last_updated = datetime.datetime.now()
    session.add(director)


def main():
    engine = db.create_engine()
    Session = sessionmaker(bind=engine)

    n_directors = get_number_of_directors_to_update(Session())

    i = 1
    while True:
        session = Session()
        d = get_director_to_update(session)
        if d is None:
            break

        print(
            f"{i}/{n_directors}: Updating director: {d.name} @ {d.lb_url}",
            flush=True,
        )

        session.rollback()

        director_obj = dir_obj.Director(d.lb_url)
        films = list(director_obj.films())

        for f in films:
            update_genres(session, f.genres)
            update_countries(session, f.countries)

        update_films(session, films)
        touch_director(session, d)

        session.commit()

        sys.stdout.flush()

        i += 1

    print("No more directors to update")


if __name__ == "__main__":
    main()
