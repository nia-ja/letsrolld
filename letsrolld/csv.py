import csv


def read_csv_file(file_name):
    headers = []
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if not headers:
                headers = row
            else:
                yield dict(zip(headers, row))
