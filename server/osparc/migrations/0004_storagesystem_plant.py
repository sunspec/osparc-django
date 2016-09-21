# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osparc', '0003_storagesystem'),
    ]

    operations = [
        migrations.AddField(
            model_name='storagesystem',
            name='plant',
            field=models.ForeignKey(to='osparc.Plant', null=True),
        ),
    ]
