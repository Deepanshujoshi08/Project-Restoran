# Generated by Django 4.2 on 2023-06-28 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_orders_delete_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
                ('quantity', models.IntegerField()),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.menu')),
            ],
        ),
        migrations.DeleteModel(
            name='Orders',
        ),
    ]
