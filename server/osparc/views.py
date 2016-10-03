from rest_framework import viewsets
from osparc.models import Account,UploadActivity,PlantType,Plant,StorageSystem,PVArray,PlantTimeSeries,PVArrayTimeSeries
from osparc.serializers import AccountSerializer,UploadActivitySerializer,PlantTypeSerializer,PlantSerializer,StorageSystemSerializer,PVArraySerializer
from osparc.serializers import PlantTimeSeriesSerializer,PVArrayTimeSeriesSerializer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class UploadActivityViewSet(viewsets.ModelViewSet):
    queryset = UploadActivity.objects.all()
    serializer_class = UploadActivitySerializer

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

class PlantTimeSeriesViewSet(viewsets.ModelViewSet):
    queryset = PlantTimeSeries.objects.all()
    serializer_class = PlantTimeSeriesSerializer

class PVArrayTimeSeriesViewSet(viewsets.ModelViewSet):
    queryset = PVArrayTimeSeries.objects.all()
    serializer_class = PVArrayTimeSeriesSerializer

@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='oSPARC API')
    return response.Response(generator.get_schema(request=request))
