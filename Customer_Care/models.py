from django.db import models


# Create your models here.


class Contact(models.Model):
    customerLine1 = models.CharField(max_length=20, blank=True, null=True)
    customerLine2 = models.CharField(max_length=20, blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'Mobile Contact'


class Whatsapp(models.Model):
    customerCare = models.CharField(max_length=20, blank=True, null=True)
    customerBot = models.CharField(max_length=20, blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'Whatsapp Contact'


class Email(models.Model):
    customerEmail1 = models.CharField(max_length=225, blank=True, null=True)
    customerEmail2 = models.CharField(max_length=225, blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'Email Contact'


class Social(models.Model):
    facebook = models.CharField(max_length=225, blank=True, null=True)
    instagram = models.CharField(max_length=225, blank=True, null=True)
    twitter = models.CharField(max_length=225, blank=True, null=True)
    youtube = models.CharField(max_length=225, blank=True, null=True)
    tiktok = models.CharField(max_length=225, blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'Social Contact'


class Location(models.Model):
    address = models.CharField(max_length=225, blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'Location'


class AppDownloadLink(models.Model):
    playStore = models.CharField(max_length=225, blank=True, null=True)
    AppStore = models.CharField(max_length=225, blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'AppDownloadLink'
