# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, null=True, blank=True)),
                ('description', models.CharField(max_length=254, null=True, blank=True)),
                ('activationDate', models.DateField(auto_now_add=True)),
                ('postalCode', models.CharField(default=b'', max_length=6)),
                ('state', models.CharField(default=b'', max_length=2)),
                ('county', models.CharField(default=b'', max_length=32)),
                ('city', models.CharField(default=b'', max_length=32)),
                ('latitude', models.CharField(default=b'none', max_length=16)),
                ('longitude', models.CharField(default=b'none', max_length=16)),
                ('timeZone', models.CharField(default=b'none', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='PlantType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45)),
                ('description', models.CharField(max_length=254, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PVArray',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, null=True, blank=True)),
                ('description', models.CharField(max_length=254, null=True, blank=True)),
                ('arrayId', models.IntegerField()),
                ('trackerType', models.CharField(max_length=32)),
                ('tilt', models.IntegerField()),
                ('azimuth', models.IntegerField()),
                ('plant', models.ForeignKey(to='osparc.Plant', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StorageSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=254, null=True, blank=True)),
                ('activationDate', models.DateField(auto_now_add=True)),
                ('originalCapacity', models.IntegerField(null=True, blank=True)),
                ('currentCapacity', models.IntegerField(null=True, blank=True)),
                ('stateOfCharge', models.FloatField(null=True, blank=True)),
                ('plant', models.ForeignKey(to='osparc.Plant', null=True)),
            ],
        ),
    ]
