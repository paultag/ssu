#

import xslt
from pupa.scrape.popolo import Person, Organization, Membership


OCD_SOURCE_URL = "http://opencivicdata.org/manual-data/source-notice"


def people_to_pupa(stream, org):
    for row in []:
        pass



def import_xls(stream, jurisdiction_id, organization_name):
    org = Organization(
        name=organization_name,
        classification='legislature'
    )
    org.add_source(url=OCD_SOURCE_URL)

    yield from people_to_pupa(stream, org)
    yield org
