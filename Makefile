DOCKER?=docker
IMAGE_NAME=letsrolld

DB=$(PWD)/letsrolld.db
HTTP_CACHE=$(PWD)/cache.sqlite

ifndef VERBOSE
.SILENT:
endif

ifndef EMAIL
DOCKER_ARGS=-it
endif

DOCKER_CMD=\
	$(DOCKER) run $(DOCKER_ARGS) --rm --name $(IMAGE_NAME) \
		-v $(DB):/app/letsrolld.db:z \
		-v $(HTTP_CACHE):/app/cache.sqlite:z \
		-v $(PWD)/data:/app/data:z \
		$(IMAGE_NAME)

build:
	$(DOCKER) build -t $(IMAGE_NAME) .

# TODO: move cache init into container startup script?
run-prep:
	mkdir -p $(PWD)/data
	test -f $(DB) || sqlite3 $(DB) "VACUUM;"
	test -f $(HTTP_CACHE) || sqlite3 $(HTTP_CACHE) "VACUUM;"

run: run-prep
	$(DOCKER_CMD)

run-shorts: run-prep
	$(DOCKER_CMD) pdm run recommend --config configs/shorts.json

run-debug: run-prep
	$(DOCKER_CMD) bash

install:
	pdm install

test: install
	pdm run pytest

lint: install
	pre-commit run --all-files

all: lint test
