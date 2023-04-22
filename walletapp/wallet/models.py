from django.db import models
from accounts.models import WalletUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# Create your models here.


class UserWallet(models.Model):
    wallet_amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    wallet_user = models.ForeignKey(WalletUser, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    last_updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.wallet_user.get_full_name()} - {self.wallet_amount}"

class WalletTransaction(models.Model):
    transaction_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_uuid
    
    class Meta:
        verbose_name        = 'WalletTransactionID'
        verbose_name_plural = 'WalletTransactionIDs'


class WalletTransactions(models.Model):
    TRANSACTION_METHOD_CHOICES = (
        ("debit", "Debit"),
        ("credit", "Credit"),
        ("charges", "Charges")
    )
    transaction_id = models.ForeignKey(WalletTransaction, on_delete=models.CASCADE)
    transaction_amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    transaction_method = models.CharField(
        max_length=10, choices=TRANSACTION_METHOD_CHOICES
    )
    transaction_user = models.ForeignKey(
        WalletUser, on_delete=models.CASCADE, related_name="sent_transactions"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_amount} {self.transaction_method}ed"
    
    class Meta:
        verbose_name        = 'WalletTransactions'
        verbose_name_plural = 'WalletTransactions'
