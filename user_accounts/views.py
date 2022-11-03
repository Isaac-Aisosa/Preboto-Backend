from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account, TemporaryAccount
from Management.models import ClientTradeHistory
from userprofile.serializers import UserProfileSerializers
from .serializers import CreateTransactionCodeSerializers, GetBalanceSerializers


class CreateTransactionCode(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data['transaction_code']
        username = request.user.username
        account = Account.objects.get(user=request.user)
        account.transaction_code = code
        account.userName = username
        account.approved = True
        account.save()
        TempAccount = TemporaryAccount.objects.get(user=request.user)
        TempAccount.ref_number = account.ref_number
        TempAccount.userName = username
        TempAccount.save()
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_account_balance(request):
    account = Account.objects.get(user=request.user)
    temp_account = TemporaryAccount.objects.get(user=request.user)
    balance = account.balance + temp_account.balance
    return Response({
        'balance': balance,
        'trade_value': account.balance,
        'interest_rate': account.interest_rate,
        'block': account.block,
        'acct_number': account.account_number,
        'emailVaried': account.emailVaried
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_account_trade_history(request):
    trade = ClientTradeHistory.objects.filter(user=request.user).order_by('-timestamp').values()
    return Response({
        "trade": list(trade),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_last_client_account_trade(request):
    trade = ClientTradeHistory.objects.filter(user=request.user).last()
    return Response({
        "inputAmount": trade.inputAmount,
        "outputAmount": trade.outputAmount,
        "returns": trade.returns,
        "gain": trade.gain,
        "loss": trade.loss,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_last_six_client_account_trade(request):
    trade = ClientTradeHistory.objects.filter(user=request.user).order_by('-timestamp')[:6].values()
    return Response({
        "trade": list(trade),
    })
