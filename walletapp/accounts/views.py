from django.shortcuts import render, redirect
from accounts.forms import WalletUserRegistrationForm, WalletUserLoginForm
from wallet.models import UserWallet

# Create your views here.
from django.http import HttpResponse
import datetime
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from accounts.models import WalletUser


def register(request):
    print("Entering register page")
    form = WalletUserRegistrationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            kwargs = {
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "is_premium_user": form.cleaned_data["is_premium_user"],
            }
            user = WalletUser.objects.create_user(
                email=email, password=password, **kwargs
            )
            if user.is_premium_user:
                UserWallet.objects.create(wallet_amount=2500, wallet_user=user)
                print(
                    f"Premium user wallet created and Rs:1000 credited for user {user}."
                )
            else:
                UserWallet.objects.create(wallet_amount=1000, wallet_user=user)
                print(
                    f"Normal user wallet created and Rs:1000 credited for user {user}."
                )

            print("User Registration Successfull")
            return redirect("login")
        else:
            context = {"form": form}
            print("Some error in form")
            return render(request, "accounts/register.html", context)
    print("Get Method, opening page")
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def login(request):
    form = WalletUserLoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("homepage")
            else:
                print("Invalid credentials")
                context = {"form": form}
                return render(request, "accounts/login.html", context)
        else:
            print("Form invalid")
            context = {"form": form}
            return render(request, "accounts/login.html", context)
    context = {"form": form}
    return render(request, "accounts/login.html", context)


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    print("user successfully logged out")
    return redirect("homepage")
