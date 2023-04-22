from django.shortcuts import render
from accounts.forms import WalletUserRegistrationForm
from wallet.forms import TransactionRequestForm

# Create your views here.
from django.http import HttpResponse
import datetime


def homepage(request):
    print("Printing homepage")
    form = WalletUserRegistrationForm()
    context = {"form": form}
    return render(request, "homepage.html", context)


def pay_or_receive(request):
    print("pay or receive page")
    form = TransactionRequestForm()
    context = {"form": form}
    return render(request, "wallet/pay-or-receive.html", context)
