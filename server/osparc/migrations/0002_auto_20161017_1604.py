# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-17 16:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('osparc', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plant',
            old_name='accountID',
            new_name='accountid',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='activationDate',
            new_name='activationdate',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='DCRating',
            new_name='dcrating',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='plantUUID',
            new_name='plantuuid',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='postalCode',
            new_name='postalcode',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='recordStatus',
            new_name='recordstatus',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='solarAnywhereSite',
            new_name='solaranywheresite',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='storageCurrentCapacity',
            new_name='storagecurrentcapacity',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='storageOriginalCapacity',
            new_name='storageoriginalcapacity',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='storageStateOfCharge',
            new_name='storagestateofcharge',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='timeZone',
            new_name='timezone',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='trackerType',
            new_name='trackertype',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='versionCreationTime',
            new_name='versioncreationtime',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='versionID',
            new_name='versionid',
        ),
        migrations.RenameField(
            model_name='plant',
            old_name='weatherSource',
            new_name='weathersource',
        ),
    ]
