from .views import (
    view_transactions,
    homepage,
    pay_or_receive,
    approve_payment,
    reject_payment,
    payment_requests,
)
from django.urls import path

urlpatterns = [
    path("", homepage, name="homepage"),
    path("payment_requests", payment_requests, name="payment_requests"),
    path("transactions/", view_transactions, name="view_transactions"),
    path("pay_or_receive/", pay_or_receive, name="pay_or_receive"),
    path("approve_request/<int:id>/", approve_payment, name="approve_request"),
    path("reject_request/<int:id>/", reject_payment, name="reject_request"),
]
