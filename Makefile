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
	pytest

init_db:
	test -f $(DB) || (touch $(DB) && sqlite3 $(DB) "VACUUM;")

run-update-directors: init_db
	pdm run update-directors $(ARGS)

run-cleanup: init_db
	pdm run cleanup $(ARGS)

run-all: run-update-directors run-cleanup

run-db-upgrade:
	pdm run alembic upgrade head
