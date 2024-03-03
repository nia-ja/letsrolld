DOCKER?=docker
IMAGE_NAME=letsrolld

DB=$(PWD)/letsrolld.db
HTTP_CACHE=$(PWD)/cache.sqlite

ifndef VERBOSE
.SILENT:
endif

build:
	$(DOCKER) build -t $(IMAGE_NAME) .

# TODO: move cache init into container startup script?
run-prep:
	mkdir -p $(PWD)/data
	test -f $(DB) || sqlite3 $(DB) "VACUUM;"
	test -f $(HTTP_CACHE) || sqlite3 $(HTTP_CACHE) "VACUUM;"

run: run-prep
	$(DOCKER) run -it --rm --name $(IMAGE_NAME) \
		-v $(DB):/app/letsrolld.db:z \
		-v $(HTTP_CACHE):/app/cache.sqlite:z \
		-v $(PWD)/data:/app/data \
		$(IMAGE_NAME)

run-shorts: run-prep
	$(DOCKER) run -it --rm --name $(IMAGE_NAME) \
		-v $(DB):/app/letsrolld.db:z \
		-v $(HTTP_CACHE):/app/cache.sqlite:z \
		-v $(PWD)/data:/app/data \
		$(IMAGE_NAME) pdm run recommend --config configs/shorts.json

install:
	pdm install

test: install
	pdm run pytest

lint: install
	pre-commit run --all-files

all: lint test
