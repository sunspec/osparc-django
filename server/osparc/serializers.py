from rest_framework import serializers
from osparc.models import PlantType,Plant,StorageSystem


class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantType
        fields = ("name", "description")

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ("name","description","activationDate","type","postalCode","state","county","city","latitude","longitude","timeZone","DCOptimized","inverterType","weatherSource","designModel","nominalACPowerRating","ACCapacity","DCRating","derate","degradationRate")

class StorageSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageSystem
        fields = ("name", "description", "plant", "activationDate", "originalCapacity", "currentCapacity", "stateOfCharge")


