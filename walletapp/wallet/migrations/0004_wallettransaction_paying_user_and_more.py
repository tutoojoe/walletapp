# Generated by Django 4.2 on 2023-04-23 04:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wallet", "0003_transactioncharges_alter_wallettransaction_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="wallettransaction",
            name="paying_user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="paid_transactions",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="wallettransaction",
            name="receiving_user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="collected_transactions",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="wallettransactions",
            name="receiving_user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="received_transactions",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
