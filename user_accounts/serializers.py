from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Account


class CreateTransactionCodeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['transaction_code']


class GetBalanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['balance', 'interest_rate']
