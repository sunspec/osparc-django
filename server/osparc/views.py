from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from osparc.models import Account,UploadActivity,PlantType,Plant,PlantTimeSeries
from osparc.serializers import AccountSerializer,UploadActivitySerializer,PlantTypeSerializer,PlantSerializer
from osparc.serializers import PlantTimeSeriesSerializer


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

class PlantTimeSeriesViewSet(viewsets.ModelViewSet):
    queryset = PlantTimeSeries.objects.all()
    serializer_class = PlantTimeSeriesSerializer

# counts
class PlantStatsView(APIView):
    def get(self, request, format=None):
        print request.query_params
        if 'count' in request.query_params:
            count = True
        try:
            by = request.query_params['by']
        except:
            by = None
        print by
        try:
            dc = request.query_params['DCRating']
        except:
            dc = None
        print dc

        if count:
            plantDict = { 'count': Plant.objects.count() }
            return Response(plantDict)

        return Response("KLARN")

class PlantDCCapacityView(APIView):
    def get(self, request, format=None):
        print request.query_params
        plants = Plant.objects.all()
        capacity = 0.0
        for plant in plants:
            capacity += plant.DCRating
        capDict = { 'DCCapacity':capacity}
        return Response(capDict)

# swagger
@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='oSPARC API')
    return response.Response(generator.get_schema(request=request))
