# Generated by Django 4.2.4 on 2023-08-19 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0003_resume_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
    ]