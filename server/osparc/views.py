from rest_framework import viewsets
from osparc.models import PlantType,Plant,StorageSystem,PVArray
from osparc.serializers import PlantTypeSerializer,PlantSerializer,StorageSystemSerializer,PVArraySerializer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer


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

@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='oSPARC API')
    return response.Response(generator.get_schema(request=request))
