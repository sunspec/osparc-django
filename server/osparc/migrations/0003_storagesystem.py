# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osparc', '0002_plant_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=254, null=True, blank=True)),
                ('activationDate', models.DateField(auto_now_add=True)),
                ('origCapacity', models.IntegerField(null=True, blank=True)),
                ('currentCapacity', models.IntegerField(null=True, blank=True)),
                ('stateOfCharge', models.FloatField(null=True, blank=True)),
            ],
        ),
    ]
