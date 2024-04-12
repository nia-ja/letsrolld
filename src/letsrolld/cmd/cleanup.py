import argparse

from sqlalchemy.orm import sessionmaker

from letsrolld import db
from letsrolld.db import models


_REDIRECT_LB_PREFIX = "https://www.letterboxd.com"
_NORMALIZED_LB_PREFIX = _REDIRECT_LB_PREFIX.replace("www.", "")


def lb_obj_exists(session, model, lb_url):
    q = session.query(model).filter(model.lb_url == lb_url)
    return session.query(q.exists()).scalar()


def normalize_lb_url(lb_url):
    return lb_url.replace(_REDIRECT_LB_PREFIX, _NORMALIZED_LB_PREFIX)


def shorten_lb_urls(session, model, dry_run=False):
    try:
        for obj in (
            session.query(model)
            .filter(model.lb_url.startswith(_REDIRECT_LB_PREFIX))
            .all()
        ):
            new_url = normalize_lb_url(obj.lb_url)
            if lb_obj_exists(session, model, new_url):
                print(f"Deleting duplicate {obj.lb_url}")
                session.delete(obj)
            else:
                print(f"Updating lb_url for {obj.lb_url}")
                obj.lb_url = new_url
                session.add(obj)
    finally:
        if not dry_run:
            session.commit()
        else:
            session.rollback()


def delete_orphaned_films(session, model, dry_run=False):
    try:
        for film in session.query(model).all():
            if not film.directors:
                print(f"Deleting orphaned film: {film.name} @ {film.lb_url}")
                session.delete(film)
    finally:
        if not dry_run:
            session.commit()
        else:
            session.rollback()


_CLEANUP = [
    (
        models.Director,
        shorten_lb_urls,
    ),
    (
        models.Film,
        shorten_lb_urls,
    ),
    (
        models.Film,
        delete_orphaned_films,
    ),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    engine = db.create_engine()

    for cleanup in _CLEANUP:
        model, cleanup_func = cleanup
        cleanup_func(sessionmaker(bind=engine)(), model, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
