# Generated by Django 2.2.24 on 2021-09-04 00:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myblogapp', '0003_remove_blogpost_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 4, 0, 55, 43, 668245, tzinfo=utc)),
        ),
    ]
