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

class Plant(models.Model):
    plantuuid = models.CharField(max_length=254,blank=True,null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=254, blank=True, null=True)
    activationdate = models.DateField()
    postalcode = models.CharField(max_length=6,default='')
    state = models.CharField(max_length=2,default='')
    county = models.CharField(max_length=32,default='')
    city = models.CharField(max_length=32,default='')
    latitude = models.CharField(max_length=16,default='none')
    longitude = models.CharField(max_length=16,default='none')
    timezone = models.CharField(max_length=64,default='none')
    weathersource = models.CharField(max_length=32, blank=True, null=True) # CPR or local
    dcrating = models.FloatField(blank=True, null=True)     # watts (NOT kilo-watts)
    derate = models.FloatField(blank=True, null=True)
    # from PVArray
    trackertype = models.CharField(max_length=32)
    tilt = models.IntegerField()
    azimuth = models.IntegerField()
    # from StorageSystem
    storageoriginalcapacity = models.FloatField(blank=True,null=True)
    storagecurrentcapacity  = models.FloatField(blank=True,null=True)
    storagestateofcharge = models.FloatField(blank=True,null=True)
    # plant-meta-meta data
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

class UploadActivity(models.Model):
    requestTime = models.DateTimeField(auto_now_add=True)
    responseTime = models.DateTimeField(blank=True,null=True)
    plantUUID = models.CharField(max_length=254,blank=True,null=True)
    status = models.CharField(max_length=16)
    errorDetail = models.CharField(max_length=1024,blank=True,null=True)
    s3Key = models.CharField(max_length=254)
    account = models.ForeignKey(Account)
    plant = models.ForeignKey(Plant)
    def __str__(self):
        return self.name

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
    plant = models.ForeignKey(Plant)
    recordstatus = models.IntegerField(default=1) # RECORD_STATUS_ACTIVE
    def __str__(self):
        return self.name

class Total(models.Model):
    id = models.IntegerField(primary_key=True)
    totaldcrating = models.FloatField(blank=True, null=True)
    totalstoragecapacity = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osparc_total'


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


