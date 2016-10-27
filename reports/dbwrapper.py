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
			query = "update osparc_reportrun set status=%d,runstarttime='%s' where id=%d" % (status,time,id)
			cursor.execute(query)
			db.commit()
			db.close()
		except:
			print "ERROR updating runs"

	def readDef(self,defId):
		try:
			runquery = "select * from osparc_reportdefinition where id=%d" % (defId)
			print runquery
			db = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","osparc")
			cursor = db.cursor()
			cursor.execute(runquery)
			defi = cursor.fetchone()
			print defi[0],defi[1],defi[2],defi[3],defi[4],defi[5],defi[6]
			db.close
			return defi
		except:
			print "ERROR reading defs"


