# -*- coding: utf-8 -*-
# Created by dbergh 2016-10-17
# 
# 
# 
# 
# 
# 
# 
# 
#      THIS DOES NOT WORK
# 
# 
# 
# 
# 
# 
# 
# The view must be created manually if it is ever dropped!
# 
# You must run the initial migration, to create the database and tables from which the view is 
# defined, prior to creating the view.
# 
# 
from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    initial = False

    dependencies = [
        ('osparc', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("drop view if exists osparc_total;"),
        migrations.RunSQL("create view osparc_total as select SUM(dcrating) totaldcrating,SUM(storagecapacity) totalstoragecapacity from osparc_plant;")
    ]
