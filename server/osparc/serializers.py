from rest_framework import serializers
from osparc.models import Account,UploadActivity,PlantType,Plant
from osparc.models import PlantTimeSeries

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
        fields = ("plantUUID","name","description","activationDate","postalCode","state","county","city",
            "latitude","longitude","timeZone","weatherSource","DCRating","derate","trackerType","tilt","azimuth",
            "storageOriginalCapacity","storageCurrentCapacity","storageStateOfCharge","accountID",
            "versionCreationTime","versionID","solarAnywhereSite")

class PlantTimeSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantTimeSeries
        fields = ("timeStamp","sampleInterval","WH_DIFF","GHI_DIFF","TMPAMB_AVG","plant","recordStatus")

