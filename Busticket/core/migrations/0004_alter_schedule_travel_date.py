# Generated by Django 5.2 on 2025-05-08 12:15

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='travel_date',
            field=models.DateField(verbose_name=builtins.format),
        ),
    ]
