# Generated by Django 4.2.4 on 2023-08-31 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0003_workhistory_job_description'),
    ]

    operations = [
        migrations.DeleteModel(
            name='JobDescription',
        ),
    ]