# Generated by Django 4.2.5 on 2023-09-21 23:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_groups_user_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
