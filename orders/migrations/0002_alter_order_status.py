# Generated by Django 5.1.6 on 2025-02-14 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('A', 'Awaiting payment'), ('p', 'Paid'), ('X', 'Cancelled'), ('D', 'Delivered'), ('S', 'Shipped')], default='A', max_length=1),
        ),
    ]
