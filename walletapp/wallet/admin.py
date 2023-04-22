from django.contrib import admin
from wallet.models import WalletTransactions, UserWallet, WalletTransaction

# Register your models here.
admin.site.register(WalletTransactions)
admin.site.register(UserWallet)
admin.site.register(WalletTransaction)
