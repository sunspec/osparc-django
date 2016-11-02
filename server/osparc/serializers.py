from rest_framework import serializers
from osparc import models

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ("accountID","role","name","companyName","companyAddress","companyCityState","companyPostalCode","email","password")

class UploadActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UploadActivity
        fields = ("plantuploadtime","mostrecenttimeseriesuploadtime","status","errorDetail")

class PlantTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.PlantType
        fields = ("name", "description")

class PlantReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlantReport
        fields = ("recordstatus","createtime","sampleinterval","firstmeasurementdate","lastmeasurementdate","monthlyyield","performanceratio","storagestateofhealth")

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = models.Plant
        fields = ("id","uuid","name","activationdate","dcrating","postalcode","state",
            "description","county","city",
            "latitude","longitude","timezone","weathersource","derate","arraytype","tilt","azimuth",
            "storageoriginalcapacity","storagecurrentcapacity","storagestateofcharge","plantreport","accountid",
            "versioncreationtime","versionid","solaranywheresite","uploadactivity")

class PlantTimeSeriesSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = models.PlantTimeSeries
        fields = ("id","timestamp","sampleinterval","WH_DIFF","GHI_DIFF","TMPAMB_AVG","HPOA_DIFF","plant","recordstatus","plantUUID")

class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KPI
        fields = ("name","reportrun","plants","sampleinterval","firstday","lastday","mean","median","minimum","maximum")

class ReportDefinitionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = models.ReportDefinition
        fields = ("id","name","observationstartdate","observationenddate","plantfilterattribute","plantfilteroperation","plantfiltervalue")

class ReportRunSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    kpis = KPISerializer(source='kpi_set',many=True)
    class Meta:
        model = models.ReportRun
        fields = ("id","status","reportdefinition","runsubmittime","runstarttime","runcompletetime","firstmeasurementdate",
                "lastmeasurementdate","numberofmeasurements","numberofplants","totaldccapacity","totalstoragecapacity","kpis")
