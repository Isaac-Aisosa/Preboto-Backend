from django.urls import path
from . import views
from .views import AdminAuthToken

urlpatterns = [

    path('api-admin-login/', AdminAuthToken.as_view()),
    path('api-admin-get-account-count/', views.get_account_count),
    path('api-admin-get-new-deposit/', views.get_pending_deposit_count),
    path('api-admin-get-withdraw-request/', views.get_withdraw_request_count),
    path('api-admin-get-trade-account-balance/', views.get_trade_account_balance),
    path('api-admin-get-new-deposits/', views.new_deposit),
    path('api-admin-get-deposit_details/', views.admin_get_deposit_details),
    path('api-admin-confirmed-deposit/', views.admin_confirm_deposit),
    path('api-admin-Failed-deposit/', views.admin_failed_deposit),
    path('api-admin-withdraw-request/', views.admin_withdraw_request),
    path('api-admin-get-WithdrawRequest_details/', views.admin_get_withdraw_request_details),
    path('api-admin-get-Withdraw_complete/', views.admin_complete_withdraw),
    path('api-admin-get-Withdraw_terminated/', views.admin_terminate_withdraw),
    path('api-admin-get-confirmed-Deposit/', views.admin_get_confirmed_deposit),
    path('api-admin-get-pending-Deposit/', views.admin_get_pending_deposit),
    path('api-admin-get-failed-Deposit/', views.admin_get_failed_deposit),
    path('api-admin-get-draft-Deposit/', views.admin_get_draft_deposit),
    path('api-admin-deposit-search/', views.admin_deposit_search),
    path('api-admin-get-confirmed-Withdraw/', views.admin_get_confirmed_withdraw),
    path('api-admin-get-pending-Withdraw/', views.admin_get_pending_withdraw),
    path('api-admin-get-failed-Withdraw/', views.admin_get_failed_withdraw),
    path('api-admin-withdraw-search/', views.admin_withdraw_search),
    path('api-admin-get-complete-transfer/', views.admin_get_complete_transfer),
    path('api-admin-get-pending-transfer/', views.admin_get_pending_transfer),
    path('api-admin-get-failed-transfer/', views.admin_get_failed_transfer),
    path('api-admin-transfer-search/', views.admin_transfer_search),
    path('api-admin-get-accounts/', views.admin_get_accounts),
    path('api-admin-accounts-search/', views.admin_accounts_search),
    path('api-admin-open-daily-trade/', views.admin_open_daily_trade),
    path('api-admin-get-current-opened-trade/', views.admin_get_current_daily_trade),
    path('api-admin-close-daily-trade/', views.admin_close_daily_trade),
    path('api-admin-get-daily-trades/', views.admin_get_daily_trades),
    path('api-admin-get-trades-history/', views.admin_get_trades_history),
    path('api-admin-get-revenue-history/', views.admin_get_revenue_history),
    path('api-admin-get-revenue-account/', views.admin_get_revenue_account),
    path('api-admin-get-trades-growth/', views.admin_get_trades_growth),

    #General Account management API
    path('api-admin-deposit-account-transfer/', views.admin_deposit_account_transfer),
    path('api-admin-deposit-account-transfer-history/', views.admin_get_deposit_account_transfer_history),
]
