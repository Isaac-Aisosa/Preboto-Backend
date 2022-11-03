from django.conf import settings
from django.db import models


# Create your models here.
class DepositAccount(models.Model):
    balance = models.BigIntegerField(default=0)
    bank_account_number = models.CharField(max_length=15, blank=True, null=True)
    bank_account_name = models.CharField(max_length=225, blank=True, null=True)
    bank_name = models.CharField(max_length=225, blank=True, null=True)
    active = models.BooleanField(default=False)
    block = models.BooleanField(default=False)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.bank_name} Deposit Account'


class PrebotoWithdrawAccount(models.Model):
    balance = models.BigIntegerField(default=0)
    bank_account_number = models.CharField(max_length=15, blank=True, null=True)
    bank_account_name = models.CharField(max_length=225, blank=True, null=True)
    bank_name = models.CharField(max_length=225, blank=True, null=True)
    active = models.BooleanField(default=False)
    block = models.BooleanField(default=False)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.bank_name} Withdraw Account'


class RevenueAccount(models.Model):
    balance = models.BigIntegerField(default=0)
    bank_account_number = models.CharField(max_length=15, blank=True, null=True)
    bank_account_name = models.CharField(max_length=225, blank=True, null=True)
    bank_name = models.CharField(max_length=225, blank=True, null=True)
    active = models.BooleanField(default=False)
    block = models.BooleanField(default=False)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.bank_name} Revenue Account'


class ServiceAccount(models.Model):
    balance = models.BigIntegerField(default=0)
    bank_account_number = models.CharField(max_length=15, blank=True, null=True)
    bank_account_name = models.CharField(max_length=225, blank=True, null=True)
    bank_name = models.CharField(max_length=225, blank=True, null=True)
    active = models.BooleanField(default=False)
    block = models.BooleanField(default=False)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.bank_name} Service Account'


class UtilityAccount(models.Model):
    balance = models.BigIntegerField(default=0)
    bank_account_number = models.CharField(max_length=15, blank=True, null=True)
    bank_account_name = models.CharField(max_length=225, blank=True, null=True)
    bank_name = models.CharField(max_length=225, blank=True, null=True)
    active = models.BooleanField(default=False)
    block = models.BooleanField(default=False)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.bank_name} Utility Account'
