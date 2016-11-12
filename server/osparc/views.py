from django.http import Http404
import collections
import datetime
import sys
import math
import uuid

#import library
from django.db import connection
from django.forms.models import model_to_dict

from rest_framework import viewsets
from rest_framework import status
from rest_framework import response, schemas
from rest_framework import generics
from rest_framework import mixins
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.mixins import ListModelMixin

from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from osparc.models import Account,UploadActivity,PlantType,Plant,PlantTimeSeries
from osparc.models import ReportDefinition,ReportRun,UploadActivity,PlantReport
from osparc.models import KPI
from osparc.serializers import AccountSerializer,UploadActivitySerializer,PlantTypeSerializer,PlantSerializer
from osparc.serializers import PlantReportSerializer,PlantTimeSeriesSerializer,KPISerializer
from osparc.serializers import ReportDefinitionSerializer,ReportRunSerializer

from .mixins import KPIs


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class UploadActivityViewSet(viewsets.ModelViewSet):
    queryset = UploadActivity.objects.all()
    serializer_class = UploadActivitySerializer

class PlantTypeViewSet(viewsets.ModelViewSet):
    queryset = PlantType.objects.all()
    serializer_class = PlantTypeSerializer

class PlantTimeSeriesViewSet(viewsets.ModelViewSet):
    queryset = PlantTimeSeries.objects.all()
    serializer_class = PlantTimeSeriesSerializer

    # override create in order to update the uploadActivity entry
    def perform_create(self, serializer):

        instance = serializer.save()

        # Find the plant associated with this timeseries element.
        # If the timeseries element's plant attribute is set, it is the db id
        # of the plant. If not, then it is specified by the timeseries element's uuid.
        # That is the case of importing from oSPARC v1, where the timeseries' plant
        # attribute is not imported because the db id of the plant is likely different
        # in oSPARC v2.
        # When a new timeseries element is added, the plant's PlantReport must be 
        # re-generated (since there is new data). We invalidate it here if it exists,
        # and it is recalculated asynchronously.

        try:
            if instance.plant != None and instance.plant > 0:
                plant = Plant.objects.get(id=instance.plant_id)
            else:
                plant = Plant.objects.get(uuid=instance.plantUUID)

                instance.plant = plant
                if serializer.is_valid():
                    serializer.save()
                else:
                    print serializer.errors

            # here, we have identified the plant

            # (1) update the uploadactivity 
            try:
                ua = UploadActivity.objects.get(id=plant.uploadactivity_id)
                ua.mostrecenttimeseriesuploadtime = datetime.datetime.now()
                ua.status = 'success'
                ua.save()
            except:
                print "ERROR updating UA"

            # (2) invalidate the plantreport
            try:
                report = plant.plantreport
                report.recordstatus = 9     # invalid
                newser = PlantReportSerializer(report, data=report.__dict__)
                if newser.is_valid():
                    newser.save()
                else:
                    print "ERROR invalidating PlantReport: errors:",newser.errors
            except:
                print "ERROR invalidating PlantReport"


        except:
            print "Unable to locate plant for timeseries %s" % instance.timestamp
            return


class KPIViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer

class KPIView(generics.ListAPIView):
    def list(self, request):
        queryset = KPI.objects.all()
        serializer = KPISerializer(queryset, many=True)
        return Response(serializer.data)


# plants
class PlantList(generics.ListCreateAPIView):
    serializer_class = PlantSerializer

    def get_queryset(self):
        queryset = Plant.objects.all()
        uuid = self.request.query_params.get('uuid', None)
        if uuid is not None:
            queryset = queryset.filter(uuid=uuid)
        return queryset

    # override create in order to generate a random uuid if one is not provided,
    # and to create an UploadActivity entry
    def perform_create(self, serializer):

        instance = serializer.save()

        instance.uploadactivity = UploadActivity.objects.create()
        instance.plantreport = PlantReport.objects.create()

        if instance.uuid == None or instance.uuid == "":
            instance.uuid = str(uuid.uuid4());
            
        newser = PlantSerializer(instance, data=instance.__dict__)
        if newser.is_valid():
            newser.save()
        else:
            print "newser errors:",newser.errors

# class PlantDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Plant.objects.all()
#     serializer_class = PlantSerializer

class PlantReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlantReport.objects.all()
    serializer_class = PlantReportSerializer


class PlantDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

    def createAndSaveReport(self,plant):
        # TODO TBD XXX this is horrible - figure out how to apply a filter to PlantTimeSeries.all()
        timeseriesrecords = PlantTimeSeries.objects.all()
        myrecords = list()
        for record in timeseriesrecords:
            if record.plant.id == plant.id:
                myrecords.append(record)

        print len(myrecords)

        plants = [ plant ]

        mixin = KPIs()
        kpis = mixin.calculateKPIs(plants,myrecords)

        try:
            firstmeasdate = kpis['PerformanceRatio']['firstday']
        except:
            firstmeasdate = None
        try:
            lastmeasdate = kpis['PerformanceRatio']['lastday']
        except:
            lastmeasdate = None
        try:
            monthlyyield = kpis['MonthlyYield']['mean'] # production yield kWh/kWdc
        except:
            monthlyyield = None
        try:
            pr = kpis['PerformanceRatio']['mean'] # performance ratio yf/yr
        except:
            pr = None
        try:
            soh = kpis['StorageStateOfHealth']['mean']
        except:
            soh = None

        plantreportData = { 'recordstatus':1,
                            'createtime':datetime.datetime.now(),
                            'sampleinterval':'monthly',
                            'firstmeasurementdate':firstmeasdate,
                            'lastmeasurementdate':lastmeasdate,
                            'monthlyyield':monthlyyield,
                            'performanceratio':pr,
                            'StorageStateofhealth':soh
        }

        # we save the report regardless of whether there were timeseries elements - the report is complete
        serializer = PlantReportSerializer(plant.plantreport,data=plantreportData)
        if serializer.is_valid():
            serializer.save()
        else:
            print "ERROR saving plantreport:",serializer.errors

    def get(self, request, pk, format=None):
        plant = Plant.objects.get(pk=pk)

        if plant.plantreport.recordstatus == 9:
            # must create plantreport

            self.createAndSaveReport(plant)

            # the report was built & saved so we have to get the updated plant
            plant = Plant.objects.get(pk=pk)

        serializer = PlantSerializer(plant)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# queries & reports
class ReportDefinitionList(generics.ListCreateAPIView):
    queryset = ReportDefinition.objects.all()
    serializer_class = ReportDefinitionSerializer


class ReportDefinitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReportDefinition.objects.all()
    serializer_class = ReportDefinitionSerializer


class ReportRunList(generics.ListCreateAPIView):
    queryset = ReportRun.objects.all()
    serializer_class = ReportRunSerializer



class ReportRunDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReportRun.objects.all()
    serializer_class = ReportRunSerializer


# stats
class AggregatesView(APIView):

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

    def plantsByYearAndDcrating(self,plants):
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
                if plant.dcrating is not None:
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

        #  count, dcrating
        result = dict(AggregatesView.totals(self))

        #  kpis
        result['kpis'] = KPISerializer(KPI.objects.all(), context={'request': request}, many=True).data

        # wacky groupings if needed

        queries = dict(request.query_params.iterlists())

        if 'by' in request.query_params:
            year = False
            dc = False
            state = False
            by = queries['by']
            if 'year' in by:
                year = True
            if 'dcrating' in by:
                dc = True
            if 'state' in by:
                state = True

            print("year=%s,dc=%s,state=%s" %(year,dc,state))

            if year == False and dc == False and state == False:
                return Response({"I don't understand the query string": dict(request.query_params.iterlists()).keys()[0]})

            plants = Plant.objects.all()

            if state == True:
                result['bystate'] = AggregatesView.plantsByState(self,plants)

            if year == True and dc == False:
                result['byyear'] = AggregatesView.plantsByYear(self,plants)

            if year == True and dc == True:
                result['byyearanddcrating'] = AggregatesView.plantsByYearAndDcrating(self,plants)

        return Response(result)


# KPIs
class KPIsView(APIView):

    def create(self, validated_data):
        return KPI.objects.create(**validated_data)

    def get(self, request, format=None):

        print("calculating kpis starting %s" % (datetime.datetime.now()))

        plants = Plant.objects.all()
        timeseries = PlantTimeSeries.objects.all()

        mixin = KPIs()

        kpis = mixin.calculateKPIs(plants,timeseries)

        print("calculating kpis finished %s" % (datetime.datetime.now()))

        return Response(kpis)


# swagger
@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='oSPARC API')
    return response.Response(generator.get_schema(request=request))


