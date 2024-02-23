FROM python:3.11
COPY . /app
RUN pip install pdm
RUN pdm install -p /app

WORKDIR /app
CMD ["pdm", "run", "recommend", "--config", "configs/default.json"]
