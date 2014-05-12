from django.shortcuts import render_to_response
from ssu.parser import import_stream
from opencivicdata.models import Jurisdiction


def home(request):
    return render_to_response("ssu/public/index.html", {})


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
