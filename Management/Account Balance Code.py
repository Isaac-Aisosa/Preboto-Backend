



#Account Balance code solution one
# problem or bug
#  missing values in balanced account

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def admin_close_daily_trade(request):
#     Amount = request.data['closeAmount']
#     closedAmount = int(Amount)
#     trade = DailyTrade.objects.get(timestamp__gte=datetime.date.today(), opened=True)
#     prebotoConstant = PrebotoConstant.objects.get(active=True)
#     userAccounts = Account.objects.filter(approved=True)
#
#     revenueAccount = RevenueAccount.objects.get(active=True)
#     generalAccount = DepositAccount.objects.get(active=True)
#     clientsGainPercent = prebotoConstant.clientsGainPercent
#     prebotoGainPercent = prebotoConstant.prebotoGainPercent
#     clientsLossPercent = prebotoConstant.clientsLossPercent
#     prebotoLossPercent = prebotoConstant.prebotoLossPercent
#     # Get trade return
#     returns = closedAmount - trade.inputAmount
#
#     # Calculate When there is GAIN
#     if closedAmount >= trade.inputAmount:
#         print("GAIN")
#         generalAccount.balance += returns
#         generalAccount.save()
#         perIncrease = returns / trade.inputAmount
#         trade.opened = False
#         trade.outputAmount = closedAmount
#         trade.returns = returns
#         trade.closed = True
#         trade.closeTime = datetime.datetime.now()
#         trade.gain = True
#         trade.save()
#
#         for client in userAccounts:
#             interest = client.balance * perIncrease
#             clientShare = clientsGainPercent / 100
#             share = interest * clientShare
#
#             # Create client trade history
#             client_trade_history = ClientTradeHistory()
#             client_trade_history.inputAmount = client.balance
#             client_trade_history.outputAmount = client.balance + share
#             client_trade_history.returns = share
#             client_trade_history.username = client.userName
#             client_trade_history.user = client.user
#             client_trade_history.gain = True
#             client_trade_history.save()
#
#             # cal client share
#
#             client.interest_rate = share
#             client.balance = client.balance + share
#             client.save()  # saving client account after trade history has been saved
#
#             # take company revenue
#             companyShare = prebotoGainPercent / 100
#             revenue = interest * companyShare
#             revenueAccount.balance += revenue
#             revenueAccount.save()
#
#             # Update temp account and main account
#             userTempAccount = TemporaryAccount.objects.get(user=client.user)
#
#             client.balance += userTempAccount.balance
#             client.save()
#
#             userTempAccount.balance = 0
#             userTempAccount.save()
#
#
#
#
#     # Calculate When there is GAIN
#     elif closedAmount < trade.inputAmount:
#         print("LOSS")
#         generalAccount.balance += returns
#         generalAccount.save()
#         perIncrease = returns / trade.inputAmount
#         trade.opened = False
#         trade.outputAmount = closedAmount
#         trade.returns = returns
#         trade.closed = True
#         trade.closeTime = datetime.datetime.now()
#         trade.loss = True
#         trade.save()
#
#         for client in userAccounts:
#             interest = client.balance * perIncrease
#
#             # cal client share
#             clientShare = clientsLossPercent / 100
#             share = interest * clientShare
#             # Create client trade history
#             client_trade_history = ClientTradeHistory()
#             client_trade_history.inputAmount = client.balance
#             client_trade_history.outputAmount = client.balance + share
#             client_trade_history.returns = share
#             client_trade_history.username = client.userName
#             client_trade_history.user = client.user
#             client_trade_history.loss = True
#             client_trade_history.save()
#
#             client.interest_rate = share
#             client.balance = client.balance + share
#             client.save()  # saving client account after trade history has been saved
#
#             # take company revenue
#             companyShare = prebotoLossPercent / 100
#             revenue = interest * companyShare
#             revenueAccount.balance += revenue
#             revenueAccount.save()
#
#             # Update temp account and main account
#             userTempAccount = TemporaryAccount.objects.get(user=client.user)
#
#             client.balance += userTempAccount.balance
#             client.save()
#
#             userTempAccount.balance = 0
#             userTempAccount.save()
#
#     return Response(status=status.HTTP_201_CREATED)
