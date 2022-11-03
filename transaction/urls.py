from django.urls import path
from . import views

from .views import create_deposit
urlpatterns = [
      path("api-customer-create-deposit/", views.create_deposit),
      path("api-get-deposit-account/", views.get_deposit_account),
      path("api-deposit-complete/", views.deposit_complete),
      path("api-preboto-transfer/", views.preboto_transfer),
      path("api-transfer-summary/", views.get_transfer_summary),
      path("api-transfer-approved/", views.get_transfer_approved),
      path("api-get-bank/", views.get_bank),
      path("api-get-withdraw-account/", views.get_withdraw_account),
      path("api-add-withdraw-account/", views.add_withdraw_account),
      path("api-customer-withdraw/", views.customer_withdraw),
      path("api-get-deposit-transaction/", views.get_deposit_transactions),
      path("api-get-transfer-transaction/", views.get_transfer_transactions),
      path("api-get-withdraw-transaction/", views.get_withdraw_transactions),
      path("api-get-withdraw-account-detail/", views.get_withdraw_account_detail),
]
