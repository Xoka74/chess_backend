# Generated by Django 4.2.5 on 2023-09-21 22:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_game_start_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 21, 22, 30, 0, 489587, tzinfo=datetime.timezone.utc)),
        ),
    ]
