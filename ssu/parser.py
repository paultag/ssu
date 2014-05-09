import csv
from ssu.xlrd import xlrd_dict_reader
from ssu.csv import csv_dict_reader
from ssu.models import (SpreadsheetUpload, SpreadsheetPerson,
                        SpreadsheetAddress, SpreadsheetPhone,
                        SpreadsheetEmail)

from contextlib import contextmanager
from pupa.scrape.helpers import Legislator
from pupa.scrape.popolo import Organization


OCD_SOURCE_URL = "http://opencivicdata.org/manual-data/source-notice"


def people_to_pupa(stream, org, jurisdiction_id):
    for row in stream:
        # XXX: Validate the row better.
        name = row.get("Name", "").strip()
        district = row.get("District", "").strip()

        if not name:
            raise ValueError("A name is required for each entry.")

        if not district:
            raise ValueError("A district is required for each entry.")

        obj = Legislator(name=name, district=district)
        org.add_post(label=district, role="member")

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
        obj.pre_save(jurisdiction_id)

        yield obj

        for related in obj._related:
            yield related

    for related in org._related:
        yield related


def import_parsed_stream(stream, user):
    upload = SpreadsheetUpload(user=user)
    upload.save()

    for person in stream:
        who = SpreadsheetPerson(
            name=person['Name'],
            spreadsheet=upload,
            district=person['District'],
        )
        who.save()

        for address in ["Address 1", "Address 2", "Address 3"]:
            where = person.get(address)
            if where:
                a = SpreadsheetAddress(person=who, address=where)
                a.save()

        for phone in ["Phone 1", "Phone 2", "Phone 3"]:
            phone = person.get(phone)
            if phone:
                p = SpreadsheetPhone(person=who, phone=phone)
                p.save()

        for email in ["Phone 1", "Phone 2", "Phone 3"]:
            email = person.get(email)
            if email:
                e = SpreadsheetEmail(person=who, email=email)
                e.save()

        print(who.as_dict())


def import_stream(stream, extension, user):
    reader = {"csv": csv_dict_reader,
              "xlsx": xlrd_dict_reader,
              "xls": xlrd_dict_reader}[extension]

    return import_parsed_stream(reader(stream), user)


@contextmanager
def import_file_stream(fpath, user):
    _, xtn = fpath.rsplit(".", 1)

    with open(fpath, 'br') as fd:
        yield import_stream(fd, xtn, user)
