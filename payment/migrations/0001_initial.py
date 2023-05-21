# Generated by Django 4.1.6 on 2023-02-24 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("product", "0002_alter_product_options_product_product_image2_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BillingAddress",
            fields=[
                (
                    "bill_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("full_name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("address", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=50)),
                ("state", models.CharField(max_length=50)),
                ("zip_code", models.CharField(max_length=50)),
            ],
            options={"verbose_name_plural": "Billing Address",},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "order_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("ordered_date", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(default="Pending", max_length=50)),
                (
                    "billing_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="payment.billingaddress",
                    ),
                ),
            ],
            options={"verbose_name_plural": "Order",},
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "payment_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("payment_method", models.CharField(max_length=50)),
                ("card_number", models.CharField(max_length=50)),
                ("exp_month", models.CharField(max_length=50)),
                ("exp_year", models.CharField(max_length=50)),
                ("cvv", models.CharField(max_length=50)),
                (
                    "billing_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="payment.billingaddress",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name_plural": "Payment",},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "order_item_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("quantity", models.IntegerField()),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="payment.order"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.product",
                    ),
                ),
            ],
            options={"verbose_name_plural": "Order Item",},
        ),
        migrations.AddField(
            model_name="order",
            name="payment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="payment.payment"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="product.product"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]