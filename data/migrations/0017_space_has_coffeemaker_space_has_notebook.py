# Generated by Django 4.2 on 2023-05-04 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0016_alter_packagedetails_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='has_coffeemaker',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='space',
            name='has_notebook',
            field=models.BooleanField(default=False),
        ),
    ]
