# Convert a CSV.

import os
import sys

import django
from django.contrib.auth.models import User

from ssu.parser import import_file_stream, people_to_pupa
from ssu.importer import do_import
from ssu.models import (SpreadsheetUpload, SpreadsheetPerson)

from opencivicdata.models.jurisdiction import Jurisdiction as JurisdictionModel

from pupa.scrape import (Jurisdiction, Person, Organization, Membership, Post)
from pupa.importers import (JurisdictionImporter, OrganizationImporter,
                            PersonImporter, PostImporter, MembershipImporter)

def import_spreadsheet(fpath, user, jurisdiction):
    with import_file_stream(fpath, user, jurisdiction) as stream:
        print("{} - Uploaded {} people. Record {}.".format(
            user.username,
            stream.people.count(),
            stream.id,
        ))


def migrate_spreadsheet(transaction):
    for person in transaction.people.all():
        yield person.as_dict()


if __name__ == "__main__":
    django.setup()

    def _load(fpath, jurisdiction):
        jurisdiction = JurisdictionModel.objects.get(id=jurisdiction)
        u = User.objects.get(username='tag')
        import_spreadsheet(fpath, u, jurisdiction)

    def _migrate(transaction):
        t = SpreadsheetUpload.objects.get(id=int(transaction))
        stream = people_to_pupa(migrate_spreadsheet(t), t)
        report = do_import(stream, t)
        print(report)

    commands = {
        "load": _load,
        "migrate": _migrate,
    }

    def _help(*a):
        print("Valid commands:", list(commands.keys()))

    commands['help'] = _help

    sys.argv.pop(0)
    if sys.argv:
        cmd = sys.argv.pop(0)
    else:
        cmd = "help"

    commands.get(cmd, _help)(*sys.argv)
