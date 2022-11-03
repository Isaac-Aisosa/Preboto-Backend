from django.urls import path
from . import views

from .views import CreateTransactionCode
urlpatterns = [
      path("api-create-transaction_code/", CreateTransactionCode.as_view()),
      path("api-get-account-balance/", views.get_account_balance),
      path("api-get-account-trade-history/", views.get_account_trade_history),
      path("api-get-last-account-trade/", views.get_last_client_account_trade),
      path("api-get-last-six-account-trade/", views.get_last_six_client_account_trade),
]
