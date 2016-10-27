#!/usr/bin/python

# run periodically to create custom reports.
# reads reportrun table and if records are found in the pending state, 
# runs the report and updates the table with results and status.
# Sets status to processing when it starts, ready when it finishes.

import MySQLdb
import datetime
import time
from kpis import KPIs
from dbwrapper import DbWrapper

url = 'http://localhost:8001/api/reports'

try:
	dbwrapper = DbWrapper()

	runs = DbWrapper.readRun(dbwrapper)

	print( "retrieved %d rows from osparc_reportruns" % (len(runs)))

	for run in runs:

		print run

		status = run[1]
		print "status=%d" % (status)
		if status == 2:		# pending

			# let the system know we're working on this run
			id = run[0]
			now = datetime.datetime.now()
			DbWrapper.updateRun(dbwrapper,id,now,5)

			defId = run[11]
			print "defId=%d" % (defId)

			try:
				defi = DbWrapper.readDef(dbwrapper,defId)

				startTime = datetime.datetime.combine(defi[2],datetime.time.min)
				endTime = datetime.datetime.combine(defi[3],datetime.time.max)
				timeWhere = "where timestamp between '%s' and '%s'" % (startTime,endTime)

				attr = defi[4]
				op = defi[5]
				value = defi[6]
				plantWhere = "where '%s' %s '%s'" % (attr,op,value)

				kpis = KPIs()

				KPIs.calculateKPIs(kpis,plantWhere,timeWhere)

				time.sleep(1)

			except:
				print "ERROR processing defs"



except:
	print "ERROR getting runs"

 


