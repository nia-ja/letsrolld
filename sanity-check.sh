#!/bin/sh

DIRECTORS_FILE=directors.csv

alembic upgrade head

populate-directors -d ${DIRECTORS_FILE} -n 2
update-directors
update-films
update-offers

cleanup

# TODO: check that the db has some records
