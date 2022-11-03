from django.shortcuts import render
from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, generics

from rest_framework import status
from django.http import Http404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from user_accounts.models import Account, TemporaryAccount
from transaction.models import Deposit, Withdraw, WithdrawAccount, Transfer
from General_Account.models import DepositAccount, PrebotoWithdrawAccount, RevenueAccount, ServiceAccount, \
    UtilityAccount
from django.db.models import Sum, Q
from .models import DailyTrade, PrebotoConstant, ClientTradeHistory, RevenueHistory, AccountTransactionHistory
from itertools import chain
import datetime
from django.shortcuts import get_object_or_404


class AdminAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if user.is_staff:
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'username': user.username,
                'firstname': user.first_name,
                'lastname': user.last_name
            })
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_account_count(request):
    # users = User.objects.all()
    accounts = Account.objects.all().count()

    return Response({
        "accounts": accounts
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pending_deposit_count(request):
    # users = User.objects.all()
    deposit = Deposit.objects.filter(pending=True, complete=True).count()

    return Response({
        "deposit": deposit
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_withdraw_request_count(request):
    # users = User.objects.all()
    withdraw = Withdraw.objects.filter(pending=True).count()

    return Response({
        "withdraw": withdraw
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trade_account_balance(request):
    # users = User.objects.all()
    account = DepositAccount.objects.get(active=True)

    return Response({
        "balance": account.balance
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def new_deposit(request):
    # users = User.objects.all()
    deposit = Deposit.objects.filter(pending=True, complete=True).order_by('-timestamp').values()

    return Response({
        "deposit": list(deposit)
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_get_deposit_details(request):
    transID = request.data['transactionID']

    deposit = Deposit.objects.get(transactionID=transID, pending=True, complete=True, confirmed=False)

    return Response({'transaction_id': deposit.transactionID,
                     'amount': deposit.amount,
                     'username': deposit.username,
                     'ref_number': deposit.ref_number,
                     'time': deposit.timestamp,

                     })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_confirm_deposit(request):
    transID = request.data['transactionID']
    deposit = Deposit.objects.get(transactionID=transID, pending=True, complete=True, confirmed=False)

    client_account = Account.objects.get(user=deposit.user)
    client_temp_account = TemporaryAccount.objects.get(user=deposit.user)
    preboto_account = DepositAccount.objects.get(active=True)

    open_trade = DailyTrade.objects.filter(timestamp__gte=datetime.date.today(), opened=True)
    if open_trade.exists():
        # print('Found')
        client_temp_account.balance += deposit.amount
        client_temp_account.save()
    else:
        # print('no current trade is opened')
        client_account.balance += deposit.amount
        client_account.save()

    preboto_account.balance += deposit.amount
    preboto_account.save()

    deposit.confirmed = True
    deposit.failed = False
    deposit.pending = False
    deposit.confirmedBy = request.user.username
    deposit.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_failed_deposit(request):
    transID = request.data['transactionID']
    deposit = Deposit.objects.get(transactionID=transID, pending=True, complete=True, confirmed=False)
    deposit.confirmed = False
    deposit.failed = True
    deposit.pending = False
    deposit.confirmedBy = request.user.username
    deposit.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_withdraw_request(request):
    # users = User.objects.all()
    withdraw = Withdraw.objects.filter(pending=True, complete=False).order_by('-timestamp').values()
    preboto_withdraw = PrebotoWithdrawAccount.objects.get(active=True)
    withdrawAmmount = Withdraw.objects.filter(pending=True, complete=False).aggregate(Sum('amount'))
    return Response({
        "withdraw": list(withdraw),
        "preboto_account": preboto_withdraw.balance,
        "withdrawAmmount": withdrawAmmount
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_get_withdraw_request_details(request):
    transID = request.data['transactionID']
    withdraw = Withdraw.objects.get(transactionID=transID, pending=True, complete=False)

    bank = WithdrawAccount.objects.get(pk=withdraw.bank.pk, owner=withdraw.user)
    account = Account.objects.get(user=withdraw.user)
    return Response({'transaction_id': withdraw.transactionID,
                     'amount': withdraw.amount,
                     'username': withdraw.username,
                     'ref_number': withdraw.ref_number,
                     'time': withdraw.timestamp,
                     'bank_name': bank.bank_name,
                     'bank_acct_number': bank.acct_number,
                     'bank_acct_name': bank.acct_name,
                     'account_balance': account.balance,

                     })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_complete_withdraw(request):
    transID = request.data['transactionID']
    withdraw = Withdraw.objects.get(transactionID=transID, pending=True, complete=False)
    preboto_withdraw = PrebotoWithdrawAccount.objects.get(active=True)
    account = Account.objects.get(user=withdraw.user)
    account.balance -= withdraw.amount
    account.save()
    preboto_withdraw.balance -= withdraw.amount
    preboto_withdraw.save()
    withdraw.complete = True
    withdraw.pending = False
    withdraw.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_terminate_withdraw(request):
    transID = request.data['transactionID']
    withdraw = Withdraw.objects.get(transactionID=transID, pending=True, complete=False)
    withdraw.complete = False
    withdraw.pending = False
    withdraw.failed = True
    withdraw.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_confirmed_deposit(request):
    deposit = Deposit.objects.filter(confirmed=True).order_by('-timestamp').values()
    depositAmount = Deposit.objects.filter(confirmed=True)
    depositCount = Deposit.objects.filter(confirmed=True).count()
    return Response({
        "deposit": list(deposit),
        "depositAmount": depositAmount.aggregate(Sum('amount')),
        "depositCount": depositCount
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_pending_deposit(request):
    deposit = Deposit.objects.filter(pending=True, complete=True).order_by('-timestamp').values()
    depositAmount = Deposit.objects.filter(pending=True, complete=True)
    depositCount = Deposit.objects.filter(pending=True, complete=True).count()
    return Response({
        "deposit": list(deposit),
        "depositAmount": depositAmount.aggregate(Sum('amount')),
        "depositCount": depositCount
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_failed_deposit(request):
    deposit = Deposit.objects.filter(failed=True).order_by('-timestamp').values()
    depositAmount = Deposit.objects.filter(failed=True)
    depositCount = Deposit.objects.filter(failed=True).count()
    return Response({
        "deposit": list(deposit),
        "depositAmount": depositAmount.aggregate(Sum('amount')),
        "depositCount": depositCount
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_draft_deposit(request):
    deposit = Deposit.objects.filter(complete=False).order_by('-timestamp').values()
    depositAmount = Deposit.objects.filter(complete=False)
    depositCount = Deposit.objects.filter(complete=False).count()
    return Response({
        "deposit": list(deposit),
        "depositAmount": depositAmount.aggregate(Sum('amount')),
        "depositCount": depositCount
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_deposit_search(request):
    query = request.data['search']
    if query is not None:
        lookups = Q(amount__iexact=query) | Q(username__iexact=query) | Q(transactionID__iexact=query) | \
                  Q(ref_number__iexact=query)

        deposit = Deposit.objects.filter(lookups).distinct().values()
        depositAmount = Deposit.objects.filter(lookups).distinct()
        depositCount = Deposit.objects.filter(lookups).distinct().count()
        return Response({
            "deposit": list(deposit),
            "depositAmount": depositAmount.aggregate(Sum('amount')),
            "depositCount": depositCount
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_confirmed_withdraw(request):
    withdraw = Withdraw.objects.filter(complete=True).order_by('-timestamp').values()
    withdrawAmount = Withdraw.objects.filter(complete=True)
    withdrawCount = Withdraw.objects.filter(complete=True).count()
    return Response({
        "withdraw": list(withdraw),
        "withdrawAmount": withdrawAmount.aggregate(Sum('amount')),
        "withdrawCount": withdrawCount
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_pending_withdraw(request):
    withdraw = Withdraw.objects.filter(pending=True).order_by('-timestamp').values()
    withdrawAmount = Withdraw.objects.filter(pending=True)
    withdrawCount = Withdraw.objects.filter(pending=True).count()
    return Response({
        "withdraw": list(withdraw),
        "withdrawAmount": withdrawAmount.aggregate(Sum('amount')),
        "withdrawCount": withdrawCount
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_failed_withdraw(request):
    withdraw = Withdraw.objects.filter(failed=True).order_by('-timestamp').values()
    withdrawAmount = Withdraw.objects.filter(failed=True)
    withdrawCount = Withdraw.objects.filter(failed=True).count()
    return Response({
        "withdraw": list(withdraw),
        "withdrawAmount": withdrawAmount.aggregate(Sum('amount')),
        "withdrawCount": withdrawCount
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_withdraw_search(request):
    query = request.data['search']
    if query is not None:
        lookups = Q(amount__iexact=query) | Q(username__iexact=query) | Q(transactionID__iexact=query) | \
                  Q(ref_number__iexact=query)

        withdraw = Withdraw.objects.filter(lookups).distinct().values()
        withdrawAmount = Withdraw.objects.filter(lookups).distinct()
        withdrawCount = Withdraw.objects.filter(lookups).distinct().count()
        return Response({
            "withdraw": list(withdraw),
            "withdrawAmount": withdrawAmount.aggregate(Sum('amount')),
            "withdrawCount": withdrawCount
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_complete_transfer(request):
    transfer = Transfer.objects.filter(complete=True).order_by('-timestamp').values()
    transferAmount = Transfer.objects.filter(complete=True)
    transferCount = Transfer.objects.filter(complete=True).count()
    return Response({
        "transfer": list(transfer),
        "transferAmount": transferAmount.aggregate(Sum('amount')),
        "transferCount": transferCount
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_pending_transfer(request):
    transfer = Transfer.objects.filter(pending=True).order_by('-timestamp').values()
    transferAmount = Transfer.objects.filter(pending=True)
    transferCount = Transfer.objects.filter(pending=True).count()
    return Response({
        "transfer": list(transfer),
        "transferAmount": transferAmount.aggregate(Sum('amount')),
        "transferCount": transferCount
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_failed_transfer(request):
    transfer = Transfer.objects.filter(failed=True).order_by('-timestamp').values()
    transferAmount = Transfer.objects.filter(failed=True)
    transferCount = Transfer.objects.filter(failed=True).count()
    return Response({
        "transfer": list(transfer),
        "transferAmount": transferAmount.aggregate(Sum('amount')),
        "transferCount": transferCount
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_transfer_search(request):
    query = request.data['search']
    if query is not None:
        lookups = Q(amount__iexact=query) | Q(senderName__iexact=query) | Q(transactionID__iexact=query) | \
                  Q(recipient_account_number__iexact=query) | Q(recipientName__iexact=query)

        transfer = Transfer.objects.filter(lookups).distinct().values()
        transferAmount = Transfer.objects.filter(lookups).distinct()
        transferCount = Transfer.objects.filter(lookups).distinct().count()
        return Response({
            "transfer": list(transfer),
            "transferAmount": transferAmount.aggregate(Sum('amount')),
            "transferCount": transferCount
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_accounts(request):
    accounts = Account.objects.all().order_by('-balance').values()
    accountsAmount = Account.objects.all()
    accountsCount = Account.objects.all().count()
    return Response({
        "accounts": list(accounts),
        "accountsAmount": accountsAmount.aggregate(Sum('balance')),
        "accountsCount": accountsCount
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_accounts_search(request):
    query = request.data['search']
    if query is not None:
        lookups = Q(balance__iexact=query) | Q(userName__iexact=query) | Q(account_number__iexact=query) | \
                  Q(ref_number__iexact=query) | Q(interest_rate__iexact=query)

        accounts = Account.objects.filter(lookups).distinct().values()
        accountsAmount = Account.objects.filter(lookups).distinct()
        accountsCount = Account.objects.filter(lookups).distinct().count()
        return Response({
            "accounts": list(accounts),
            "accountsAmount": accountsAmount.aggregate(Sum('balance')),
            "accountsCount": accountsCount
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_open_daily_trade(request):
    inputAmount = request.data['inputAmount']
    name = request.data['name']
    username = request.user.username
    trade = DailyTrade()
    trade.tradeName = name
    trade.inputAmount = inputAmount
    trade.opened = True
    trade.terminalUser = request.user
    trade.terminal = username
    trade.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_current_daily_trade(request):
    trade = DailyTrade.objects.get(timestamp__gte=datetime.date.today(), opened=True)
    return Response({
        "tradeName": trade.tradeName,
        "tradeInputAmount": trade.inputAmount,
        "tradeOpened": trade.opened,
        "tradeTerminal": trade.terminal,
        "tradeOpenTime": trade.openTime,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_daily_trades(request):
    trade = DailyTrade.objects.filter(timestamp__gte=datetime.date.today()).order_by('-timestamp').values()
    return Response({
        "trade": list(trade),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_trades_history(request):
    trade = DailyTrade.objects.all().order_by('-timestamp').values()
    return Response({
        "trade": list(trade),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_trades_growth(request):
    trade = DailyTrade.objects.last()
    return Response({
        "inputAmount": trade.inputAmount,
        "outputAmount": trade.outputAmount,
        "return": trade.returns,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_revenue_history(request):
    revenue = RevenueHistory.objects.all().order_by('-timestamp').values()
    return Response({
        "revenue": list(revenue),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_revenue_account(request):
    revenue = RevenueAccount.objects.get(active=True)

    return Response({
        "balance": revenue.balance,
        "bank_name": revenue.bank_name,
        "bank_account_number": revenue.bank_account_number,
        "bank_account_name": revenue.bank_account_name,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_close_daily_trade(request):
    Amount = request.data['closeAmount']
    closedAmount = int(Amount)
    trade = DailyTrade.objects.get(timestamp__gte=datetime.date.today(), opened=True)
    prebotoConstant = PrebotoConstant.objects.get(active=True)
    userAccounts = Account.objects.filter(approved=True)

    revenueAccount = RevenueAccount.objects.get(active=True)
    generalAccount = DepositAccount.objects.get(active=True)
    clientsGainPercent = prebotoConstant.clientsGainPercent
    prebotoGainPercent = prebotoConstant.prebotoGainPercent
    clientsLossPercent = prebotoConstant.clientsLossPercent
    prebotoLossPercent = prebotoConstant.prebotoLossPercent

    # Calculate When there is GAIN
    if closedAmount >= trade.inputAmount:
        print("GAIN")
        # Get trade return
        general_returns = closedAmount - trade.inputAmount
        generalAccount.balance += general_returns
        generalAccount.save()

        companyPercent = prebotoGainPercent / 100
        prebotoRevenue = general_returns * companyPercent

        # save Preboto revenue or profit history
        revenue = RevenueHistory()
        revenue.previousBalance = revenueAccount.balance
        revenue.newBalance = revenueAccount.balance + prebotoRevenue
        revenue.growth = (revenueAccount.balance + prebotoRevenue) - revenueAccount.balance
        revenue.trade = trade
        revenue.save()
        # Calculate Preboto revenue or profit
        revenueAccount.balance += prebotoRevenue
        revenueAccount.save()

        # Calculate client returns

        clients_return = general_returns - prebotoRevenue
        ClientPercentageReturn = clients_return / trade.inputAmount

        trade.opened = False
        trade.outputAmount = closedAmount
        trade.returns = general_returns
        trade.closed = True
        trade.closeTime = datetime.datetime.now()
        trade.gain = True
        trade.save()

        for client in userAccounts:
            growth = client.balance * ClientPercentageReturn

            # Create client trade history
            client_trade_history = ClientTradeHistory()
            client_trade_history.inputAmount = client.balance
            client_trade_history.outputAmount = client.balance + growth
            client_trade_history.returns = growth
            client_trade_history.username = client.userName
            client_trade_history.user = client.user
            client_trade_history.gain = True
            client_trade_history.save()

            client.interest_rate = growth
            client.balance += growth
            client.save()  # saving client account after trade history has been saved

            # Update temp account and main account
            userTempAccount = TemporaryAccount.objects.get(user=client.user)

            client.balance += userTempAccount.balance
            client.save()

            userTempAccount.balance = 0
            userTempAccount.save()

    # Calculate When there is LOSS
    elif closedAmount < trade.inputAmount:
        print("LOSS")
        # Get trade return
        general_returns = closedAmount - trade.inputAmount
        generalAccount.balance += general_returns
        generalAccount.save()

        # Calculate Preboto commission or profit
        companyPercent = prebotoLossPercent / 100
        prebotoRevenue = general_returns * companyPercent

        # save Preboto revenue or profit history
        revenue = RevenueHistory()
        revenue.previousBalance = revenueAccount.balance
        revenue.newBalance = revenueAccount.balance + prebotoRevenue
        revenue.growth = (revenueAccount.balance + prebotoRevenue) - revenueAccount.balance
        revenue.trade = trade
        revenue.save()

        # Calculate Preboto revenue or profit
        revenueAccount.balance += prebotoRevenue
        revenueAccount.save()

        # Calculate client returns

        clients_return = general_returns - prebotoRevenue
        ClientPercentageReturn = clients_return / trade.inputAmount

        trade.opened = False
        trade.outputAmount = closedAmount
        trade.returns = general_returns
        trade.closed = True
        trade.closeTime = datetime.datetime.now()
        trade.loss = True
        trade.save()

        for client in userAccounts:
            growth = client.balance * ClientPercentageReturn

            # Create client trade history
            client_trade_history = ClientTradeHistory()
            client_trade_history.inputAmount = client.balance
            client_trade_history.outputAmount = client.balance + growth
            client_trade_history.returns = growth
            client_trade_history.username = client.userName
            client_trade_history.user = client.user
            client_trade_history.loss = True
            client_trade_history.save()

            client.interest_rate = growth
            client.balance += growth
            client.save()  # saving client account after trade history has been saved

            # Update temp account and main account
            userTempAccount = TemporaryAccount.objects.get(user=client.user)

            client.balance += userTempAccount.balance
            client.save()

            userTempAccount.balance = 0
            userTempAccount.save()

    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_deposit_account_transfer(request):
    amount = request.data['amount']
    account = request.data['account']
    depositAccount = DepositAccount.objects.get(active=True)
    withdrawAccount = PrebotoWithdrawAccount.objects.get(active=True)
    revenueAccount = RevenueAccount.objects.get(active=True)
    serviceAccount = ServiceAccount.objects.get(active=True)
    utilityAccount = UtilityAccount.objects.get(active=True)

    if account == "WithdrawAccount":
        if depositAccount.balance < int(amount):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            depositAccount.balance -= int(amount)
            depositAccount.save()
            withdrawAccount.balance += int(amount)
            withdrawAccount.save()

            tansHistory = AccountTransactionHistory()
            tansHistory.account = "Deposit Account"
            tansHistory.Recipient_account = "Withdraw Account"
            tansHistory.Amount = int(amount)
            tansHistory.terminalUser = request.user.username
            tansHistory.save()

    elif account == "ServiceAccount":
        pass
    elif account == "RevenueAccount":
        pass
    elif account == "UtilityAccount":
        pass

    transHistory = AccountTransactionHistory()

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_deposit_account_transfer_history(request):
    transfer = AccountTransactionHistory.objects.filter(account="Deposit Account").order_by('-timestamp').values()

    return Response({
        "transfer": list(transfer),
    })
