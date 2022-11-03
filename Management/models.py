from django.conf import settings
from django.db import models


# Create your models here.

class DailyTrade(models.Model):
    inputAmount = models.BigIntegerField(default=0)
    outputAmount = models.BigIntegerField(default=0, blank=True, null=True)
    returns = models.BigIntegerField(default=0, blank=True, null=True)
    terminalUser = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="terminal", on_delete=models.PROTECT)
    terminal = models.CharField(max_length=225, blank=True, null=True)
    tradeName = models.CharField(max_length=225, blank=True, null=True)
    opened = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    gain = models.BooleanField(default=False)
    loss = models.BooleanField(default=False)
    openTime = models.TimeField(verbose_name='openTime', auto_now_add=True, editable=False)
    closeTime = models.TimeField(verbose_name='closeTime', editable=True, blank=True, null=True)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.tradeName}: {self.inputAmount} to {self.outputAmount}'


class ClientTradeHistory(models.Model):
    inputAmount = models.BigIntegerField(default=0)
    outputAmount = models.BigIntegerField(default=0, blank=True, null=True)
    returns = models.BigIntegerField(default=0, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="client", on_delete=models.PROTECT)
    username = models.CharField(max_length=225, blank=True, null=True)
    gain = models.BooleanField(default=False)
    loss = models.BooleanField(default=False)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.user}: {self.inputAmount} to {self.outputAmount}'


class RevenueHistory(models.Model):
    previousBalance = models.BigIntegerField(default=0, blank=True, null=True)
    newBalance = models.BigIntegerField(default=0, blank=True, null=True)
    growth = models.BigIntegerField(default=0, blank=True, null=True)
    trade = models.ForeignKey(DailyTrade, related_name="trade_source", on_delete=models.PROTECT)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'Revenue: {self.previousBalance} to {self.newBalance}'


class PrebotoConstant(models.Model):
    prebotoGainPercent = models.IntegerField(default=0)
    prebotoLossPercent = models.IntegerField(default=0)
    clientsGainPercent = models.IntegerField(default=0)
    clientsLossPercent = models.IntegerField(default=0)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'PrebotoConstants(Active:{self.active})'


class AccountTransactionHistory(models.Model):
    Amount = models.BigIntegerField(default=0)
    account = models.CharField(max_length=225, blank=True, null=True)
    Recipient_account = models.CharField(max_length=225, blank=True, null=True)
    terminalUser = models.CharField(max_length=225, blank=True, null=True)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'Transfer from {self.account} ot {self.Recipient_account}'


class Policy(models.Model):
    title = models.CharField(max_length=225, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.title}'


class About(models.Model):
    title = models.CharField(max_length=225, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.title}'
