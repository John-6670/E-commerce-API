# Generated by Django 5.1.6 on 2025-02-12 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_address_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_seller',
        ),
    ]
