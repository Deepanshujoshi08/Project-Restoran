# Generated by Django 4.2 on 2023-07-02 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0003_alter_cart_items_item'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cart_items',
            unique_together=set(),
        ),
    ]
