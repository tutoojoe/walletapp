from django import forms
from wallet.models import UserWallet, WalletTransactions
from django.contrib.auth import get_user_model


class TransactionRequestForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=get_user_model().objects.exclude(is_superuser=True)
    )
    CHOICES = (
        ("make_payment", "Make Payment"),
        ("request_payment", "Request Payment"),
    )
    make_payment_or_request_payment = forms.ChoiceField(
        choices=CHOICES, widget=forms.Select()
    )
    transaction_amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop("current_user", None)
        super(TransactionRequestForm, self).__init__(*args, **kwargs)
        if current_user:
            self.fields["user"].queryset = self.fields["user"].queryset.exclude(
                pk=current_user.pk
            )

    class Meta:
        fields = ["make_payment_or_request_payment", "transaction_amount", "user"]
