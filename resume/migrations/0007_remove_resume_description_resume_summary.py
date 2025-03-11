# Generated by Django 5.1.6 on 2025-02-12 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0006_remove_skill_level_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resume',
            name='description',
        ),
        migrations.AddField(
            model_name='resume',
            name='summary',
            field=models.TextField(blank=True, null=True, verbose_name='Summary'),
        ),
    ]
