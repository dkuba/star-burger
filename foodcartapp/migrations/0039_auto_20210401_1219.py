# Generated by Django 3.0.7 on 2021-04-01 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_auto_20210323_1829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='last_name',
            new_name='lastname',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='phone_number',
            new_name='phonenumber',
        ),
        migrations.RenameField(
            model_name='orderproducts',
            old_name='amount',
            new_name='quantity',
        ),
    ]