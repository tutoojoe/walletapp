from django import forms
from accounts.models import WalletUser


class WalletUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter Password"})
    )

    class Meta:
        model = WalletUser
        fields = ["first_name", "last_name", "email", "is_premium_user", "password"]


class WalletUserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter Password"})
    )
