# Generated by Django 4.1.3 on 2022-12-06 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0004_unitspecification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitspecification',
            name='features',
            field=models.TextField(help_text='in a comma-seperated format', null=True),
        ),
    ]
