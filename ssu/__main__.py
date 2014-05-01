# Convert a CSV.

import sys

from ssu.parser import import_csv
from pupa.scrape import (Jurisdiction, Person, Organization, Membership, Post)
from pupa.importers import (JurisdictionImporter, OrganizationImporter,
                            PersonImporter, PostImporter, MembershipImporter)


def _do_import(fd, org, jurisdiction_id):
    stream = import_csv(fd, org, jurisdiction_id)
    stream = list(stream)

    juris_importer = JurisdictionImporter(jurisdiction_id)
    org_importer = OrganizationImporter(jurisdiction_id)
    person_importer = PersonImporter(jurisdiction_id)
    post_importer = PostImporter(jurisdiction_id, org_importer)
    membership_importer = MembershipImporter(
        jurisdiction_id,
        person_importer,
        org_importer,
        post_importer
    )

    report = {}
    # This basically relates to Pupa's pupa.clu.commands.update:113
    # (From there - wrap this in a transaction.)

    def tfilter(otype, stream):
        for el in filter(lambda x: isinstance(x, otype), stream):
            yield el.as_dict()


    report.update(juris_importer.import_iterator(tfilter(Jurisdiction, stream)))
    report.update(org_importer.import_iterator(tfilter(Organization, stream)))
    report.update(person_importer.import_iterator(tfilter(Person, stream)))
    report.update(post_importer.import_iterator(tfilter(Post, stream)))

    report.update(membership_importer.import_iterator(
        tfilter(Membership, stream)))

    return report


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Need a csv file path to import")
        sys.exit(1)

    _, fpath = sys.argv
    with open(fpath, 'r') as fd:
        print(_do_import(
            fd,
            "Test Jurisdiction",
            "ocd-jurisdiction/country:xx/council"
        ))