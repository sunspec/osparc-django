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

	# get the reportruns. Those with status==pending will be processed.
	runs = DbWrapper.readRun(dbwrapper)

	print( "retrieved %d rows from osparc_reportruns" % (len(runs)))

	for run in runs:

		# determine whether to process this reportrun - do so if its status is pending
		status = run[1]
		if status == 2:		# pending

			# let the system know we're working on this run
			id = run[0]
			now = datetime.datetime.now()
			DbWrapper.updateRun(dbwrapper,id,now,5)

			# get the definition, which contans the plant filters
			defId = run[11]
			defi = DbWrapper.readDef(dbwrapper,defId)

			# use the plant filter from definition to get the set of plants
			# participating in the report
			attr = defi[4]
			op = defi[5]
			value = defi[6]
			plants = DbWrapper.getPlants(dbwrapper,attr,op,value)

			# use the time filter from the reportrun, and the set of plants 
			# retrieved above, to get the set of timeseries elements to be used
			# to calculate the kpis for the report
			startTime = datetime.datetime.combine(defi[2],datetime.time.min)
			endTime = datetime.datetime.combine(defi[3],datetime.time.max)
			timeseries = DbWrapper.getTimeSeries(dbwrapper,plants,startTime,endTime)

			# ...and away we go
			kpiObj = KPIs()
			kpis = KPIs.calculateKPIs(kpiObj,plants,timeseries)

			# save the KPIs for retrieval by the services
			DbWrapper.saveKpi(dbwrapper,id,kpis['DCRating'])
			DbWrapper.saveKpi(dbwrapper,id,kpis['MonthlyInsolation'])
			DbWrapper.saveKpi(dbwrapper,id,kpis['MonthlyGeneratedEnergy'])
			DbWrapper.saveKpi(dbwrapper,id,kpis['MonthlyYield'])
			DbWrapper.saveKpi(dbwrapper,id,kpis['PerformanceRatio'])


			# indicate that this reportrun is ready to be viewed
			now = datetime.datetime.now()
			DbWrapper.updateRun(dbwrapper,id,now,1)

			time.sleep(1)

except:
	print "ERROR processing runs"

 


