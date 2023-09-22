# Generated by Django 4.2.5 on 2023-09-21 22:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_winner', models.BooleanField(default=False)),
                ('remaining_time_milliseconds', models.BigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(default=datetime.datetime(2023, 9, 21, 22, 21, 14, 630067, tzinfo=datetime.timezone.utc))),
                ('end_datetime', models.DateTimeField(null=True)),
                ('board', models.CharField(default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', max_length=100)),
                ('status', models.IntegerField(choices=[(0, 'Started'), (1, 'Check'), (2, 'Checkmate'), (3, 'Stalemate'), (4, 'Surrender'), (5, 'Out Of Time')], default=0)),
                ('black', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_2', to='api.gamemember')),
                ('white', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_1', to='api.gamemember')),
            ],
        ),
    ]
