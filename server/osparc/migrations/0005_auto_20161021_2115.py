# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osparc', '0004_auto_20161021_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plantdetails',
            name='storageoriginalcapacity',
        ),
        migrations.AddField(
            model_name='plant',
            name='storageoriginalcapacity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
