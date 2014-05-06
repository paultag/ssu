#

import xlrd
from pupa.scrape.popolo import Person, Organization, Membership


OCD_SOURCE_URL = "http://opencivicdata.org/manual-data/source-notice"


def xlrd_dict_reader(stream):
    book = xlrd.open_workbook(file_contents=stream.read())
    sheet = book.sheets()[0]  # XXX: Fix this

    rows = iter([sheet.row(x) for x in range(sheet.nrows)])
    header = next(rows)
    for row in rows:
        yield dict(zip([x.value for x in header],
                       [x.value for x in row]))


def people_to_pupa(stream, org):
    for row in xlrd_dict_reader(stream):
        print(row)


def import_xls(stream, jurisdiction_id, organization_name):
    org = Organization(
        name=organization_name,
        classification='legislature'
    )
    org.add_source(url=OCD_SOURCE_URL)

    yield from people_to_pupa(stream, org)
    yield org
