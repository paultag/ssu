# Convert a CSV.

import os
import sys

import django
from django.contrib.auth.models import User

from ssu.parser import import_file_stream
from ssu.models import (SpreadsheetUpload, SpreadsheetPerson)

from pupa.scrape import (Jurisdiction, Person, Organization, Membership, Post)
from pupa.importers import (JurisdictionImporter, OrganizationImporter,
                            PersonImporter, PostImporter, MembershipImporter)

def import_spreadsheet(fpath, user):
    with import_file_stream(fpath, user) as stream:
        print("{} - Uploaded {} people. Record {}.".format(
            user.username,
            stream.people.count(),
            stream.id,
        ))


if __name__ == "__main__":
    django.setup()

    def _load(fpath):
        u = User.objects.get(username='tag')
        import_spreadsheet(fpath, u)

    def _migrate():
        pass

    commands = {
        "load": _load,
        "migrate": _migrate,
    }

    def _help(*a):
        print("Valid commands:", list(commands.keys()))

    commands['help'] = _help

    sys.argv.pop(0)
    cmd = sys.argv.pop(0)

    commands.get(cmd, _help)(*sys.argv)
