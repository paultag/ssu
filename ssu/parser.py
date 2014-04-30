#

import csv
from pupa.scrape.popolo import Person

def people_to_pupa(stream):
    for row in csv.DictReader(stream):

        # XXX: Validate the row better.

        if not row.get("Name", "").strip():
            raise ValueError("A name is required for each entry.")

        if not row.get("District", "").strip():
            raise ValueError("A district is required for each entry.")

        obj = Person(name=row.get("Name"))

        for key, keys in [
            ("email", ("Email 1", "Email 2", "Email 3")),
            ("address", ("Address 1", "Address 2", "Address 3")),
            ("phone", ("Phone 1", "Phone 2", "Phone 3")),
        ]:
            for k in keys:
                value = row.get(k)
                if value:
                    obj.add_contact_detail(type=key, value=value, note=k)
        yield obj
