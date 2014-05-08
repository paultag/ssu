from django.db import models
from django.contrib.auth.models import User


class SpreadsheetUpload(models.Model):
    # User, when, who approved
    user = models.ForeignKey(User)
    approved_by = models.ForeignKey(User)
    created_at = models.DateTimeField()


class SpreadsheetPerson(models.Model):
    # name, district, person-id given
    name = models.TextField()
    district = models.TextField()
    spreadsheet = models.ForeignKey(SpreadsheetUpload)


class SpreadsheetAddress(models.Model):
    # FK, address
    person = models.ForeignKey(SpreadsheetPerson)
    address = models.TextField()


class SpreadsheetPhone(models.Model):
    # FK, phone
    person = models.ForeignKey(SpreadsheetPerson)
    phone = models.TextField()


class SpreadsheetEmail(models.Model):
    # FK, email
    person = models.ForeignKey(SpreadsheetPerson)
    email = models.TextField()
