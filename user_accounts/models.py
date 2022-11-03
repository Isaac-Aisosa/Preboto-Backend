from django.conf import settings
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver


class Account(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="user_account", on_delete=models.CASCADE)
    userName = models.CharField(max_length=225, blank=True, null=True)
    ref_number = models.CharField(unique=True, max_length=20, blank=True, null=True)
    account_number = models.CharField(unique=True, max_length=10, blank=True, null=True)
    balance = models.BigIntegerField(default=0)
    transaction_code = models.CharField(max_length=4, default='0000', null=True, blank=True)
    interest_rate = models.BigIntegerField(default=0, null=True, blank=True)
    block = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    emailVaried = models.BooleanField(default=False)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.user} Account'

    def save(self, *args, **kwargs):
        # super().save(*args, **kwargs)
        generated_number = self.account_number
        if not generated_number:
            generated_numbe = get_random_string(length=9, allowed_chars='0123456789')
            generated_number = f'3{generated_numbe}'
        while Account.objects.filter(account_number=generated_number).exclude(pk=self.pk).exists():
            generated_numbe = get_random_string(length=9, allowed_chars='0123456789')
            generated_number = f'3{generated_numbe}'
        self.account_number = generated_number

        ref_number = self.ref_number
        if not ref_number:
            ref_num = get_random_string(length=11, allowed_chars='0123456789')
            ref_number = f'FX-{ref_num}'
        while Account.objects.filter(ref_number=ref_number).exclude(pk=self.pk).exists():
            ref_num = get_random_string(length=11, allowed_chars='0123456789')
            ref_number = f'FX-{ref_num}'
        self.ref_number = ref_number

        super(Account, self).save(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_account(sender, instance=None, created=False, **kwargs):
    if created:
        Account.objects.create(user=instance)


class TemporaryAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="user_temp_account", on_delete=models.CASCADE)
    ref_number = models.CharField(unique=True, max_length=20, blank=True, null=True)
    userName = models.CharField(max_length=225, blank=True, null=True)
    balance = models.BigIntegerField(default=0)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.user} TemporaryAccount'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_account(sender, instance=None, created=False, **kwargs):
    if created:
        TemporaryAccount.objects.create(user=instance)
