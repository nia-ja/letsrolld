IMAGE_NAME?=letsrolld
DB=$(PWD)/movie.db
DIRECTORS_NUMBER?=10
DIRECTORS_FILE?=directors.csv

ifndef VERBOSE
.SILENT:
endif

install:
	pdm install -v

lint: install
	pre-commit run --all-files

test: lint
	pdm run pytest

init_db:
	test -f $(DB) || (touch $(DB) && sqlite3 $(DB) "VACUUM;" && pdm run db-init)

populate:
	pdm run populate-directors -d ${DIRECTORS_FILE} -n ${DIRECTORS_NUMBER}

run-update-directors: init_db
	pdm run update-directors $(ARGS)

run-update-films: init_db
	pdm run update-films $(ARGS)

run-update-offers: init_db
	pdm run update-offers $(ARGS)

run-cleanup: init_db
	pdm run cleanup $(ARGS)

run-all: run-update-directors run-update-films run-update-offers run-cleanup

run-db-upgrade:
	pdm run alembic upgrade head

webapp: init_db
	pdm run webapp

get-dirs:
	pdm run lcli directors get

get-films:
	pdm run lcli films get
