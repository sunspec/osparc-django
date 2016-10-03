from rest_framework import serializers
from osparc.models import Account,UploadActivity,PlantType,Plant,StorageSystem,PVArray
from osparc.models import PlantTimeSeries,PVArrayTimeSeries

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("accountID","role","name","companyName","companyAddress","companyCityState","companyPostalCode","email","password")

class UploadActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadActivity
        fields = ("account","requestTime","responseTime","plantUUID","status","errorDetail","s3Key")

class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantType
        fields = ("name", "description")

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ("name","description","activationDate","postalCode","state","county","city","latitude","longitude","timeZone","account")

class StorageSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageSystem
        fields = ("name","description","plant","activationDate","originalCapacity","currentCapacity", "stateOfCharge")

class PVArraySerializer(serializers.ModelSerializer):
    class Meta:
        model = PVArray
        fields = ("name","description","arrayId","trackerType","tilt","azimuth","plant")

class PVArraySerializer(serializers.ModelSerializer):
    class Meta:
        model = PVArray
        fields = ("name","description","arrayId","trackerType","tilt","azimuth","plant")

class PlantTimeSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantTimeSeries
        fields = ("timeStamp","sampleInterval","WH_DIFF","GHI_DIFF","TMPAMB_AVG","plant","recordStatus")

class PVArrayTimeSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PVArrayTimeSeries
        fields = ("timeStamp","sampleInterval","HPOA_DIFF","plant","pvArray","recordStatus")
