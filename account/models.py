from __future__ import unicode_literals

from django.db import models

class Account(models.Model):
    account_name = models.CharField(max_length=200)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.account_name

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    detail = models.CharField(max_length=200)
    value = models.IntegerField(default=0)
    date = models.DateTimeField('date and time')

    def __str__(self):
        return self.detail
