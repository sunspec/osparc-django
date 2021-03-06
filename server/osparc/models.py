from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class Account(models.Model):
    accountID = models.CharField(max_length=250)
    role = models.CharField(max_length=16,blank=True,null=True)
    name = models.CharField(max_length=50,blank=True,null=True)
    companyName = models.CharField(max_length=50,blank=True,null=True)
    companyAddress = models.CharField(max_length=50,blank=True,null=True)
    companyCityState = models.CharField(max_length=50,blank=True,null=True)
    companyPostalCode = models.CharField(max_length=10,blank=True,null=True)
    email = models.CharField(max_length=50,blank=True,null=True)
    password = models.CharField(max_length=250)
    versionCreationTime = models.DateTimeField(auto_now_add=True)
    recordStatus = models.IntegerField(default=1)
    versionID = models.IntegerField(default=1)
    def __str__(self):
        return self.name

    # participantTypeID all 0
    # GeneratedPassword all NULL
    # GeneratedPasswordTime all NULL

class PlantType(models.Model):
    name = models.CharField(unique=True, max_length=45)
    description = models.CharField(max_length=254, blank=True, null=True)
    def __str__(self):
        return self.name

class UploadActivity(models.Model):
    plantuploadtime = models.DateTimeField(auto_now_add=True)
    mostrecenttimeseriesuploadtime = models.DateTimeField(blank=True,null=True)
    # plantUUID = models.CharField(max_length=254,blank=True,null=True)
    status = models.CharField(max_length=16)
    errorDetail = models.CharField(max_length=1024,blank=True,null=True)
    # s3Key = models.CharField(max_length=254,blank=True,null=True)
    # account = models.ForeignKey(Account,blank=True,null=True)

# Production Statistics pertaining to a single plant over a specific period (often its lifetime)
# Used in the construction of instances of ReportRuns
class PlantReport(models.Model):
    recordstatus = models.IntegerField(default=9)           # RECORD_STATUS_RECALCULATE
    createtime = models.DateTimeField(auto_now_add=True)    # time the report was created
    sampleinterval = models.CharField(max_length=64,blank=True,null=True)
    firstmeasurementdate = models.DateField(blank=True,null=True)
    lastmeasurementdate = models.DateField(blank=True,null=True)
    monthlyyield = models.FloatField(blank=True,null=True)    # production yield kWh/kWdc
    # yr = models.FloatField(blank=True,null=True)    # insolation yield kWh/m2/1000
    performanceratio = models.FloatField(blank=True,null=True)    # performance ratio yf/yr
    storagestateofhealth = models.FloatField(blank=True,null=True)   # storage state of health

class Plant(models.Model):
    uuid = models.CharField(max_length=254,blank=True,null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    activationdate = models.DateField()
    state = models.CharField(max_length=2,blank=True, null=True)
    postalcode = models.CharField(max_length=6,blank=True, null=True)
    dcrating = models.FloatField(blank=True, null=True)     # watts (NOT kilo-watts)
    storageoriginalcapacity = models.FloatField(blank=True,null=True)
    description = models.CharField(max_length=254, blank=True, null=True)
    county = models.CharField(max_length=32,blank=True, null=True)
    city = models.CharField(max_length=32,blank=True, null=True)
    latitude = models.CharField(max_length=16,default='none')
    longitude = models.CharField(max_length=16,default='none')
    timezone = models.CharField(max_length=64,default='none')
    weathersource = models.CharField(max_length=32, blank=True, null=True) # CPR or local
    derate = models.FloatField(blank=True, null=True)
    plantreport = models.ForeignKey(PlantReport,on_delete=models.CASCADE,blank=True, null=True)
    # from PVArray
    arraytype = models.CharField(max_length=32,blank=True, null=True)
    tilt = models.IntegerField(blank=True, null=True)
    azimuth = models.IntegerField(blank=True, null=True)
    # from StorageSystem
    storagecurrentcapacity  = models.FloatField(blank=True,null=True)
    storagestateofcharge = models.FloatField(blank=True,null=True)
    # plant-meta-meta data
    uploadactivity = models.ForeignKey(UploadActivity,on_delete=models.CASCADE,blank=True,null=True)
    accountid = models.CharField(max_length=250)
    recordstatus = models.IntegerField(default=1)
    versioncreationtime = models.DateTimeField(auto_now_add=True)
    versionid = models.IntegerField(default=1)
    solaranywheresite = models.CharField(max_length=64,blank=True,null=True)
    def __str__(self):
        return self.name

"""
current oSPARC - reason not carried forward shown in right column
    # DCOptimized = models.CharField(max_length=32, blank=True, null=True) all NULL
    # inverterType = models.CharField(max_length=32, blank=True, null=True) all NULL
    # designModel = models.CharField(max_length=32, blank=True, null=True) all NULL
    # nominalACPowerRating = models.FloatField(blank=True, null=True) all NULL
    # ACCapacity = models.FloatField(blank=True, null=True) all NULL
    # degradationRate = models.FloatField(blank=True, null=True) all NULL
"""

# class PVArray(models.Model):  INCORPORATED IN PLANT
#     name = models.CharField(max_length=250, blank=True, null=True)
#     description = models.CharField(max_length=254, blank=True, null=True)
#     plant = models.ForeignKey(Plant)
#     arrayId = models.IntegerField()
#     def __str__(self):
#         return self.name
    

# class StorageSystem(models.Model): INCORPORATED IN Plant
#     name = models.CharField(max_length=45)
#     description = models.CharField(max_length=254, blank=True, null=True)
#     plant = models.ForeignKey(Plant,null=True)
#     activationDate = models.DateField(auto_now_add=True)
#     originalCapacity = models.IntegerField(blank=True,null=True)
#     currentCapacity  = models.IntegerField(blank=True,null=True)
#     stateOfCharge = models.FloatField(blank=True,null=True)
#     def __str__(self):
#         return self.name

class PlantTimeSeries(models.Model):
    timestamp = models.DateTimeField()
    sampleinterval = models.IntegerField()
    WH_DIFF = models.FloatField()           # kWh since last entry
    GHI_DIFF = models.FloatField()
    TMPAMB_AVG = models.FloatField(blank=True,null=True)
    # from PVArrayTimeSeries
    HPOA_DIFF = models.FloatField(blank=True,null=True)
    # plantTimeSeries-meta-meta data
    plant = models.ForeignKey(Plant,on_delete=models.CASCADE,blank=True,null=True)
    recordstatus = models.IntegerField(default=1) # RECORD_STATUS_ACTIVE
    plantUUID = models.CharField(max_length=254,blank=True,null=True)

class Total(models.Model):
    dcrating = models.FloatField(blank=True, null=True)
    storageoriginalcapacity = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'osparc_total'


#  =========   REPORTS   ===========

# Custom Query Report definition
# The database query used to generate the result is built on the fly from this definition
class ReportDefinition(models.Model):
    name = models.CharField(max_length=254, blank=True, null=True)
    observationstartdate = models.DateField(blank=True,null=True)  # time plant observation started
    observationenddate = models.DateField(blank=True,null=True)  # time plant observation ended
    plantfilterattribute = models.CharField(max_length=254, blank=True, null=True)
    plantfilteroperation = models.CharField(max_length=254, blank=True, null=True)
    plantfiltervalue = models.CharField(max_length=254, blank=True, null=True)
    # plantpostalcode = models.CharField(max_length=6, blank=True, null=True)
    # plantstate = models.CharField(max_length=2, blank=True, null=True)
    # plantminsize = models.IntegerField(blank=True,null=True)
    # plantmaxsize = models.IntegerField(blank=True,null=True)
    # plantlatestactivationdate = models.DateField(blank=True,null=True) # youngest plant in query
    def __str__(self):
        return self.name


# The results of a run of a query
class ReportRun(models.Model):
    status = models.IntegerField(default=2) # 1=ready, 2=pending, 5=processing, 6=failed, 9=empty
    reportdefinition = models.ForeignKey(ReportDefinition)
    runsubmittime = models.DateTimeField(auto_now_add=True) # time user ordered the report
    runstarttime = models.DateTimeField(blank=True,null=True)  # time report preparation actually began
    runcompletetime = models.DateTimeField(blank=True,null=True)  # time report preparation actually completed
    firstmeasurementdate = models.DateField(blank=True,null=True)  # time plant observation started
    lastmeasurementdate = models.DateField(blank=True,null=True)  # time plant observation ended
    numberofmeasurements = models.IntegerField(blank=True,null=True)
    numberofplants = models.IntegerField(blank=True,null=True)
    totaldccapacity = models.FloatField(blank=True,null=True)
    totalstoragecapacity = models.FloatField(blank=True,null=True)


class KPI(models.Model):
    name = models.CharField(max_length=254, blank=True, null=True)
    reportrun = models.ForeignKey(ReportRun,blank=True,null=True)
    plants = models.IntegerField(blank=True, null=True)
    sampleinterval = models.CharField(max_length=64,default='monthly')
    firstday = models.DateField(blank=True, null=True)
    lastday = models.DateField(blank=True, null=True)
    mean = models.FloatField(blank=True, null=True)
    median = models.FloatField(blank=True, null=True)
    minimum = models.FloatField(blank=True, null=True)
    maximum = models.FloatField(blank=True, null=True)

# class KPI(models.Model):
#     dcratingplants = models.IntegerField(blank=True, null=True)
#     dcratingfirstday = models.DateField(blank=True, null=True)
#     dcratinglastday = models.DateField(blank=True, null=True)
#     dcratingmean = models.FloatField(blank=True, null=True)
#     dcratingmed = models.FloatField(blank=True, null=True)
#     dcratingmin = models.FloatField(blank=True, null=True)
#     dcratingmax = models.FloatField(blank=True, null=True)
#     insolplants = models.IntegerField(blank=True, null=True)
#     insolfirstday = models.DateField(blank=True, null=True)
#     insollastday = models.DateField(blank=True, null=True)
#     insolmean = models.FloatField(blank=True, null=True)
#     insolmed = models.FloatField(blank=True, null=True)
#     insolmin = models.FloatField(blank=True, null=True)
#     insolmax = models.FloatField(blank=True, null=True)
#     generatedplants = models.IntegerField(blank=True, null=True)
#     generatedfirstday = models.DateField(blank=True, null=True)
#     generatedlastday = models.DateField(blank=True, null=True)
#     generatedmean = models.FloatField(blank=True, null=True)
#     generatedmed = models.FloatField(blank=True, null=True)
#     generatedmin = models.FloatField(blank=True, null=True)
#     generatedmax = models.FloatField(blank=True, null=True)
#     yieldplants = models.IntegerField(blank=True, null=True)
#     yieldfirstday = models.DateField(blank=True, null=True)
#     yieldlastday = models.DateField(blank=True, null=True)
#     yieldmean = models.FloatField(blank=True, null=True)
#     yieldmed = models.FloatField(blank=True, null=True)
#     yieldmin = models.FloatField(blank=True, null=True)
#     yieldmax = models.FloatField(blank=True, null=True)
#     prplants = models.IntegerField(blank=True, null=True)
#     prfirstday = models.DateField(blank=True, null=True)
#     prlastday = models.DateField(blank=True, null=True)
#     prmean = models.FloatField(blank=True, null=True)
#     prmed = models.FloatField(blank=True, null=True)
#     prmin = models.FloatField(blank=True, null=True)
#     prmax = models.FloatField(blank=True, null=True)
#     storcapplants = models.IntegerField(blank=True, null=True)
#     storcapfirstday = models.DateField(blank=True, null=True)
#     storcaplastday = models.DateField(blank=True, null=True)
#     storcapmean = models.FloatField(blank=True, null=True)
#     storcapmed = models.FloatField(blank=True, null=True)
#     storcapmin = models.FloatField(blank=True, null=True)
#     storcapmax = models.FloatField(blank=True, null=True)
#     storsohplants = models.IntegerField(blank=True, null=True)
#     storsohfirstday = models.DateField(blank=True, null=True)
#     storsohlastday = models.DateField(blank=True, null=True)
#     storsohmean = models.FloatField(blank=True, null=True)
#     storsohmed = models.FloatField(blank=True, null=True)
#     storsohmin = models.FloatField(blank=True, null=True)
#     storsohmax = models.FloatField(blank=True, null=True)



# | WH_LAST           | float      | YES  |     | NULL    | all NULL
# | W_AVG             | float      | YES  |     | NULL    | all NULL
# | WNDSPD_AVG        | float      | YES  |     | NULL    | all NULL
# | PRES_AVG          | float      | YES  |     | NULL    | all NULL
# | RH_AVG            | float      | YES  |     | NULL    | all NULL
# | DCV_AVG           | float      | YES  |     | NULL    | all NULL
# | DCA_AVG           | float      | YES  |     | NULL    | all NULL
# | ACV_AVG           | float      | YES  |     | NULL    | all NULL
# | ACA_AVG           | float      | YES  |     | NULL    | all NULL
# | HZ_AVG            | float      | YES  |     | NULL    | all NULL
# | PF_AVG            | float      | YES  |     | NULL    | all NULL
# | WHL_LAST          | float      | YES  |     | NULL    | all NULL
# | WHL_DIFF          | float      | YES  |     | NULL    | all NULL
# | WHX_LAST          | float      | YES  |     | NULL    | all NULL
# | WHX_DIFF          | float      | YES  |     | NULL    | all NULL
# | WHI_LAST          | float      | YES  |     | NULL    | all NULL
# | WHI_DIFF          | float      | YES  |     | NULL    | all NULL
# | WHC_LAST          | float      | YES  |     | NULL    | all NULL
# | WHC_DIFF          | float      | YES  |     | NULL    | all NULL
# | WHD_LAST          | float      | YES  |     | NULL    | all NULL
# | WHD_DIFF          | float      | YES  |     | NULL    | all NULL
# | WHP_LAST          | float      | YES  |     | NULL    | all NULL
# | WHP_DIFF          | float      | YES  |     | NULL    | all NULL
# | StateOperating    | int(11)    | YES  |     | NULL    | all NULL
# | StateIslanded     | int(11)    | YES  |     | NULL    | all NULL
# | StateStandby      | int(11)    | YES  |     | NULL    | all NULL
# | StateEnv          | int(11)    | YES  |     | NULL    | all NULL
# | StateGrid         | int(11)    | YES  |     | NULL    | all NULL
# | StateShutdown     | int(11)    | YES  |     | NULL    | all NULL
# | StateForced       | int(11)    | YES  |     | NULL    | all NULL
# | StateEmergency    | int(11)    | YES  |     | NULL    | all NULL
# | NumInverterFaults | int(11)    | YES  |     | NULL    | all NULL
# | NumModuleFaults   | int(11)    | YES  |     | NULL    | all NULL
# | NumMeterFaults    | int(11)    | YES  |     | NULL    | all NULL
# | NumSensorFaults   | int(11)    | YES  |     | NULL    | all NULL
# | NumCommFaults     | int(11)    | YES  |     | NULL    | all NULL
# | NumOtherFaults    | int(11)    | YES  |     | NULL    | all NULL

# class PVArrayTimeSeries(models.Model):   INCORPORATED IN PlantTimeSeries
#     timeStamp = models.DateTimeField()
#     sampleInterval = models.IntegerField()
#     HPOA_DIFF = models.FloatField()
#     # meta-data
#     plant = models.ForeignKey(Plant)
#     pvArray = models.ForeignKey(PVArray)
#     recordStatus = models.IntegerField(default=1) # RECORD_STATUS_ACTIVE
#     def __str__(self):
#         return self.name

# | GPOA           | float       | YES  |     | NULL    |                |
# | HPOA_LAST      | float       | YES  |     | NULL    |                |
# | TMPBOM         | float       | YES  |     | NULL    |                |
# | DCW            | float       | YES  |     | NULL    |                |
# | DCWH_LAST      | float       | YES  |     | NULL    |                |
# | DCWH_DIFF      | float       | YES  |     | NULL    |                |


