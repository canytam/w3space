# Generated by Django 4.2 on 2023-05-01 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_cleanup'),
    ]

    operations = [
        migrations.RenameField(
            model_name='package',
            old_name='coupon',
            new_name='credits',
        ),
        migrations.RenameField(
            model_name='packagedetails',
            old_name='coupon',
            new_name='credits',
        ),
        migrations.RenameField(
            model_name='space',
            old_name='coupon',
            new_name='credits',
        ),
    ]