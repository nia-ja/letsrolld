import argparse

from sqlalchemy.orm import sessionmaker

from letsrolld import db
from letsrolld.db import models


def get_orphaned_films(session, model, dry_run=False):
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
        models.Film,
        get_orphaned_films,
    )
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
