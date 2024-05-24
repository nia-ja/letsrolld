#!/bin/sh

# DB?=movie.db
DIRECTORS_FILE=directors.csv

# TODO: make db-init create a new db file, if missing
# touch $(DB)
# sqlite3 $(DB) "VACUUM;"
# db-init
alembic upgrade head

populate-directors -d ${DIRECTORS_FILE} -n 2

update-directors
update-films
update-offers

cleanup

# TODO: check that the db has some records
