# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osparc', '0004_storagesystem_plant'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storagesystem',
            old_name='origCapacity',
            new_name='originalCapacity',
        ),
    ]
