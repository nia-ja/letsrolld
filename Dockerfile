FROM python:3.11

RUN pip install pdm

WORKDIR /app
COPY pyproject.toml pdm.lock ./
RUN touch README.md
RUN pdm sync -v

COPY . /app
RUN pdm install -v

RUN pdm run pytest

CMD ["pdm", "run", "recommend", "--config", "configs/default.json"]
