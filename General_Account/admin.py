from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(DepositAccount)
admin.site.register(PrebotoWithdrawAccount)
admin.site.register(RevenueAccount)
admin.site.register(ServiceAccount)
admin.site.register(UtilityAccount)