from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Deposit)
admin.site.register(Transfer)
admin.site.register(Withdraw)
admin.site.register(Bank)
admin.site.register(WithdrawAccount)
#admin.site.register(CustomerTransaction)
