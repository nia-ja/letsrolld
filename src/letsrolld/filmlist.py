from . import csv


class FilmListEntry:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'Name':
                self.name = value
            elif key == 'Year':
                self.year = value
            elif key == 'Letterboxd URI' or key == 'URL':
                self.uri = value

    def __str__(self):
        return f'{self.name} ({self.year})'


def read_film_list(file_name):
    for row in csv.read_csv_file(file_name):
        yield FilmListEntry(**row)
