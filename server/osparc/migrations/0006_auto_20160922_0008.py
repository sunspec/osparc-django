# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osparc', '0005_auto_20160921_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='ACCapacity',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='plant',
            name='DCOptimized',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='plant',
            name='DCRating',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='plant',
            name='city',
            field=models.CharField(default=b'', max_length=32),
        ),
        migrations.AddField(
            model_name='plant',
            name='county',
            field=models.CharField(default=b'', max_length=32),
        ),
        migrations.AddField(
            model_name='plant',
            name='degradationRate',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='plant',
            name='derate',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='plant',
            name='designModel',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='plant',
            name='inverterType',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='plant',
            name='latitude',
            field=models.CharField(default=b'none', max_length=16),
        ),
        migrations.AddField(
            model_name='plant',
            name='longitude',
            field=models.CharField(default=b'none', max_length=16),
        ),
        migrations.AddField(
            model_name='plant',
            name='nominalACPowerRating',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='plant',
            name='postalCode',
            field=models.CharField(default=b'', max_length=6),
        ),
        migrations.AddField(
            model_name='plant',
            name='state',
            field=models.CharField(default=b'', max_length=2),
        ),
        migrations.AddField(
            model_name='plant',
            name='timeZone',
            field=models.CharField(default=b'none', max_length=64),
        ),
        migrations.AddField(
            model_name='plant',
            name='weatherSource',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='plant',
            name='name',
            field=models.CharField(max_length=45, null=True, blank=True),
        ),
    ]
