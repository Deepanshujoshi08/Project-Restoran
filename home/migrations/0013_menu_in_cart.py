# Generated by Django 4.2 on 2023-06-29 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_cart_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='in_cart',
            field=models.BooleanField(default=False),
        ),
    ]
