# Generated by Django 4.2.6 on 2023-10-13 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.IntegerField(null=True),
        ),
    ]
