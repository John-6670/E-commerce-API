# Generated by Django 5.1.6 on 2025-02-14 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShippingAddress',
        ),
    ]
