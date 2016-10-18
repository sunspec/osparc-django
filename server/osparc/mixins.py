import datetime
import sys
import collections
from osparc.models import KPI
from osparc.serializers import KPISerializer

class KpiMixin(object):

    def median(self,lst):
        sortedLst = sorted(lst)
        lstLen = len(lst)
        index = (lstLen - 1) // 2
        if (lstLen % 2):
            return sortedLst[index]
        else:
            return (sortedLst[index] + sortedLst[index + 1])/2.0

    def buildKpi(self,entryList,name):
        firstEntry = datetime.date.today()
        lastEntry = datetime.datetime.strptime('01012001', '%d%m%Y').date()
        total = 0
        if len(entryList) > 0:
            minValue = sys.float_info.max
        else:
            minValue = 0
        maxValue = 0
        valueList = list()
        currentPlant = 0
        numberOfPlants = 0

        if len(entryList) > 0:
            for entry in entryList:
                if entry.plantId != currentPlant:
                    currentPlant = entry.plantId
                    numberOfPlants = numberOfPlants+1 # there are multiple entries from the same plant
                # print( "currentPlant=%d, entry.plantId=%d, numberOfPlants=%d" % (currentPlant,entry.plantId,numberOfPlants))
                if entry.timestamp < firstEntry:
                    firstEntry = entry.timestamp
                if entry.timestamp > lastEntry:
                    lastEntry = entry.timestamp
                total += entry.value
                if entry.value < minValue:
                    minValue = entry.value
                if entry.value > maxValue:
                    maxValue = entry.value
                valueList.append(entry.value)

        kpi = collections.defaultdict(dict)
        kpi['name'] = name
        kpi['plants'] = numberOfPlants
        kpi['firstday'] = firstEntry
        kpi['lastday'] = lastEntry
        kpi['minimum'] = round( minValue,1 )
        kpi['maximum'] = round( maxValue,1 )
        if len(entryList) > 0:
            kpi['mean'] = round(total/len(entryList),1)
        else:
            kpi['mean'] = 0
        if len(valueList) > 0:
            kpi['median'] = round( KpiMixin.median(self,valueList),1 )
        else:
            kpi['median'] = 0

        return kpi

    def divide( self, dict1, dict2 ):
        kpi = collections.defaultdict(dict)
        kpi['plants'] = min( dict1['plants'],dict2['plants'] )
        kpi['firstday'] = max( dict1['firstday'],dict2['firstday'] )
        kpi['lastday'] = min( dict1['lastday'],dict2['lastday'] )
        kpi['minimum'] = round(dict1['minimum'] / dict2['minimum'],2)
        kpi['maximum'] = round(dict1['maximum'] / dict2['maximum'],2)
        kpi['mean'] = round(dict1['mean'] / dict2['mean'],2)
        kpi['median'] = round(dict1['median'] / dict2['median'],2)
        return kpi

    def saveKpi( self,kpi,name ):
        existing = KPI.objects.all()
        try:
            existingKpi = KPI.objects.get(name=name)
            serializer = KPISerializer(existingKpi,data=kpi)
            valid = serializer.is_valid()
            serializer.save()
            return serializer.validated_data
        except:
            serializer = KPISerializer(data=kpi)
            valid = serializer.is_valid()
            serializer.save()
            return serializer.validated_data
        return

    def buildAndSaveKpi(self,entryList,name):
        return KpiMixin.saveKpi( self,KpiMixin.buildKpi(self,entryList,name),name )
