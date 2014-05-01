#

import csv
from pupa.scrape.popolo import Person, Organization


def people_to_pupa(stream, org):
    for row in csv.DictReader(stream):

        # XXX: Validate the row better.
        name = row.get("Name", "").strip()
        district = row.get("District", "").strip()

        if not name:
            raise ValueError("A name is required for each entry.")

        if not district:
            raise ValueError("A district is required for each entry.")

        obj = Person(name=name)
        # XXX: org add post -> district
        # XXX: org add membership -> person
        org.add_post(label=district, role="member")
        obj.add_membership(org, role="member", post_id=district)

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


def import_csv(stream, jurisdiction_id, organization_name):
    org = Organization(
        name=organization_name,
        classification='legislature'
    )  # , jurisdiction_id=jurisdiction_id)
    # XXX: Re-add Jurisdiction ID

    yield org
    yield from people_to_pupa(stream, org)
