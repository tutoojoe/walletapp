# Generated by Django 4.2 on 2023-04-23 08:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wallet", "0005_wallettransactions_remarks"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="transactioncharges",
            options={
                "verbose_name": "TransactionCharge",
                "verbose_name_plural": "TransactionCharges",
            },
        ),
        migrations.CreateModel(
            name="PaymentRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "request_amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("is_completed", models.BooleanField(default=False)),
                ("request_creation_date", models.DateTimeField(auto_now_add=True)),
                ("request_completed_date", models.DateTimeField(auto_now=True)),
                (
                    "paying_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="paying_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "requesting_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment_requesting_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
