# Generated by Django 4.2 on 2023-04-19 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_remove_customer_coupon'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Room',
            new_name='Space',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='room',
            new_name='space',
        ),
    ]