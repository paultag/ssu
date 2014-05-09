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

def import_spreadsheet(stream):
    pass


if __name__ == "__main__":
    django.setup()

    if len(sys.argv) != 2:
        print("Error: Need a csv file path to import")
        sys.exit(1)

    u = User.objects.get(username='tag')

    _, fpath = sys.argv
    with import_file_stream(fpath, u) as stream:
        print(stream)
