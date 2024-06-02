#!/bin/sh
set -xe

StringContains() {
    string="$1"
    substring="$2"

    case "$string" in
        *"$substring"*)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

DIRECTORS_FILE=directors.csv

# create empty database
alembic upgrade head

# populate database with some data
populate-directors -d ${DIRECTORS_FILE} -n 2
update-directors
update-films
update-offers
cleanup

# start webapp
webapp &
WEBAPP_PID=$!
sleep 5

# check that it is running and returns some data
lines=$(lcli films get | wc -l)
test $lines -eq 10  # 10 is default in webapi

# we know which directors we fed into the database
# (the first two entries in the input file)
out=$(lcli directors get)
# TODO: we could probably extract these programmatically here
StringContains "$out" "Maryam Touzani"
StringContains "$out" "Štefan Uher"

# stop webapp
kill $WEBAPP_PID
