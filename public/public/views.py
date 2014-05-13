from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods

from ssu.parser import import_stream, people_to_pupa
from ssu.importer import do_import
from ssu.models import SpreadsheetUpload
from opencivicdata.models import Jurisdiction


def home(request):
    return render_to_response("ssu/public/index.html", {})


@require_http_methods(["POST"])
def upload(request):
    sheet = request.FILES['sheet']
    _, xtn = sheet.name.rsplit(".", 1)
    jurisdiction = Jurisdiction.objects.get(id=request.POST['jurisdiction'])

    transaction = import_stream(
        sheet.read(),
        xtn,
        request.user,
        jurisdiction,
    )

    return render_to_response("ssu/public/upload.html", {
        "transaction": transaction,
    })


def manage(request, transaction):
    transaction = SpreadsheetUpload.objects.get(id=int(transaction))

    return render_to_response("ssu/public/manage.html", {
        "transaction": transaction,
    })


@require_http_methods(["POST"])
def migrate(request):
    transaction_id = int(request.POST['transaction'])
    transaction = SpreadsheetUpload.objects.get(id=transaction_id)

    if transaction.approved_by:
        return render_to_response("ssu/public/migrate_fail.html", {
            "transaction": transaction,
        })

    approver = request.user

    def migrate_spreadsheet(transaction):
        for person in transaction.people.all():
            yield person.as_dict()

    stream = people_to_pupa(migrate_spreadsheet(transaction), transaction)
    report = do_import(stream, transaction)

    transaction.approved_by = approver
    transaction.save()

    return render_to_response("ssu/public/migrate.html", {
        "transaction": transaction,
        "report": report,
    })
