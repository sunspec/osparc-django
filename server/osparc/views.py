from rest_framework import viewsets
from osparc.models import PlantType, Plant
from osparc.serializers import PlantTypeSerializer, PlantSerializer


class PlantTypeViewSet(viewsets.ModelViewSet):
    queryset = PlantType.objects.all()
    serializer_class = PlantTypeSerializer

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

