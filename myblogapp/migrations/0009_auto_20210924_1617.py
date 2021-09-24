# Generated by Django 2.2.24 on 2021-09-24 08:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myblogapp', '0008_auto_20210909_0715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 24, 8, 17, 49, 897245, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 24, 8, 17, 49, 896841, tzinfo=utc)),
        ),
    ]
