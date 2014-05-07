#

from pupa.scrape.popolo import Organization, Person, Post, Membership
from ssu.parser import import_stream
from contextlib import contextmanager
import os
import csv

jid = "ocd-jurisdiction/country:xx/state:yy/place:foo"
oname = "Foo City"


@contextmanager
def load_resource(name):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
            "resources", name), 'rb') as fd:
        yield fd


def istream(test, xtn, *args, **kwargs):
    args = list(args)
    args.insert(1, xtn)

    for el in import_stream(*args, **kwargs):
        if isinstance(el, test):
            yield el


def test_org_conversion():
    with load_resource("testdata.csv") as fd:
        org_stream = istream(Organization, "csv", fd, jid, oname)
        o = next(org_stream)
        assert o.name == oname
        # assert o.jurisdiction_id == jid
        # XXX: Re-enable when we set JIDs again


def test_john_conversion():
    with load_resource("testdata.csv") as fd:
        people_stream = istream(Person, "csv", fd, jid, oname)
        john = next(people_stream)

    obj = john.as_dict()
    assert obj['name'] == "John Q. Public"
    email, address, phone = obj['contact_details']

    assert email == {'value': 'ward1@example.com',
                     'note': 'Email 1', 'type': 'email'}

    assert address == {'value': '123 Test Place, East North-Westchester',
                       'note': 'Address 1', 'type': 'address'}

    assert phone == {'value': '781-555-5555', 'note': 'Phone 1',
                     'type': 'voice'}


def test_xls_john_conversion():
    with load_resource("testdata.xls") as fd:
        people_stream = istream(Person, "xls", fd, jid, oname)
        john = next(people_stream)

    obj = john.as_dict()
    assert obj['name'] == "John Quincy Adams"
    address, = obj['contact_details']
    # No phone or email. Duh.

    assert address == {'value': 'Quincy MA, 02169',
                       'note': 'Address 1', 'type': 'address'}


def test_xlsx_john_conversion():
    with load_resource("testdata.xlsx") as fd:
        people_stream = istream(Person, "xlsx", fd, jid, oname)
        john = next(people_stream)

    obj = john.as_dict()
    assert obj['name'] == "John Quincy Adams"
    address, = obj['contact_details']
    # No phone or email. Duh.

    assert address == {'value': 'Quincy MA, 02169',
                       'note': 'Address 1', 'type': 'address'}


def test_people_name_stream():
    with load_resource("testdata.csv") as fd:
        people_stream = istream(Person, "csv", fd, jid, oname)
        with load_resource("testdata.csv") as fd:
            csv_stream = csv.DictReader((x.decode('utf-8') for x in fd))

            for person, row in zip(people_stream, csv_stream):
                assert person.name == row['Name']


def test_bad_people_stream():
    with load_resource("noname.csv") as fd:
        people_stream = istream(Person, "csv", fd, jid, oname)
        good = next(people_stream)

        try:
            assert False == next(people_stream), ("No assertion error was "
                "raised by people_to_pupa given a blank name.")
        except ValueError as e:
            assert (str(e)) == "A name is required for each entry."


def test_bad_district_stream():
    with load_resource("nodistrict.csv") as fd:
        people_stream = istream(Person, "csv", fd, jid, oname)
        good = next(people_stream)

        try:
            assert False == next(people_stream), ("No assertion error was "
                "raised by people_to_pupa given a blank district.")
        except ValueError as e:
            assert (str(e)) == "A district is required for each entry."


def test_people_post_stream():
    with load_resource("testdata.csv") as fd:
        post_stream = istream(Post, "csv", fd, jid, oname)
        post = next(post_stream)
        assert post.label == "Ward 20", "Bad district"


def test_people_membership_stream():
    with load_resource("testdata.csv") as fd:
        membership_stream = istream(Membership, "csv", fd, jid, oname)
        membership = next(membership_stream)
        assert membership.post_id == "district::Ward 20", "Bad Post relation"
