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


def _get_obj_to_update_query(model):
    return or_(
        model.last_checked < _BASE_THRESHOLD,
        model.last_checked == None,  # noqa
    )


def get_obj_to_update(session, model):
    return (
        session.execute(
            select(model).filter(_get_obj_to_update_query(model)).limit(1)
        )
        .scalars()
        .first()
    )


def get_number_of_objs_to_update(session, model):
    try:
        return session.scalar(
            select(func.count())
            .select_from(model)
            .filter(_get_obj_to_update_query(model))
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


def touch_obj(session, obj, updated=False):
    if updated:
        obj.last_updated = _NOW
    obj.last_checked = _NOW
    session.add(obj)


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


def skip_obj(obj):
    if obj.last_updated is not None:
        multiplier = get_refresh_threshold_multiplier(obj)
        return _NOW - obj.last_updated < _THRESHOLD * multiplier


def refresh_director(session, db_obj, api_obj):
    films = list(api_obj.films())

    # don't refresh existing films here
    new_films = [f for f in films if not get_db_film(session, f.url)]
    for f in new_films:
        update_genres(session, f.genres)
        update_countries(session, f.countries)

    add_films(session, new_films)
    db_obj.films = list(get_db_films(session, films))


_UPDATES = [
    (models.Director, dir_obj.Director, refresh_director),
]


def run_update(session, update):
    model, api_cls, refresh_func = update
    model_name = model.__name__

    n_objs = get_number_of_objs_to_update(session, model)

    i = 1

    def loop_housekeeping(session, obj, updated=False):
        touch_obj(session, obj, updated=updated)
        session.commit()
        sys.stdout.flush()
        nonlocal i
        i += 1

    while True:
        obj = get_obj_to_update(session, model)
        if obj is None:
            break

        if skip_obj(obj):
            print(
                f"{i}/{n_objs}: Skipping {model_name}: "
                f"{obj.name} @ {obj.lb_url}",
            )
            loop_housekeeping(session, obj, updated=False)
            continue

        print(
            f"{i}/{n_objs}: Updating {model_name}: {obj.name} @ {obj.lb_url}",
            flush=True,
        )

        api_obj = api_cls(obj.lb_url)
        refresh_func(session, obj, api_obj)

        loop_housekeeping(session, obj, updated=True)

    # TODO: is there a better way to extract plural names?
    print(f"No more {model_name}s to update")


def main():
    engine = db.create_engine()
    for update in _UPDATES:
        run_update(sessionmaker(bind=engine)(), update)


if __name__ == "__main__":
    main()
