from rest_framework import viewsets
from osparc.models import PlantType, Plant, StorageSystem
from osparc.serializers import PlantTypeSerializer, PlantSerializer, StorageSystemSerializer


class PlantTypeViewSet(viewsets.ModelViewSet):
    queryset = PlantType.objects.all()
    serializer_class = PlantTypeSerializer

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

class StorageSystemViewSet(viewsets.ModelViewSet):
    queryset = StorageSystem.objects.all()
    serializer_class = StorageSystemSerializer
