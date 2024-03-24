IMAGE_NAME?=letsrolld
DB=$(PWD)/movie.db

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
	test -f $(DB) || (touch $(DB) && sqlite3 $(DB) "VACUUM;")

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
