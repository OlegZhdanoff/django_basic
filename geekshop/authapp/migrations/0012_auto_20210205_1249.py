# Generated by Django 2.2.17 on 2021-02-05 07:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0011_auto_20210123_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 7, 7, 49, 58, 606324, tzinfo=utc)),
        ),
    ]
