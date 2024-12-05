from collections import defaultdict

import click
from jinja2 import Environment, PackageLoader


from letsrolld_api_client import Client
from letsrolld_api_client.api.default import get_directors

# from letsrolld_api_client.api.default import get_directors_id
from letsrolld_api_client.api.default import get_films

# from letsrolld_api_client.api.default import get_films_id
from letsrolld_api_client.api.default import get_reports
from letsrolld_api_client.api.default import get_reports_id


# TODO: make the url configurable
client = Client(base_url="http://localhost:8000")


env = Environment(
    loader=PackageLoader("letsrolld.webcli"),
)


def list_film(film):
    template = env.get_template("film.j2")
    return template.render(film=film)


def list_director(director):
    template = env.get_template("director.j2")
    return template.render(director=director)


def _seen(url, urls_seen):
    if url is None:
        return False
    if url in urls_seen:
        return True
    if any(url.startswith(u) for u in urls_seen):
        return True
    if any(u.startswith(url) for u in urls_seen):
        return True
    return False


def _get_services_to_report(film):
    offers_to_report = defaultdict(list)
    urls_seen = set()
    for o in film.offers:
        if not _seen(o.url, urls_seen):
            offers_to_report[o.monetization_type].append(o)
            if o.url:
                urls_seen.add(o.url)
    return offers_to_report


def report_film(film):
    template = env.get_template("film-full.j2")
    return template.render(film=film, offers=_get_services_to_report(film))


def list_report(report):
    template = env.get_template("report.j2")
    return template.render(report=report)


def render_report(report):
    template = env.get_template("report-full.j2")
    return template.render(report=report, film_renderer=report_film)


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
            director_reports.append(list_director(director))

    print("\n".join(director_reports))


@cli.group()
def films():
    pass


def _get_short_report_section(films):
    film_entries = []
    for film in films:
        film_entries.append(list_film(film))
    return "\n".join(film_entries)


def _get_long_report_section(films):
    film_entries = []
    for film in films:
        film_entries.append(report_film(film))
    return "\n".join(film_entries)


@films.command(name="get")
def films_get():
    global client
    with client as client:
        print(_get_short_report_section(get_films.sync(client=client)))


def _get_query_args(limit, genre, country, offer):
    args = {"limit": limit}
    if genre:
        args["genre"] = genre
    if country:
        args["country"] = country
    if offer:
        args["offer"] = offer
    return args


@films.command(name="query")
# TODO: build options from the API model definition
@click.option("--limit", default=10)
@click.option("--genre", default=None)
@click.option("--country", default=None)
@click.option("--offer", default=None)
def films_query(
    limit: int,
    genre: str,
    country: str,
    offer: str,
):
    global client
    with client as client:
        args = _get_query_args(limit, genre, country, offer)
        films = get_films.sync(client=client, **args)
        if films:
            print(_get_long_report_section(films))


@cli.group()
def report():
    pass


@report.command(name="get")
def report_get():
    global client
    with client as client:
        reports = get_reports.sync(client=client)
        if reports:
            report_entries = []
            for report in reports:
                report_entries.append(list_report(report))
            print("\n".join(report_entries))


@report.command(name="render")
@click.option("--name", required=True)
def report_render(
    name: str,
):
    global client
    with client as client:
        reports = get_reports.sync(client=client)
        if reports:
            id_ = None
            for report in reports:
                if report.name == name:
                    id_ = report.id
                    break
            if id_ is not None:
                requested_report = get_reports_id.sync(client=client, id=id_)
                if requested_report:
                    print(render_report(requested_report))


if __name__ == "__main__":
    cli()
