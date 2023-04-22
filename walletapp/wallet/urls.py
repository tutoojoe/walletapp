from .views import homepage, pay_or_receive
from django.urls import path

urlpatterns = [
    path("", homepage, name="homepage"),
    path("pay_or_receive/", pay_or_receive, name="pay_or_receive"),
]
