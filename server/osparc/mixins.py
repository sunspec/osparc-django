import datetime
import sys
import collections
from osparc.models import KPI
from osparc.serializers import KPISerializer

class KpiTimeseriesElement:
    def __init__(self,plantId,timestamp,numerator,denominator):
        self.plantId = plantId
        self.timestamp = timestamp
        self.value = numerator/denominator

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


    def calculateKPIs(self,plants,timeseries):

        # dcrating and StorageCapacity

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
        result['DCRating'] = self.buildAndSaveKpi(dcList,'DCRating')

        # 2. Storage Capacity
        result['StorageCapacity'] = self.buildAndSaveKpi(storCapList,'StorageCapacity')

        # 3. Storage State of Health
        result['StorageStateOfHealth'] = self.buildAndSaveKpi(storSOHList,'StorageStateOfHealth')

        #  Now the timeseries-related KPIs

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
        result['MonthlyInsolation'] = self.buildAndSaveKpi(ghiList,'MonthlyInsolation')

        # 2. WH (daily generated energy)
        result['MonthlyGeneratedEnergy'] = self.buildAndSaveKpi(whList,'MonthlyGeneratedEnergy')

        # 3. YF (generated yield kWh/kWp)
        result['MonthlyYield'] = self.buildAndSaveKpi(yfList,'MonthlyYield')
        
        # 4. YR (hpoa yield kWh/kWp)
        if len(yrList) > 0:
            result['PerformanceRatio'] = self.divide(result['MonthlyYield'],self.buildKpi(yrList,''))
            result['PerformanceRatio']['name'] = 'PerformanceRatio'
            self.saveKpi(result['PerformanceRatio'],'PerformanceRatio')

        return result
