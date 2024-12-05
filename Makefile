IMAGE_NAME?=letsrolld
DB=$(PWD)/movie.db
DIRECTORS_NUMBER?=10
DIRECTORS_FILE?=directors.csv
RUN_LOG?=run.log
RUN_LOG_CMD?=ts | tee -a $(RUN_LOG)

.PHONY: install lint test populate-directors run-update-directors run-update-films run-update-offers run-cleanup run-all run-db-upgrade webapp ui swagger swagger-py swagger-js swagger-ts swagger-all get-dirs get-films

install:
	pdm install -vd

lint: install swagger
	pre-commit run --all-files

test: lint
	pdm run pytest

get-directors:
	pdm run get-directors -i ./data/lists/everything.csv -o ${DIRECTORS_FILE} | $(RUN_LOG_CMD)

populate-directors:
	pdm run populate-directors -d ${DIRECTORS_FILE} -n ${DIRECTORS_NUMBER}

dump-directors:
	pdm run dump-directors -o ${DIRECTORS_FILE}.new | $(RUN_LOG_CMD)

run-update-directors:
	pdm run update-directors $(ARGS) | $(RUN_LOG_CMD)

run-update-films:
	pdm run update-films $(ARGS) | $(RUN_LOG_CMD)

run-update-offers:
	pdm run update-offers $(ARGS) | $(RUN_LOG_CMD)

run-update-services:
	pdm run update-services $(ARGS) | $(RUN_LOG_CMD)

run-cleanup:
	pdm run cleanup $(ARGS) | $(RUN_LOG_CMD)

run-all: run-update-directors run-update-films run-update-offers run-update-services run-cleanup

run-db-upgrade:
	pdm run alembic upgrade head

webapp: install
	pdm run webapp

email: install
	./scripts/email.sh --start-server

swagger:
	#curl http://localhost:8000/api/doc/swagger.json -o swagger.json
	pdm run swagger > swagger.json.tmp
	mv swagger.json.tmp swagger.json
	openapi-generator-cli validate -i swagger.json

swagger-py: swagger
	rm -rf letsrolld-api-client
	pdm run openapi-python-client generate --path swagger.json

swagger-js: swagger
	rm -rf js
	openapi-generator-cli generate -i swagger.json -g javascript -o js

swagger-ts: swagger
	rm -rf ts
	openapi-generator-cli generate -i swagger.json -g typescript-node -o ts

swagger-all: swagger-py swagger-js swagger-ts

ui:
	cd ui && http-server --port 8081 -c-1 -o

get-dirs:
	pdm run lcli directors get

get-films:
	pdm run lcli films get
