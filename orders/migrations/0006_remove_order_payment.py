# Generated by Django 5.0.6 on 2024-07-30 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_orderproduct_payment_confirm_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
    ]
