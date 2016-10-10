from django.http import Http404
import collections
import datetime
import sys

from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

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

# stats
class PlantStatsView(APIView):

    def plantsByState(self,plants):
        result = collections.defaultdict(int)
        for plant in plants:
            result[plant.state] += 1
        return result

    def plantsByYear(self,plants):
        result = collections.defaultdict(int)
        for plant in plants:
            adate = plant.activationDate
            result[adate.year] += 1
        return result

    def plantsByYearAndDCRating(self,plants):
            # there are 12 years and 5 DCRating buckets
            result = collections.defaultdict(dict)
            result['2007']['<10kW'] = 0
            result['2007']['10-100kW'] = 0
            result['2007']['100kW-1MW'] = 0
            result['2007']['1-10MW'] = 0
            result['2007']['>10MW'] = 0
            result['2008']['<10kW'] = 0
            result['2008']['10-100kW'] = 0
            result['2008']['100kW-1MW'] = 0
            result['2008']['1-10MW'] = 0
            result['2008']['>10MW'] = 0
            result['2009']['<10kW'] = 0
            result['2009']['10-100kW'] = 0
            result['2009']['100kW-1MW'] = 0
            result['2009']['1-10MW'] = 0
            result['2009']['>10MW'] = 0
            result['2010']['<10kW'] = 0
            result['2010']['10-100kW'] = 0
            result['2010']['100kW-1MW'] = 0
            result['2010']['1-10MW'] = 0
            result['2010']['>10MW'] = 0
            result['2011']['<10kW'] = 0
            result['2011']['10-100kW'] = 0
            result['2011']['100kW-1MW'] = 0
            result['2011']['1-10MW'] = 0
            result['2011']['>10MW'] = 0
            result['2012']['<10kW'] = 0
            result['2012']['10-100kW'] = 0
            result['2012']['100kW-1MW'] = 0
            result['2012']['1-10MW'] = 0
            result['2012']['>10MW'] = 0
            result['2013']['<10kW'] = 0
            result['2013']['10-100kW'] = 0
            result['2013']['100kW-1MW'] = 0
            result['2013']['1-10MW'] = 0
            result['2013']['>10MW'] = 0
            result['2014']['<10kW'] = 0
            result['2014']['10-100kW'] = 0
            result['2014']['100kW-1MW'] = 0
            result['2014']['1-10MW'] = 0
            result['2014']['>10MW'] = 0
            result['2015']['<10kW'] = 0
            result['2015']['10-100kW'] = 0
            result['2015']['100kW-1MW'] = 0
            result['2015']['1-10MW'] = 0
            result['2015']['>10MW'] = 0
            result['2015']['<10kW'] = 0
            result['2016']['10-100kW'] = 0
            result['2016']['100kW-1MW'] = 0
            result['2016']['1-10MW'] = 0
            result['2016']['>10MW'] = 0
            result['2017']['<10kW'] = 0
            result['2017']['10-100kW'] = 0
            result['2017']['100kW-1MW'] = 0
            result['2017']['1-10MW'] = 0
            result['2017']['>10MW'] = 0
            result['2018']['<10kW'] = 0
            result['2018']['10-100kW'] = 0
            result['2018']['100kW-1MW'] = 0
            result['2018']['1-10MW'] = 0
            result['2018']['>10MW'] = 0
            for plant in plants:
                adate = plant.activationDate
                for yearBucket in [2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]:
                    if adate.year == yearBucket:
                        # for rangeBucket in [[0,10],[10,100],[100,1000],[1000,10000],[10000,sys.maxint]:
                        if plant.DCRating < 10:
                            result[str(yearBucket)]['<10kW'] += 1
                        elif plant.DCRating < 100:
                            result[str(yearBucket)]['10-100kW'] += 1
                        elif plant.DCRating < 1000:
                            result[str(yearBucket)]['100kW-1MW'] += 1
                        elif plant.DCRating < 10000:
                            result[str(yearBucket)]['1-10MW'] += 1
                        else:
                            result[str(yearBucket)]['>10MW'] += 1
            return result

    def totals(self):
        result = collections.defaultdict(dict)
        result['count'] = Plant.objects.count()

        plants = Plant.objects.all()
        dcCap = 0.0
        stCap = 0.0
        for plant in plants:
            dcCap += plant.DCRating
            if plant.storageOriginalCapacity is not None:
                stCap += plant.storageOriginalCapacity
        result['DCRating'] = dcCap
        result['StorageCapacity'] = stCap

        return result


    def get(self, request, format=None):

        if not dict(request.query_params.iterlists()):
            return Response(PlantStatsView.totals(self))

        queries = dict(request.query_params.iterlists())

        if 'by' in request.query_params:
            year = False
            dc = False
            state = False
            by = queries['by']
            if 'year' in by:
                year = True
            if 'DCRating' in by:
                dc = True
            if 'state' in by:
                state = True

            plants = Plant.objects.all()

            if state == True:
                return Response(PlantStatsView.plantsByState(self,plants))

            if year == True and dc == False:
                return Response(PlantStatsView.plantsByYear(self,plants))

            if year == True and dc == True:
                return Response(PlantStatsView.plantsByYearAndDCRating(self,plants))

        return Response({"I don't understand the query string": dict(request.query_params.iterlists()).keys()[0]})

# KPIs
class PlantKPIsView(APIView):

    def median(self,lst):
        sortedLst = sorted(lst)
        lstLen = len(lst)
        index = (lstLen - 1) // 2
        if (lstLen % 2):
            return sortedLst[index]
        else:
            return (sortedLst[index] + sortedLst[index + 1])/2.0


    def totals(self):

        # DCRating and StorageCapacity
        plants = Plant.objects.all()
        dcCapList = list()
        storCapList = list()

        dcCapTotal = 0.0
        dcCapMin = sys.float_info.max
        dcCapMax = 0.0
        dcCapFirstEntry = datetime.date.today()
        dcCapLastEntry = datetime.datetime.strptime('01012001', '%d%m%Y').date()

        storCapTotal = 0.0
        storCapMin = sys.float_info.max
        storCapMax = 0.0
        storCapFirstEntry = datetime.date.today()
        storCapLastEntry = datetime.datetime.strptime('01012001', '%d%m%Y').date()

        for plant in plants:
            if plant.DCRating is not None:
                if plant.activationDate < dcCapFirstEntry:
                    dcCapFirstEntry = plant.activationDate
                if plant.activationDate > dcCapLastEntry:
                    dcCapLastEntry = plant.activationDate
                dcCapTotal += plant.DCRating
                dcCapList.append(plant.DCRating)
                if plant.DCRating < dcCapMin:
                    dcCapMin = plant.DCRating
                if plant.DCRating > dcCapMax:
                    dcCapMax = plant.DCRating

            if plant.storageOriginalCapacity is not None:
                if plant.activationDate < storCapFirstEntry:
                    storCapFirstEntry = plant.activationDate
                if plant.activationDate > storCapLastEntry:
                    storCapLastEntry = plant.activationDate
                storCapTotal += plant.storageOriginalCapacity
                storCapList.append(plant.storageOriginalCapacity)
                if plant.storageOriginalCapacity < storCapMin:
                    storCapMin = plant.storageOriginalCapacity
                if plant.storageOriginalCapacity > storCapMax:
                    storCapMax = plant.storageOriginalCapacity

        result = collections.defaultdict(dict)

        dcRating = collections.defaultdict(dict)
        dcRating['plants'] = len(dcCapList)
        dcRating['firstDay'] = dcCapFirstEntry
        dcRating['lastDay'] = dcCapLastEntry
        dcRating['min'] = dcCapMin
        dcRating['max'] = dcCapMax
        dcRating['mean'] = dcCapTotal / len(dcCapList)
        dcRating['median'] = PlantKPIsView.median(self,dcCapList)
        result['DCRating'] = dcRating

        storCap = collections.defaultdict(dict)
        if len(storCapList) > 0:
            storCap['plants'] = len(storCapList)
            storCap['firstDay'] = storCapFirstEntry
            storCap['lastDay'] = storCapLastEntry
            storCap['min'] = storCapMin
            storCap['max'] = storCapMax
            storCap['mean'] = storCapTotal / len(storCapList)
            storCap['median'] = PlantKPIsView.median(self,storCapList)
        else:
            storCap['plants'] = 0
            storCap['firstDay'] = datetime.datetime.strptime('01012001', '%d%m%Y').date()
            storCap['lastDay'] = datetime.date.today()
            storCap['min'] = 0.0
            storCap['max'] = 0.0
            storCap['mean'] = 0.0
            storCap['median'] = 0.0
        result['StorageCapacity'] = storCap

        return result

    def get(self, request, format=None):

        if not dict(request.query_params.iterlists()):
            return Response(PlantKPIsView.totals(self))

        queries = dict(request.query_params.iterlists())

        return Response({"I don't understand the query string": dict(request.query_params.iterlists()).keys()[0]})
       


# swagger
@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='oSPARC API')
    return response.Response(generator.get_schema(request=request))
