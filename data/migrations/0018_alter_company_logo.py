# Generated by Django 4.2 on 2023-05-04 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0017_space_has_coffeemaker_space_has_notebook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(upload_to='media/images/'),
        ),
    ]