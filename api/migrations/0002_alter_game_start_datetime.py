# Generated by Django 4.2.5 on 2023-09-21 22:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 21, 22, 29, 11, 16119, tzinfo=datetime.timezone.utc)),
        ),
    ]