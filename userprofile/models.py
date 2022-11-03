from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="user", on_delete=models.CASCADE)
    profileImage = models.ImageField(verbose_name='Profile Image',
                                     upload_to='media/profile_images', blank=True, null=True)
    DOB = models.DateField(verbose_name="DOB:YYYY-MM-DD", blank=True, null=True)
    Gender = models.CharField(max_length=7, blank=True, null=True)
    Phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=225, blank=True, null=True)
    timestamp = models.DateTimeField(verbose_name='timestamp', auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.user} Profile'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_account(sender, instance=None, created=False, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

