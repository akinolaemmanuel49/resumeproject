# Generated by Django 5.1.6 on 2025-02-15 17:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_alter_token_token_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token_expires',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 15, 17, 54, 16, 611536, tzinfo=datetime.timezone.utc), verbose_name='Token Expires'),
        ),
    ]
