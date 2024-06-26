IMAGE_NAME?=letsrolld
DB=$(PWD)/movie.db
DIRECTORS_NUMBER?=10
DIRECTORS_FILE?=directors.csv
RUN_LOG?=run.log
RUN_LOG_CMD?=ts | tee -a $(RUN_LOG)

.PHONY: install lint test init_db populate run-update-directors run-update-films run-update-offers run-cleanup run-all run-db-upgrade webapp ui swagger get-dirs get-films

install:
	pdm install -v

lint: install swagger
	pre-commit run --all-files

test: lint
	pdm run pytest

init_db:
	test -f $(DB) || (touch $(DB) && sqlite3 $(DB) "VACUUM;" && pdm run db-init)

populate:
	pdm run populate-directors -d ${DIRECTORS_FILE} -n ${DIRECTORS_NUMBER}

run-update-directors: init_db
	pdm run update-directors $(ARGS) | $(RUN_LOG_CMD)

run-update-films: init_db
	pdm run update-films $(ARGS) | $(RUN_LOG_CMD)

run-update-offers: init_db
	pdm run update-offers $(ARGS) | $(RUN_LOG_CMD)

run-cleanup: init_db
	pdm run cleanup $(ARGS) | $(RUN_LOG_CMD)

run-all: run-update-directors run-update-films run-update-offers run-cleanup

run-db-upgrade:
	pdm run alembic upgrade head

webapp: init_db
	pdm run webapp

swagger:
	#curl http://localhost:8000/api/doc/swagger.json -o swagger.json
	pdm run swagger > swagger.json
	openapi-generator-cli validate -i swagger.json

ui:
	cd ui && http-server --port 8081 -c-1 -o

get-dirs:
	pdm run lcli directors get

get-films:
	pdm run lcli films get
