# Generated by Django 4.2.4 on 2023-08-31 18:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=8, verbose_name='Token')),
                ('token_expires', models.DateTimeField(default=datetime.datetime(2023, 8, 31, 18, 51, 24, 628351, tzinfo=datetime.timezone.utc), verbose_name='Token Expires')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
