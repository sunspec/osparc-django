from rest_framework import serializers
from osparc.models import PlantType,Plant,StorageSystem,PVArray


class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantType
        fields = ("name", "description")

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ("name","description","activationDate","postalCode","state","county","city","latitude","longitude","timeZone")

class StorageSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageSystem
        fields = ("name","description","plant","activationDate","originalCapacity","currentCapacity", "stateOfCharge")

class PVArraySerializer(serializers.ModelSerializer):
    class Meta:
        model = PVArray
        fields = ("name","description","plant","arrayId","trackerType","tilt","azimuth")

