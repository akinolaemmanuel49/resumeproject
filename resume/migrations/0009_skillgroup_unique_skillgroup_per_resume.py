# Generated by Django 5.1.6 on 2025-02-15 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0008_alter_skill_skill_group'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='skillgroup',
            constraint=models.UniqueConstraint(fields=('name', 'resume'), name='unique_skillgroup_per_resume'),
        ),
    ]
