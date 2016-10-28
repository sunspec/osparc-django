# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 20:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('osparc', '0003_auto_20161027_1957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportkpi',
            name='reportrun',
        ),
        migrations.AddField(
            model_name='kpi',
            name='reportrun',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='osparc.ReportRun'),
        ),
        migrations.DeleteModel(
            name='ReportKPI',
        ),
    ]
