import csv


def csv_dict_reader(fd):
    stream = fd.decode('utf-8').splitlines()
    ret = csv.DictReader(stream)
    return ret
