#!/bin/bash
set -xe

StringContains() {
    string="$1"
    substring="$2"

    if grep -q "$substring" <<< "$string"; then
        return 0
    fi
    return 1
}

DIRECTORS_FILE=directors.csv

git worktree add ../sanity-check-env
trap "git worktree remove ../sanity-check-env" EXIT

cd ../sanity-check-env

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
trap 'kill $WEBAPP_PID; git worktree remove ../sanity-check-env' EXIT
sleep 5

# check that it is running and returns some data
lines=$(lcli films get | wc -l)
test "$lines" -eq 10  # 10 is default in webapi

# we know which directors we fed into the database
# (the first two entries in the input file)
out=$(lcli directors get)
# TODO: we could probably extract these programmatically here
StringContains "$out" "Maryam Touzani"
StringContains "$out" "Štefan Uher"

# TODO: support structured output for cli, then use it to extract values
out=$(lcli films query --limit 1 --genre drama --offer criterionchannel)
StringContains "$out" "criterionchannel"
StringContains "$out" "drama"
StringContains "$out" ">>>"
StringContains "$out" '⌛:[[:space:]]' && exit 1

exit 0
