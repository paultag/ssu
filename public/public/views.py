from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods

from ssu.parser import import_stream
from ssu.models import SpreadsheetUpload
from opencivicdata.models import Jurisdiction


def home(request):
    return render_to_response("ssu/public/index.html", {})


@require_http_methods(["POST"])
def upload(request):
    sheet = request.FILES['sheet']
    _, xtn = sheet.name.rsplit(".", 1)
    jurisdiction = Jurisdiction.objects.get(id=request.POST['jurisdiction'])

    print(sheet)

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
