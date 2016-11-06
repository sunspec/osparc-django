#!/usr/bin/python

# run periodically to create custom reports.
# reads reportrun table and if records are found in the pending state, 
# runs the report and updates the table with results and status.
# Sets status to processing when it starts, ready when it finishes.

import datetime
import time
import collections
from kpis import KPIs
from dbwrapper import DbWrapper

try:
	dbwrapper = DbWrapper()

	# get the reportruns. Those with status==pending will be processed.
	runs = DbWrapper.readRun(dbwrapper)

	print( "retrieved %d rows from osparc_reportruns" % (len(runs)))

	for run in runs:

		# determine whether to process this reportrun - do so if its status is pending
		status = run[1]
		if status == 2:		# pending

			try:
				runid = run[0]
				now = datetime.datetime.now()

				print("starting report %d at %s" % (runid,now))

				# let the system know we're working on this run
				DbWrapper.updateRunStatus(dbwrapper,runid,now,5)

				# get the definition, which contans the plant filters
				defId = run[11]
				defi = DbWrapper.readDef(dbwrapper,defId)

				# use the plant filter from definition to get the set of plants
				# participating in the report
				attr = defi[4]
				op = defi[5]
				value = defi[6]
				plants = DbWrapper.getPlants(dbwrapper,attr,op,value)
				totaldccapacity = 0;
				totalstoragecapacity = 0;

				for plant in plants:
					if plant.dcrating is not None:
						totaldccapacity += plant.dcrating
					if plant.storageoriginalcapacity is not None:
						totalstoragecapacity += plant.storageoriginalcapacity

				# use the time filter from the reportrun, and the set of plants 
				# retrieved above, to get the set of timeseries elements to be used
				# to calculate the kpis for the report
				startTime = datetime.datetime.combine(defi[2],datetime.time.min)
				endTime = datetime.datetime.combine(defi[3],datetime.time.max)
				timeseries = DbWrapper.getTimeSeries(dbwrapper,plants,startTime,endTime)

				print "creating report with %d plants, %d timeseries elements" % (len(plants),len(timeseries))

				# The results are saved as a summary in the reportrun table, and a set of
				# kpis, in the kpi table. Kpi table entries have a foreign key to the reportrun table

				# calculate and save the KPIs
				kpiObj = KPIs()
				plantKpis = KPIs.calculatePlantKPIs(kpiObj,plants)
				if plantKpis != None:
					DbWrapper.saveKpi(dbwrapper,runid,plantKpis['DCRating'])
					DbWrapper.saveKpi(dbwrapper,runid,plantKpis['StorageCapacity'])
					DbWrapper.saveKpi(dbwrapper,runid,plantKpis['StorageStateOfHealth'])
				timeseriesKpis = kpiObj.calculateTimeseriesKPIs(plants,timeseries)
				if timeseriesKpis != None:
					DbWrapper.saveKpi(dbwrapper,runid,timeseriesKpis['MonthlyInsolation'])
					DbWrapper.saveKpi(dbwrapper,runid,timeseriesKpis['MonthlyGeneratedEnergy'])
					DbWrapper.saveKpi(dbwrapper,runid,timeseriesKpis['MonthlyYield'])
					DbWrapper.saveKpi(dbwrapper,runid,timeseriesKpis['PerformanceRatio'])

				# update the reportrun table with the summary of the run...
				summary = collections.defaultdict(int)
				summary["numberofplants"] = len(plants)
				summary['totaldccapacity'] = totaldccapacity
				summary["numberofmeasurements"] = len(timeseries)
				summary["firstmeasurementdate"] = defi[2]	# note: get this from timeseries instead!
				summary["lastmeasurementdate"] = defi[3]	# ditto
				summary['totalstoragecapacity'] = totalstoragecapacity
				DbWrapper.updateRunSummary(dbwrapper,runid,summary)

				# ...and the status, indicating that it's ready to be viewed
				now = datetime.datetime.now()
				DbWrapper.updateRunStatus(dbwrapper,runid,now,1)

				print("finished report %d at %s" % (runid,datetime.datetime.now()))
			except:
				print "ERROR processing run",runid


except Exception as e:
	print "ERROR processing runs:",e.message,"exception type ",type(e)
