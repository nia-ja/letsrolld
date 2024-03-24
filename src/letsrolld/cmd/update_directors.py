import argparse
import datetime
import math
import sys
import time
import traceback

from sqlalchemy import func, select, or_
from sqlalchemy.orm import sessionmaker

from letsrolld import db
from letsrolld.db import models
from letsrolld import director as dir_obj
from letsrolld import film as film_obj


_SEC_WAIT_ON_FAIL = 5


_NOW = datetime.datetime.now()


_MODEL_TO_THRESHOLD = {
    models.Film: 7,
    models.Director: 1,
}


def _get_obj_to_update_query(model, threshold):
    return or_(
        model.last_checked < _NOW - threshold,
        model.last_checked > _NOW,
        model.last_checked == None,  # noqa
    )


def _seen_obj_query(model, seen):
    return model.id.notin_(seen)


def get_obj_to_update(session, model, threshold, seen):
    return (
        session.execute(
            select(model)
            .filter(_get_obj_to_update_query(model, threshold))
            .filter(_seen_obj_query(model, seen))
            .limit(1)
        )
        .scalars()
        .first()
    )


def get_number_of_objs_to_update(session, model, threshold):
    try:
        return session.scalar(
            select(func.count())
            .select_from(model)
            .filter(_get_obj_to_update_query(model, threshold))
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


def get_offers(session, offers):
    return get_objs(session, models.Offer, offers)


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


def update_offers(session, offers):
    update_objs(session, models.Offer, offers)


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
    obj.last_updated = min(_NOW, obj.last_updated)
    obj.last_checked = _NOW
    session.add(obj)


def director_threshold(d):
    multiplier = 1
    if d is None:
        return multiplier

    films = sorted(d.films, key=lambda f: f.year, reverse=True)

    current_year = _NOW.year
    for f in films[:2]:
        multiplier *= max(1, current_year - f.year)
        current_year = f.year

    return multiplier


def film_threshold(f):
    multiplier = 1
    if f is None:
        return multiplier

    multiplier = max(0, _NOW.year - f.year) + 1
    return min(100, multiplier)


def skip_obj(obj, threshold_func, threshold):
    if obj.last_updated:
        return _NOW - min(_NOW, obj.last_updated) <= threshold * threshold_func(obj)
    return False


def refresh_director(session, db_obj, api_obj):
    films = list(api_obj.films())

    # don't refresh existing films here
    new_films = [f for f in films if not get_db_film(session, f.url)]
    add_films(session, new_films)
    db_obj.films = list(get_db_films(session, films))


def refresh_film(session, db_obj, api_obj):
    # just in case genres or countries or offers changed
    update_genres(session, api_obj.genres)
    update_countries(session, api_obj.countries)
    update_offers(session, api_obj.available_services)

    if not math.isclose(float(api_obj.rating), db_obj.rating):
        print(
            f"\t{db_obj.rating:.3f} -> {api_obj.rating}"
        )

    offers = get_offers(session, api_obj.available_services)
    old = set(o.name for o in db_obj.offers) - set(api_obj.available_services)
    new = set(api_obj.available_services) - set(o.name for o in db_obj.offers)
    if new or old:
        for o in new:
            print(f"\t+ {o}")
        for o in old:
            print(f"\t- {o}")

    db_obj.title = api_obj.name
    db_obj.description = api_obj.description
    db_obj.year = api_obj.year
    db_obj.rating = api_obj.rating
    db_obj.runtime = api_obj.runtime
    db_obj.jw_url = api_obj.jw_url
    db_obj.genres = get_genres(session, api_obj.genres)
    db_obj.countries = get_countries(session, api_obj.countries)
    db_obj.offers = offers
    db_obj.last_updated = _NOW


def run_update(session, model, api_cls, refresh_func, threshold_func, threshold, dry_run=False):
    model_name = model.__name__
    threshold = datetime.timedelta(days=threshold)

    n_objs = get_number_of_objs_to_update(session, model, threshold)

    i = 1
    seen = set()

    def maybe_commit():
        if dry_run:
            session.rollback()
        else:
            session.commit()

    def loop_housekeeping(session, obj, updated=False):
        touch_obj(session, obj, updated=updated)
        if dry_run:
            # build the list of seen objects only when we cannot rely on
            # last_checked fields in db
            seen.add(obj.id)
        maybe_commit()
        sys.stdout.flush()
        nonlocal i
        i += 1

    while True:
        obj = get_obj_to_update(session, model, threshold, seen)
        if obj is None:
            break

        if skip_obj(obj, threshold_func, threshold):
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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main(model, api_cls, refresh_func, threshold_func):
    args = parse_args()
    while True:
        try:
            threshold = 0 if args.force else _MODEL_TO_THRESHOLD[model]
            run_update(
                sessionmaker(bind=db.create_engine())(),
                model, api_cls, refresh_func, threshold_func, threshold,
                dry_run=args.dry_run
            )
            break
        except Exception as e:
            traceback.print_exception(e)
            print(f"Retrying in {_SEC_WAIT_ON_FAIL} seconds...")
            time.sleep(_SEC_WAIT_ON_FAIL)
            continue


def directors_main():
    main(models.Director, dir_obj.Director,
         refresh_director, director_threshold)


def films_main():
    main(models.Film, film_obj.Film,
         refresh_film, film_threshold)
