# Generated by Django 4.1.3 on 2022-12-04 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financials', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]