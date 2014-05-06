#

import csv
from pupa.scrape.popolo import Person, Organization, Membership




def csv_dict_reader(stream):
    return csv.DictReader(stream)


