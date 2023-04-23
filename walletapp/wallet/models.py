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
    transaction_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    paying_user = models.ForeignKey(
        WalletUser, on_delete=models.CASCADE, related_name="paid_transactions"
    )
    receiving_user = models.ForeignKey(
        WalletUser, on_delete=models.CASCADE, related_name="collected_transactions"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_uuid}"

    class Meta:
        verbose_name = "WalletTransactionID"
        verbose_name_plural = "WalletTransactionIDs"


class WalletTransactions(models.Model):
    TRANSACTION_METHOD_CHOICES = (
        ("debit", "Debit"),
        ("credit", "Credit"),
        ("charges", "Charges"),
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
    receiving_user = models.ForeignKey(
        WalletUser, on_delete=models.CASCADE, related_name="received_transactions"
    )
    remarks = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.remarks}"

    class Meta:
        verbose_name = "WalletTransactions"
        verbose_name_plural = "WalletTransactions"


class TransactionCharges(models.Model):
    user_type = models.CharField(max_length=20)
    sending_charge = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(25)],
    )
    receiving_charge = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(25)],
    )

    def __str__(self) -> str:
        return f"{self.user_type} - Sending charges = {self.sending_charge}% | Receiving charges = {self.receiving_charge}%."

    class Meta:
        verbose_name = "TransactionCharge"
        verbose_name_plural = "TransactionCharges"


class PaymentRequest(models.Model):
    requesting_user = models.ForeignKey(
        WalletUser, on_delete=models.CASCADE, related_name="payment_requesting_user"
    )
    paying_user = models.ForeignKey(
        WalletUser, on_delete=models.CASCADE, related_name="paying_user"
    )
    request_amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    is_completed = models.BooleanField(default=False)
    request_creation_date = models.DateTimeField(auto_now_add=True)
    request_completed_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.requesting_user} requested {self.request_amount} from {self.paying_user} - Status: {'Completed' if self.is_completed else 'Pending'}"
