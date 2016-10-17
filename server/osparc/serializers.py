from rest_framework import serializers
from osparc import models

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ("accountID","role","name","companyName","companyAddress","companyCityState","companyPostalCode","email","password")

class UploadActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UploadActivity
        fields = ("account","requestTime","responseTime","plantUUID","status","errorDetail","s3Key")

class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlantType
        fields = ("name", "description")

class PlantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Plant
        fields = ("plantuuid","name","description","activationdate","postalcode","state","county","city",
            "latitude","longitude","timezone","weathersource","dcrating","derate","trackertype","tilt","azimuth",
            "storageoriginalcapacity","storagecurrentcapacity","storagestateofcharge","accountid",
            "versioncreationtime","versionid","solaranywheresite")

class PlantTimeSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlantTimeSeries
        fields = ("timestamp","sampleinterval","WH_DIFF","GHI_DIFF","TMPAMB_AVG","HPOA_DIFF","plant","recordstatus")

# class TotalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Total
#         fields = ("totaldcrating","totalstoragecapacity")
