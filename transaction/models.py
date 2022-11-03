from django.conf import settings
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from General_Account.models import DepositAccount


class Deposit(models.Model):
    amount = models.BigIntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="depositor", on_delete=models.PROTECT)
    username = models.CharField(max_length=225, blank=True, null=True)
    ref_number = models.CharField(max_length=15, blank=True, null=True)
    bank_account = models.ForeignKey(DepositAccount, related_name="deposited_acct", on_delete=models.PROTECT)
    complete = models.BooleanField(default=False)
    pending = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)
    confirmedBy = models.CharField(max_length=225, blank=True, null=True)
    transactionID = models.CharField(unique=True, max_length=20, blank=False, null=False)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.user} Deposit at {self.timestamp}'


class Transfer(models.Model):
    amount = models.BigIntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="from_user", on_delete=models.PROTECT)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="to_user", on_delete=models.PROTECT)
    senderName = models.CharField(max_length=225, blank=True, null=True, default='null')
    recipientName = models.CharField(max_length=225, blank=True, null=True)
    recipient_account_number = models.CharField(max_length=15, blank=True, null=True)
    transactionID = models.CharField(unique=True, max_length=20, blank=False, null=False)
    pending = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.user} Transfer at {self.timestamp}'


class Bank(models.Model):
    bank_code = models.IntegerField(default=0,blank=False, null=False)
    bank_name = models.CharField(max_length=225, blank=False, null=False)
    allowed = models.BooleanField(default=True)
    block = models.BooleanField(default=False)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.bank_name}'


class WithdrawAccount(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="acct_owner", on_delete=models.PROTECT)
    bank = models.ForeignKey(Bank, related_name="to_bank", on_delete=models.PROTECT)
    bank_name = models.CharField(max_length=225, blank=False, null=False, default='my bank')
    acct_name = models.CharField(max_length=225, blank=False, null=False)
    acct_number = models.CharField(max_length=20, blank=False, null=False)
    verified = models.BooleanField(default=False)
    verified_failed = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.owner} {self.bank}'


class Withdraw(models.Model):
    amount = models.BigIntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="account_user", on_delete=models.PROTECT)
    username = models.CharField(max_length=225, blank=True, null=True)
    ref_number = models.CharField(max_length=15, blank=True, null=True)
    bank = models.ForeignKey(WithdrawAccount, related_name="user_bank", on_delete=models.PROTECT)
    transactionID = models.CharField(unique=True, max_length=20, blank=False, null=False)
    pending = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.user} Withdraw'

# class CustomerTransaction(models.Model):
#    transactionID = models.CharField(unique=True, max_length=20, blank=False, null=False)
#    transactionType = models.CharField(max_length=8, blank=False, null=False)
#    deposit = models.ForeignKey(
#        Deposit, related_name="Deposit", on_delete=models.PROTECT)

#  withdraw = models.ForeignKey(
#       Withdraw, related_name="Withdraw", on_delete=models.PROTECT)

#    transfer = models.ForeignKey(
#        Transfer, related_name="Transfer", on_delete=models.PROTECT)

#   timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

#   def __str__(self):
#       return f'{self.transactionID}'

#   def save(self, *args, **kwargs):
# super().save(*args, **kwargs)

#        transaction_id = self.transactionID

#       if not transaction_id:
#           ID_num = get_random_string(length=20,
#                                      allowed_chars='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqurstuvwxyz')
#    while CustomerTransaction.objects.filter(transactionID=transaction_id).exists():
#          ID_num = get_random_string(length=20,
#                                     allowed_chars='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqurstuvwxyz')
#          transaction_id = ID_num
#      self.transactionID = transaction_id

#     super(CustomerTransaction, self).save(*args, **kwargs)

########
# @receiver(post_save, sender=Deposit)
# def create_transaction_id(sender, instance=None, created=False, **kwargs):
#    if created:
#        CustomerTransaction.objects.create(deposit=instance, transactionType='deposit')
