# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 22:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osparc', '0006_reportdefinition_plantfilter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportdefinition',
            name='plantfilter',
        ),
        migrations.RemoveField(
            model_name='reportdefinition',
            name='plantlatestactivationdate',
        ),
        migrations.RemoveField(
            model_name='reportdefinition',
            name='plantmaxsize',
        ),
        migrations.RemoveField(
            model_name='reportdefinition',
            name='plantminsize',
        ),
        migrations.RemoveField(
            model_name='reportdefinition',
            name='plantpostalcode',
        ),
        migrations.RemoveField(
            model_name='reportdefinition',
            name='plantstate',
        ),
        migrations.AddField(
            model_name='reportdefinition',
            name='plantfilterattribute',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='reportdefinition',
            name='plantfilteroperation',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='reportdefinition',
            name='plantfiltervalue',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]