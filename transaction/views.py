# Create your views here.
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user_accounts.models import Account
from General_Account.models import DepositAccount
from .models import Deposit, Transfer, Bank, WithdrawAccount, Withdraw
from django.utils.crypto import get_random_string

from userprofile.serializers import UserProfileSerializers
from .serializers import DepositSerializers


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_deposit(request):
    amount = request.data['amount']
    user_account = Account.objects.get(user=request.user)
    ref_number = user_account.ref_number
    preboto_account = DepositAccount.objects.get(active=True)

    transaction_id = ''

    if not transaction_id:
        id_num = get_random_string(length=20,
                                   allowed_chars='123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqurstuvwxy')
        transaction_id = id_num

    while Deposit.objects.filter(transactionID=transaction_id).exists():
        id_num = get_random_string(length=20,
                                   allowed_chars='123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqurstuvwxy')
        transaction_id = id_num

    deposit = Deposit()
    deposit.user = request.user
    deposit.username = request.user.username
    deposit.amount = amount
    deposit.ref_number = ref_number
    deposit.bank_account = preboto_account
    deposit.transactionID = transaction_id
    deposit.pending = True
    deposit.verified = False
    deposit.failed = False
    deposit.complete = False
    deposit.save()

    return Response({'transaction_id': transaction_id, 'amount': amount})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_deposit_account(request):
    preboto_account = DepositAccount.objects.get(active=True)

    return Response({
        'acct_number': preboto_account.bank_account_number,
        'bank': preboto_account.bank_name,
        'account_name': preboto_account.bank_account_name
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_complete(request):
    transaction_id = request.data['transaction_id']
    deposit = Deposit.objects.get(transactionID=transaction_id)
    deposit.complete = True
    deposit.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def preboto_transfer(request):
    amount = request.data['amount']
    recipient = request.data['recipient']
    recipient_acct = Account.objects.get(account_number=recipient)

    transaction_id = ''
    if not transaction_id:
        id_num = get_random_string(length=20,
                                   allowed_chars='012345ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqurstuvwxyz')
        transaction_id = id_num

        while Transfer.objects.filter(transactionID=transaction_id).exists():
            id_num = get_random_string(length=20,
                                       allowed_chars='012345ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqurstuvwxyz')
            transaction_id = id_num

        transfer = Transfer()
        transfer.transactionID = transaction_id
        transfer.amount = amount
        transfer.user = request.user
        transfer.recipient = recipient_acct.user
        transfer.recipientName = recipient_acct.user
        transfer.senderName = request.user.username
        transfer.recipient_account_number = recipient
        transfer.pending = True
        transfer.complete = False
        transfer.failed = False
        transfer.save()
        return Response({'transaction_id': transaction_id})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_transfer_summary(request):
    transaction_id = request.data['transaction_id']
    transfer = Transfer.objects.get(transactionID=transaction_id)
    res_user = transfer.recipient
    profile = User.objects.get(username=res_user)
    fullname = f'{profile.first_name} {profile.last_name}'
    return Response({
        'amount': transfer.amount,
        'username': profile.username,
        'fullname': fullname,
        'accountNum': transfer.recipient_account_number,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_transfer_approved(request):
    transaction_id = request.data['transaction_id']
    pin = request.data['pin']
    transfer = Transfer.objects.get(transactionID=transaction_id)
    res_user = transfer.recipient
    recipient = Account.objects.get(user=res_user)
    sender = Account.objects.get(user=request.user)

    if pin == sender.transaction_code:
        # print('pin match')
        if sender.balance < transfer.amount:
            transfer.complete = False
            transfer.pending = False
            transfer.failed = True
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            #  print('funds avaliable')
            sender.balance = sender.balance - transfer.amount
            sender.save()
            recipient.balance = recipient.balance + transfer.amount
            recipient.save()
            transfer.complete = True
            transfer.pending = False
            transfer.failed = False
            transfer.save()
            return Response(status=status.HTTP_201_CREATED)
    else:
        print('pin didnt match')
        transfer.complete = False
        transfer.pending = False
        transfer.failed = True
        transfer.save()
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bank(request):
    bank = Bank.objects.filter(allowed=True).values()

    return Response({
        'bank': list(bank)
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_withdraw_account(request):
    bankname = request.data['bankname']
    bankcode = request.data['bankcode']
    name = request.data['name']
    number = request.data['number']

    bank = Bank.objects.get(bank_code=bankcode, bank_name=bankname)

    account = WithdrawAccount()
    account.bank = bank
    account.owner = request.user
    account.acct_name = name
    account.bank_name = bankname
    account.acct_number = number
    account.verified = True
    account.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def customer_withdraw(request):
    amount = request.data['amount']
    bankId = request.data['bank']
    bankname = request.data['bankname']
    acc_owner = request.data['owner']

    bank = WithdrawAccount.objects.get(pk=bankId, owner=acc_owner)
    account = Account.objects.get(user=request.user)

    transaction_id = ''
    if not transaction_id:
        id_num = get_random_string(length=20,
                                   allowed_chars='012345ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqursuvwxyz')
        transaction_id = id_num

        while Transfer.objects.filter(transactionID=transaction_id).exists():
            id_num = get_random_string(length=20,
                                       allowed_chars='012345ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqursuvwxyz')
            transaction_id = id_num

    withdraw = Withdraw()
    withdraw.amount = amount
    withdraw.user = request.user
    withdraw.username = request.user.username
    withdraw.ref_number = account.ref_number
    withdraw.bank = bank
    withdraw.transactionID = transaction_id
    withdraw.pending = True
    withdraw.complete = False
    withdraw.failed = False
    withdraw.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_withdraw_account(request):
    bank = WithdrawAccount.objects.filter(owner=request.user).values()
    return Response({
        'bank': list(bank)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_deposit_transactions(request):
    deposit = Deposit.objects.filter(user=request.user).order_by('-timestamp').values()
    return Response({
        'deposit': list(deposit)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transfer_transactions(request):
    transfer = Transfer.objects.filter(user=request.user).order_by('-timestamp').values()
    return Response({
        'transfer': list(transfer)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_withdraw_transactions(request):
    withdraw = Withdraw.objects.filter(user=request.user).order_by('-timestamp').values()
    return Response({
        'withdraw': list(withdraw)
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_withdraw_account_detail(request):
    bankId = request.data['bank']
    bank = WithdrawAccount.objects.get(pk=bankId, owner=request.user)
    return Response({
        'bankName': bank.bank_name,
        'accName': bank.acct_name,
        'accNumber': bank.acct_number
    })
