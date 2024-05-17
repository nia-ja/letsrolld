import click
from jinja2 import Environment, PackageLoader

from letsrolld_api_client import Client
from letsrolld_api_client.api.default import get_directors

# from letsrolld_api_client.api.default import get_directors_id
from letsrolld_api_client.api.default import get_films
# from letsrolld_api_client.api.default import get_films_id


# TODO: make the url configurable
client = Client(base_url="http://localhost:8000")


env = Environment(
    loader=PackageLoader("letsrolld.webcli"),
)


def report_film(film):
    template = env.get_template("film.template")
    return template.render(film=film)


def report_director(director):
    template = env.get_template("director.template")
    return template.render(director=director)


@click.group()
def cli():
    pass


@cli.group()
def directors():
    pass


@directors.command(name="get")
def directors_get():
    global client
    with client as client:
        director_reports = []
        for director in get_directors.sync(client=client):
            director_reports.append(report_director(director))

    print("\n\n".join(director_reports))


@cli.group()
def films():
    pass


@films.command(name="get")
def films_get():
    global client
    with client as client:
        film_reports = []
        for film in get_films.sync(client=client):
            film_reports.append(report_film(film))

    print("\n".join(film_reports))


if __name__ == "__main__":
    cli()
