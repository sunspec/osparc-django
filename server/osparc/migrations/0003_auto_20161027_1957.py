# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osparc', '0002_auto_20161027_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportrun',
            name='runcompletetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]