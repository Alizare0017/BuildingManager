# Generated by Django 4.1.3 on 2022-11-28 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='used',
            field=models.BooleanField(default=False),
        ),
    ]
