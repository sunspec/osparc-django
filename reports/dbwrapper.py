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

	def updateRun(self,id,time,status):
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
			print "ERROR updating runs"

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
				query = "select id,dcrating,storageoriginalcapacity,storagecurrentcapacity from osparc_plant where %s %s %s" % (attr,op,value)
			else:
				query = "select id,dcrating,storageoriginalcapacity,storagecurrentcapacity from osparc_plant"
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






