import datetime as dt
from django.db import models
from django.contrib.auth.models import User


class SpreadsheetUpload(models.Model):
    user = models.ForeignKey(User, related_name='uploads')
    approved_by = models.ForeignKey(User, related_name='approvals', null=True)
    created_at = models.DateTimeField(default=dt.datetime.utcnow())


class SpreadsheetPerson(models.Model):
    name = models.TextField()
    district = models.TextField()
    spreadsheet = models.ForeignKey(SpreadsheetUpload)
    # HStore here.


class SpreadsheetAddress(models.Model):
    person = models.ForeignKey(SpreadsheetPerson)
    address = models.TextField()


class SpreadsheetPhone(models.Model):
    person = models.ForeignKey(SpreadsheetPerson)
    phone = models.TextField()


class SpreadsheetEmail(models.Model):
    person = models.ForeignKey(SpreadsheetPerson)
    email = models.TextField()
