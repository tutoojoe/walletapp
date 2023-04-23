from django.shortcuts import render, redirect
from accounts.forms import WalletUserRegistrationForm
from wallet.forms import TransactionRequestForm
from accounts.models import WalletUser

# Create your views here.
from django.http import HttpResponse
import datetime
import uuid
from django.contrib.auth.decorators import login_required
from wallet.models import (
    TransactionCharges,
    WalletTransaction,
    UserWallet,
    WalletTransactions,
    PaymentRequest,
)


def homepage(request):
    print("Printing homepage")
    if request.user.is_authenticated:
        wallet = UserWallet.objects.get(wallet_user=request.user)
        created_payment_requests_count = PaymentRequest.objects.filter(
            requesting_user=request.user, is_completed=False
        ).count()
        received_payment_requests_count = PaymentRequest.objects.filter(
            paying_user=request.user, is_completed=False
        ).count()

        context = {
            "wallet": wallet,
            "received_payment_requests_count": received_payment_requests_count,
            "created_payment_requests_count": created_payment_requests_count,
        }
    return render(request, "homepage.html", context)


def get_charges(user):
    if user.is_premium_user:
        charges = TransactionCharges.objects.filter(user_type="premium")[0]
    else:
        charges = TransactionCharges.objects.filter(user_type="normal")[0]
    return charges


def make_transaction(
    transaction_id,
    transaction_amount,
    transaction_method,
    transaction_user,
    receiving_user,
):
    remarks = f"Amount {transaction_amount} {transaction_method}ed from {transaction_user} to {receiving_user}."
    WalletTransactions.objects.create(
        transaction_id=transaction_id,
        transaction_amount=transaction_amount,
        transaction_method="debit",
        transaction_user=transaction_user,
        receiving_user=receiving_user,
        remarks=remarks,
    )
    return


def make_payment(request, payment_data):
    # Check the user is premium or not.
    # create a transaction id
    paying_user = request.user
    receiving_user = payment_data.get("selected_user")
    superuser = WalletUser.objects.filter(is_superuser=True).first()
    superuser_wallet = UserWallet.objects.filter(wallet_user=superuser)[0]

    paying_user_charges = get_charges(paying_user)
    receiving_user_charge = get_charges(receiving_user)

    # Calculating sending amount
    paying_charges = paying_user_charges.sending_charge
    receiving_charges = receiving_user_charge.receiving_charge
    transaction_amount = payment_data.get("transaction_amount")
    payment_charge_amount = transaction_amount * (paying_charges / 100)
    receiving_charge_amount = transaction_amount * (receiving_charges / 100)

    total_amount = transaction_amount + payment_charge_amount
    paying_user_wallet = UserWallet.objects.filter(wallet_user=paying_user)[0]

    if paying_user_wallet.wallet_amount < total_amount:
        print("not enough balance left")
        return
    transaction_id = WalletTransaction.objects.create(
        paying_user=paying_user, receiving_user=payment_data.get("selected_user")
    )
    # Calculating receiving side
    # 1. Getting receiving user wallet
    receiving_user_wallet = UserWallet.objects.filter(
        wallet_user=payment_data.get("selected_user")
    )[0]
    # 2. Adding transaction amount to wallet
    receiving_user_wallet.wallet_amount = (
        receiving_user_wallet.wallet_amount + transaction_amount
    )

    # 3. Deducting receiving transaction charges
    # 3.1 from paying user
    paying_user_wallet.wallet_amount = paying_user_wallet.wallet_amount - total_amount
    superuser_wallet.wallet_amount += payment_charge_amount
    paying_user_wallet.save()
    # 3.2 from receiving user
    receiving_user_wallet.wallet_amount = (
        receiving_user_wallet.wallet_amount - receiving_charge_amount
    )
    superuser_wallet.wallet_amount += receiving_charge_amount
    receiving_user_wallet.save()
    superuser_wallet.save()

    # making payment.

    payment_debit_transaction = make_transaction(
        transaction_id=transaction_id,
        transaction_amount=transaction_amount,
        transaction_method="debit",
        transaction_user=paying_user,
        receiving_user=receiving_user,
    )
    payment_debit_charges_transaction = make_transaction(
        transaction_id=transaction_id,
        transaction_amount=payment_charge_amount,
        transaction_method="debit",
        transaction_user=paying_user,
        receiving_user=superuser,
    )

    receiver_credit_transaction = make_transaction(
        transaction_id=transaction_id,
        transaction_amount=transaction_amount,
        transaction_method="credit",
        transaction_user=paying_user,
        receiving_user=payment_data.get("selected_user"),
    )

    receiver_charges_transaction = make_transaction(
        transaction_id=transaction_id,
        transaction_amount=payment_charge_amount,
        transaction_method="credit",
        transaction_user=payment_data.get("selected_user"),
        receiving_user=superuser,
    )

    return


@login_required(login_url="login")
def request_payment(request, payment_data):
    payment_request = PaymentRequest.objects.create(
        requesting_user=request.user,
        paying_user=payment_data.get("selected_user"),
        request_amount=payment_data.get("transaction_amount"),
    )
    return


@login_required(login_url="login")
def pay_or_receive(request):
    print("pay or receive page")
    form = TransactionRequestForm(request.POST or None)
    if request.method == "POST":
        print("POST Method - ")
        if form.is_valid():
            payment_data = {
                "selected_user": form.cleaned_data["user"],
                "transaction_amount": form.cleaned_data["transaction_amount"],
            }
            payment_type = form.cleaned_data["make_payment_or_request_payment"]
            if payment_type == "make_payment":
                make_payment(request, payment_data)
                return redirect("homepage")
            if payment_type == "request_payment":
                request_payment(request, payment_data)
                return redirect("homepage")
        else:
            context = {"form": form}
            return render(request, "wallet/pay-or-receive.html", context)

    context = {"form": form}
    return render(request, "wallet/pay-or-receive.html", context)


def approve_payment(request, id):
    payment_request = PaymentRequest.objects.get(pk=id)
    payment_data = {
        "selected_user": payment_request.requesting_user,
        "transaction_amount": payment_request.request_amount,
    }
    make_payment(request, payment_data)
    payment_request.is_completed = True
    payment_request.save()
    return redirect("homepage")


def reject_payment(request, id):
    payment_request = PaymentRequest.objects.get(pk=id)
    payment_request.is_completed = True
    payment_request.save()
    return redirect("homepage")


def payment_requests(request):
    if request.user.is_authenticated:
        received_requests = PaymentRequest.objects.filter(
            paying_user=request.user, is_completed=False
        )
        for user_request in received_requests:
            print(f"{user_request.requesting_user} - {user_request.request_amount}")
        created_requests = PaymentRequest.objects.filter(
            requesting_user=request.user, is_completed=False
        )
        context = {
            "received_requests": received_requests,
            "created_requests": created_requests,
        }
        return render(request, "wallet/payment_requests.html", context)


@login_required(login_url="login")
def view_transactions(request):
    if request.user.is_authenticated:
        transactions = WalletTransactions.objects.filter(transaction_user=request.user)
    context = {"transactions": transactions}
    return render(request, "wallet/transactions.html", context)
