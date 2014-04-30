#

from pupa.scrape.popolo import Person, Organization
from ssu.parser import import_csv
from contextlib import contextmanager
import os
import csv

jid = "ocd-jurisdiction/country:xx/state:yy/place:foo"
oname = "Foo City"


@contextmanager
def load_resource(name):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
            "resources", name)) as fd:
        yield fd


def icsv(test, *args, **kwargs):
    for el in import_csv(*args, **kwargs):
        if isinstance(el, test):
            yield el


def test_org_conversion():
    with load_resource("testdata.csv") as fd:
        org_stream = icsv(Organization, fd, jid, oname)
        o = next(org_stream)
        assert o.name == oname
        assert o.jurisdiction_id == jid


def test_john_conversion():
    with load_resource("testdata.csv") as fd:
        people_stream = icsv(Person, fd, jid, oname)
        john = next(people_stream)

    obj = john.as_dict()
    assert obj['name'] == "John Q. Public"
    email, address, phone = obj['contact_details']

    assert email == {'value': 'ward1@example.com',
                     'note': 'Email 1', 'type': 'email'}

    assert address == {'value': '123 Test Place, East North-Westchester',
                       'note': 'Address 1', 'type': 'address'}

    assert phone == {'value': '781-555-5555', 'note': 'Phone 1',
                     'type': 'phone'}


def test_people_name_stream():
    with load_resource("testdata.csv") as fd:
        people_stream = icsv(Person, fd, jid, oname)
        with load_resource("testdata.csv") as fd:
            csv_stream = csv.DictReader(fd)

            for person, row in zip(people_stream, csv_stream):
                assert person.name == row['Name']


def test_bad_people_stream():
    with load_resource("noname.csv") as fd:
        people_stream = icsv(Person, fd, jid, oname)
        good = next(people_stream)

        try:
            assert False == next(people_stream), ("No assertion error was "
                "raised by people_to_pupa given a blank name.")
        except ValueError as e:
            assert (str(e)) == "A name is required for each entry."


def test_bad_district_stream():
    with load_resource("nodistrict.csv") as fd:
        people_stream = icsv(Person, fd, jid, oname)
        good = next(people_stream)

        try:
            assert False == next(people_stream), ("No assertion error was "
                "raised by people_to_pupa given a blank district.")
        except ValueError as e:
            assert (str(e)) == "A district is required for each entry."
