# Generated by Django 4.2 on 2023-04-19 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_rename_rank_package_price_remove_room_rank'),
    ]

    operations = [
        migrations.RenameField(
            model_name='packagedetails',
            old_name='copuon',
            new_name='coupon',
        ),
    ]