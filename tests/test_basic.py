#

from ssu.parser import people_to_pupa
from contextlib import contextmanager
import os


@contextmanager
def load_resource(name):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
            "resources", name)) as fd:
        yield fd


def test_popolo_conversion():
    with load_resource("testdata.csv") as fd:
        john = next(people_to_pupa(fd))
        obj = john.as_dict()
        assert obj['name'] == "John Q. Public"
        email, address, phone = obj['contact_details']

        assert email == {'value': 'ward1@example.com',
                         'note': 'Email 1', 'type': 'email'}

        assert address == {'value': '123 Test Place, East North-Westchester',
                           'note': 'Address 1', 'type': 'address'}

        assert phone == {'value': '781-555-5555', 'note': 'Phone 1',
                         'type': 'phone'}

    with load_resource("testdata.csv") as fd:
        for person in people_to_pupa(fd):
            pass
