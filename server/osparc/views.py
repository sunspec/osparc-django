from django.http import Http404
import collections
import datetime
import sys
import math

#import library
from django.db import connection
from django.forms.models import model_to_dict

from rest_framework import viewsets
from rest_framework import status
from rest_framework import response, schemas
from rest_framework import generics
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.mixins import ListModelMixin

from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from osparc.models import Account,UploadActivity,PlantType,Plant,PlantTimeSeries
from osparc.models import KPI
from osparc.serializers import AccountSerializer,UploadActivitySerializer,PlantTypeSerializer,PlantSerializer
from osparc.serializers import PlantTimeSeriesSerializer,KPISerializer
from .mixins import KpiMixin


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

class KPIViewSet(viewsets.ModelViewSet):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer


# plants
class PlantSummary:
    def __init__(self,id,name,uuid,state,postalcode,activationdate,dcrating,link):
        self.id = id
        self.name = name
        self.uuid = uuid
        self.state = state
        self.postalcode = postalcode
        self.activationdate = activationdate
        self.dcrating = dcrating
        self.link = link

    def serialize(obj):
        return {
            "id": obj.id,
            "name":   obj.name,
            "uuid": obj.uuid,
            "state": obj.state,
            "postalcode": obj.postalcode,
            "activationdate": obj.activationdate,
            "dcrating": obj.dcrating,
            "link": obj.link
        }

class PlantView(APIView):

    def summary(self, queryset, request, format=None):
        result = collections.defaultdict(int)
        result['count'] = '/api/plants/count'
        result['kpi'] = '/api/plants/kpi'
        result['capacity'] = '/api/plants/capacity'
        result['plants'] = list()

        for plant in queryset:
            ps = PlantSummary(plant.id,plant.name,plant.plantuuid,plant.state,plant.postalcode,plant.activationdate,plant.dcrating,("/api/plants/%s" % (plant.id)))
            result['plants'].append( ps.serialize() )

        return result

    def get(self, request, format=None):
        if 'id' in request.query_params:
            plantId = int(request.query_params['id'][0])
            plant = Plant.objects.get(id=plantId)
            return Response(model_to_dict(plant))
        queryset = Plant.objects.all()
        res = PlantView.summary(self,queryset,request,format)
        return Response(PlantView.summary(self,queryset,request,format))

# stats
class StatsView(APIView):

    def plantsByState(self,plants):
        result = collections.defaultdict(int)
        for plant in plants:
            result[plant.state] += 1
        return result

    def plantsByYear(self,plants):
        result = collections.defaultdict(int)
        for plant in plants:
            adate = plant.activationdate
            result[adate.year] += 1
        return result

    def plantsByYearAnddcrating(self,plants):
            # there are 12 years and 5 dcrating buckets
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
            result['2016']['<10kW'] = 0
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
                adate = plant.activationdate
                for yearBucket in [2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]:
                    if adate.year == yearBucket:
                        # for rangeBucket in [[0,10],[10,100],[100,1000],[1000,10000],[10000,sys.maxint]:
                        if plant.dcrating/1000 < 10:
                            result[str(yearBucket)]['<10kW'] += 1
                        elif plant.dcrating/1000 < 100:
                            result[str(yearBucket)]['10-100kW'] += 1
                        elif plant.dcrating/1000 < 1000:
                            result[str(yearBucket)]['100kW-1MW'] += 1
                        elif plant.dcrating/1000 < 10000:
                            result[str(yearBucket)]['1-10MW'] += 1
                        else:
                            result[str(yearBucket)]['>10MW'] += 1
            return result

    def totals(self):
        result = collections.defaultdict(dict)

        result['count'] = Plant.objects.count()

        # osparc_total is a view containing the sums of dcrating and storageorigcapacity.
        # The following abomination is required to read views. As if that were not abominable
        # enough, you have to create the view manually, separate from makemigrations.
        # There's a good chance I'll replace this with a table that I populate in code whenever
        # a plant is added..
        cursor = connection.cursor()
        sql_string = 'SELECT * FROM osparc_total'
        cursor.execute(sql_string)
        dbRes = cursor.fetchall()
        result['DCRating'] = dbRes[0][0]
        result['StorageCapacity'] = dbRes[0][1]

        return result


    def get(self, request, format=None):

        # note: this is executed for both plants/count and plants/capacity. Both return both...
        if not dict(request.query_params.iterlists()):
            return Response(StatsView.totals(self))

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
                return Response(StatsView.plantsByState(self,plants))

            if year == True and dc == False:
                return Response(StatsView.plantsByYear(self,plants))

            if year == True and dc == True:
                return Response(StatsView.plantsByYearAnddcrating(self,plants))

        return Response({"I don't understand the query string": dict(request.query_params.iterlists()).keys()[0]})

# KPIs
class KpiTimeseriesElement:
    def __init__(self,plantId,timestamp,numerator,denominator):
        self.plantId = plantId
        self.timestamp = timestamp
        self.value = numerator/denominator

class KPIsView(APIView):

    def create(self, validated_data):
        return KPI.objects.create(**validated_data)

    def calculateKPIs(self):

        mixin = KpiMixin()

        # dcrating and StorageCapacity
        plants = Plant.objects.all()

        dcList = list()
        storCapList = list()
        storSOHList = list()
        for plant in plants:
            if plant.dcrating is not None:
                dcList.append( KpiTimeseriesElement(plant.id,plant.activationdate,plant.dcrating,1) )
            if plant.storageoriginalcapacity is not None:
                storCapList.append( KpiTimeseriesElement(plant.id,plant.activationdate,plant.storageoriginalcapacity,1) )
                if plant.storagecurrentcapacity is not None:
                    storSOHList.append( KpiTimeseriesElement(plant.id,plant.activationdate,plant.storagecurrentcapacity,plant.storageoriginalcapacity) )
                else:
                    storCapList.append( KpiTimeseriesElement(plant.id,plant.activationdate,plant.storageoriginalcapacity,1) )

        # Fill in the plant-related KPIs
        result = collections.defaultdict(dict)

        # 1. DC Power Rating (rated DC power)
        result['DCRating'] = KpiMixin.buildAndSaveKpi(mixin,dcList,'DCRating')

        # 2. Storage Capacity
        result['StorageCapacity'] = KpiMixin.buildAndSaveKpi(mixin,storCapList,'StorageCapacity')

        # 3. Storage State of Health
        result['StorageStateOfHealth'] = KpiMixin.buildAndSaveKpi(mixin,storSOHList,'StorageStateOfHealth')

        #  Now the timeseries-related KPIs
        timeseries = PlantTimeSeries.objects.all()

        # First, get a list of each element that will contribute to each KPI
        # We get a separate list per KPI because not all time series elements contain all measurements
        ghiList = list()
        whList = list()
        yfList = list()
        yrList = list()
        for entry in timeseries:
            if entry.GHI_DIFF is not None:
                ghiList.append( KpiTimeseriesElement(entry.plant.id,entry.timestamp.date(),entry.GHI_DIFF,1) )
            if entry.WH_DIFF is not None:
                whList.append( KpiTimeseriesElement(entry.plant.id,entry.timestamp.date(),entry.WH_DIFF,1) )
                yfList.append( KpiTimeseriesElement(entry.plant.id,entry.timestamp.date(),entry.WH_DIFF,entry.plant.dcrating) )
            if entry.HPOA_DIFF is not None:
                yrList.append( KpiTimeseriesElement(entry.plant.id,entry.timestamp.date(),entry.HPOA_DIFF,1000) )

        # Now calculate the KPIs

        # 1. GHI (daily insolation)
        result['MonthlyInsolation'] = KpiMixin.buildAndSaveKpi(mixin,ghiList,'MonthlyInsolation')

        # 2. WH (daily generated energy)
        result['MonthlyGeneratedEnergy'] = KpiMixin.buildAndSaveKpi(mixin,whList,'MonthlyGeneratedEnergy')

        # 3. YF (generated yield kWh/kWp)
        result['MonthlyYield'] = KpiMixin.buildAndSaveKpi(mixin,yfList,'MonthlyYield')
        
        # 4. YR (hpoa yield kWh/kWp)
        if len(yrList) > 0:
            result['PerformanceRatio'] = KpiMixin.divide(mixin,result['MonthlyYield'],KpiMixin.buildKpi(mixin,yrList,''))
            result['PerformanceRatio']['name'] = 'PerformanceRatio'
            KpiMixin.saveKpi(mixin,result['PerformanceRatio'],'PerformanceRatio')

        return result

    def get(self, request, format=None):

        print("calculating kpis starting %s" % (datetime.datetime.now()))

        kpis = KPIsView.calculateKPIs(self)

        print("calculating kpis finished %s" % (datetime.datetime.now()))

        return Response(kpis)


# swagger
@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='oSPARC API')
    return response.Response(generator.get_schema(request=request))
