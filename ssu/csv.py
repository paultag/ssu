import csv


def csv_dict_reader(fd):
    stream = (x.decode('utf-8') for x in fd)
    return csv.DictReader(stream)
