# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-06 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osparc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='activationDate',
            field=models.DateField(),
        ),
    ]
