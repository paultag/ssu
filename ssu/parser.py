import csv
from ssu.xlrd import xlrd_dict_reader

from pupa.scrape.popolo import Person, Organization


OCD_SOURCE_URL = "http://opencivicdata.org/manual-data/source-notice"


def people_to_pupa(stream, org):
    for row in stream:

        # XXX: Validate the row better.
        name = row.get("Name", "").strip()
        district = row.get("District", "").strip()

        if not name:
            raise ValueError("A name is required for each entry.")

        if not district:
            raise ValueError("A district is required for each entry.")

        obj = Person(name=name)
        org.add_post(label=district, role="member")
        obj.add_membership(org, role="member", post_id=district)

        for key, keys in [
            ("email", ("Email 1", "Email 2", "Email 3")),
            ("address", ("Address 1", "Address 2", "Address 3")),
            ("voice", ("Phone 1", "Phone 2", "Phone 3")),
        ]:
            for k in keys:
                value = row.get(k)
                if value:
                    obj.add_contact_detail(type=key, value=value, note=k)

        obj.add_source(url=OCD_SOURCE_URL)
        obj.validate()

        yield obj

        for related in obj._related:
            yield related

    for related in org._related:
        yield related


def import_parsed_stream(stream, jurisdiction_id, organization_name):
    org = Organization(
        name=organization_name,
        classification='legislature'
    )  # , jurisdiction_id=jurisdiction_id)
    org.add_source(url=OCD_SOURCE_URL)
    # XXX: Re-add Jurisdiction ID

    yield from people_to_pupa(stream, org)
    yield org


def import_stream(stream, extension, name, jurisdiction):
    reader = {"csv": csv.DictReader,
              "xls": xlrd_dict_reader}[extension]

    return import_parsed_stream(reader(stream), name, jurisdiction)


def import_file_stream(fpath, name, jurisdiction):
    _, xtn = fpath.rsplit(".", 1)

    with open(fpath, 'br') as fd:
        return import_stream(fd, xtn, name, jurisdiction)
