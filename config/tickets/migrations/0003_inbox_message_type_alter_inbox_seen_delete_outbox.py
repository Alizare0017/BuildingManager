# Generated by Django 4.1.3 on 2022-11-29 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_remove_inbox_msg_type_inbox_to_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inbox',
            name='message_type',
            field=models.CharField(choices=[('IN', 'inbox'), ('OUT', 'outbox')], default='IN', max_length=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inbox',
            name='seen',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.DeleteModel(
            name='OutBox',
        ),
    ]
