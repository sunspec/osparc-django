# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osparc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='type',
            field=models.ForeignKey(to='osparc.PlantType', null=True),
        ),
    ]
