# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 21:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('osparc', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadactivity',
            old_name='mostrecentuploadtime',
            new_name='mostrecenttimeseriesuploadtime',
        ),
        migrations.RenameField(
            model_name='uploadactivity',
            old_name='firstuploadtime',
            new_name='plantuploadtime',
        ),
        migrations.RemoveField(
            model_name='uploadactivity',
            name='plant',
        ),
        migrations.AddField(
            model_name='plant',
            name='uploadactivity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='osparc.UploadActivity'),
        ),
    ]
