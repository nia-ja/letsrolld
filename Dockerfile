FROM python:3.11
COPY . /app
WORKDIR /app

RUN pip install pdm
RUN pdm install
RUN pdm run pytest

CMD ["pdm", "run", "recommend", "--config", "configs/default.json"]
