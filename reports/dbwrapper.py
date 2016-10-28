#!/usr/bin/python

# manage the database tables

import MySQLdb


class DbWrapper(object):

	readPlantreportSql = "select * from osparc_plantreport"

	def readRun(self):
		try:
			db = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","osparc")
			cursor = db.cursor()
			cursor.execute("select * from osparc_reportrun")
			runs = cursor.fetchall()
			db.close()
			return runs
		except:
			print "ERROR reading runs"

	def updateRunStatus(self,id,time,status):
		try:
			db = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","osparc")
			cursor = db.cursor()
			if status == 5:	# changing to processing
				query = "update osparc_reportrun set status=%d,runstarttime='%s' where id=%d" % (status,time,id)
			elif status == 1: # changing to ready
				query = "update osparc_reportrun set status=%d,runcompletetime='%s' where id=%d" % (status,time,id)
			else:
				return
			cursor.execute(query)
			db.commit()
			db.close()
		except:
			print "ERROR updating runstatus"

	def updateRunSummary(self,id,summary):
		try:
			summary["numberofplants"] = len(plants)
			summary["numberofobservations"] = len(timeseries)
			summary["observationstartdate"] = KPIs.getEarliestDate(kpiObj,kpis)
			summary["observationenddate"] = KPIs.getLatestDate(kpiObj,kpis)
			db = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","osparc")
			cursor = db.cursor()
			query = "update osparc_reportrun set numberofplants=%d,\
					numberofobservations='%s',observationstartdate='%s',observationenddate='%s' \
					where id=%d" % \
					(summary["numberofplants"],summary["numberofobservations"],
					summary["observationstartdate"],summary["observationenddate"],id)
			cursor.execute(query)
			db.commit()
			db.close()
		except:
			print "ERROR updating runsummary"


	def readDef(self,defId):
		try:
			query = "select * from osparc_reportdefinition where id=%d" % (defId)
			db = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","osparc")
			cursor = db.cursor()
			cursor.execute(query)
			defi = cursor.fetchone()
			db.close
			return defi
		except:
			print "ERROR reading defs"

	def getPlants(self,attr,op,value):
		try:
			if attr != "":
				query = "select id,activationdate,dcrating,storageoriginalcapacity,storagecurrentcapacity from osparc_plant where %s %s %s" % (attr,op,value)
			else:
				query = "select id,activationdate,dcrating,storageoriginalcapacity,storagecurrentcapacity from osparc_plant"
			db = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","osparc")
			cursor = db.cursor()
			cursor.execute(query)
			plants = cursor.fetchall()
			db.close
			return plants
		except:
			print "ERROR getting plants"

	def getTimeSeries(self,plants,startTime,endTime):
		try:
			plantIds = list()
			for plant in plants:
				plantIds.append(str(plant[0]))
			plantIdsStr = ','.join(plantIds)
			query = "select * from osparc_planttimeseries where plant_id in (%s) and timestamp between '%s' and '%s'" % (plantIdsStr,startTime,endTime)
			db = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","osparc")
			cursor = db.cursor()
			cursor.execute(query)
			results = cursor.fetchall()
			db.close
			return results
		except:
			print "ERROR getting timeseries"

	# save a kpi set associated with a reportrun
	def saveKpi(self,runId,kpi):
		try:
			# there must be only one (reportrun,kpi) tuple per reportrun and kpi (if one doesn't exist, query has no effect)
			query1 = "delete from osparc_kpi where name='%s' and reportrun_id=%d" % (kpi["name"],runId)
			query = "insert into osparc_kpi (name,plants,firstday,lastday,mean,median,minimum,maximum,reportrun_id) values \
('%s',%d,'%s','%s',%d,%d,%d,%d,%d)" % \
(kpi["name"],kpi["plants"],kpi["firstday"],kpi["lastday"],kpi["mean"],kpi["median"],kpi["minimum"],kpi["maximum"],runId)
			db = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","osparc")
			cursor = db.cursor()
			cursor.execute(query1)
			cursor.execute(query)
			db.commit()
			db.close()
		except:
			print "ERROR saving kpis"






