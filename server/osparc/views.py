from rest_framework import viewsets
from osparc.models import PlantType,Plant,StorageSystem,PVArray
from osparc.serializers import PlantTypeSerializer,PlantSerializer,StorageSystemSerializer,PVArraySerializer


class PlantTypeViewSet(viewsets.ModelViewSet):
    queryset = PlantType.objects.all()
    serializer_class = PlantTypeSerializer

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

class StorageSystemViewSet(viewsets.ModelViewSet):
    queryset = StorageSystem.objects.all()
    serializer_class = StorageSystemSerializer

class PVArrayViewSet(viewsets.ModelViewSet):
    queryset = PVArray.objects.all()
    serializer_class = PVArraySerializer
