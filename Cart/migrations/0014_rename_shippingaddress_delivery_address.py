# Generated by Django 4.2 on 2023-07-10 14:43

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Cart', '0013_order_order_option'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShippingAddress',
            new_name='Delivery_address',
        ),
    ]
