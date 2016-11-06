import datetime
import sys
import collections
from models import KpiTimeseriesElement

# XXX TBD TODO Heinosity Alert:
# This, i.e. the script that runs reports, uses models that are very similar, but different,
# from the models used in the django web services.
# They should be combined; meanwhile, tread carefully!


class KPIs(object):

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
        kpi['minimum'] = round( minValue,3 )
        kpi['maximum'] = round( maxValue,3 )
        if len(entryList) > 0:
            kpi['mean'] = round(total/len(entryList),3)
        else:
            kpi['mean'] = 0
        if len(valueList) > 0:
            kpi['median'] = round( KPIs.median(self,valueList),3 )
        else:
            kpi['median'] = 0
        kpi['sampleinterval'] = 'monthly'

        return kpi

    def divide( self, dict1, dict2 ):
        kpi = collections.defaultdict(dict)
        kpi['plants'] = min( dict1['plants'],dict2['plants'] )
        kpi['firstday'] = max( dict1['firstday'],dict2['firstday'] )
        kpi['lastday'] = min( dict1['lastday'],dict2['lastday'] )
        kpi['minimum'] = round(dict1['minimum'] / dict2['minimum'],3)
        kpi['maximum'] = round(dict1['maximum'] / dict2['maximum'],3)
        kpi['mean'] = round(dict1['mean'] / dict2['mean'],3)
        kpi['median'] = round(dict1['median'] / dict2['median'],3)
        kpi['sampleinterval'] = dict1['sampleinterval']
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

    def findPlantsDcrating(self,plants,id):
        for plant in plants:
            if plant.id == id:
                return plant.dcrating
        return None

    def calculatePlantKPIs(self,plants):

        # dcrating, StorageCapacity and storage State of Health

        dcList = list()
        storCapList = list()
        storSOHList = list()

        try:
            for plant in plants:
                if plant.dcrating is not None:
                    dcList.append( KpiTimeseriesElement(plant.id,plant.activationdate,plant.dcrating,1) )
                if plant.storageoriginalcapacity is not None:
                    storCapList.append( KpiTimeseriesElement(plant.id,plant.activationdate,plant.storageoriginalcapacity,1) )
                    if plant.storagecurrentcapacity is not None:
                        storSOHList.append( KpiTimeseriesElement(plant.id,plant.activationdate,plant.storagecurrentcapacity,plant.storageoriginalcapacity) )
        except:
            print "ERROR reading plant dcrating or storagecapacity"
            return None

        # Fill in the plant-related KPIs
        result = collections.defaultdict(dict)

        # 1. DC Power Rating (rated DC power)
        result['DCRating'] = KPIs.buildKpi(self,dcList,'DCRating')

        # 2. Storage Capacity
        result['StorageCapacity'] = KPIs.buildKpi(self,storCapList,'StorageCapacity')

        # 3. Storage State of Health
        result['StorageStateOfHealth'] = KPIs.buildKpi(self,storSOHList,'StorageStateOfHealth')

        return result

    def calculateTimeseriesKPIs(self,plants,timeseries):

        # First, get a list of each element that will contribute to each KPI
        # We get a separate list per KPI because not all time series elements contain all measurements
        ghiList = list()
        whList = list()
        yfList = list()
        yrList = list()

        try:
            for entry in timeseries:
                if entry.GHI_DIFF is not None:
                    ghiList.append( KpiTimeseriesElement(entry.plant_id,entry.timestamp.date(),entry.GHI_DIFF,1) )
                if entry.WH_DIFF is not None:
                    whList.append( KpiTimeseriesElement(entry.plant_id,entry.timestamp.date(),entry.WH_DIFF,1) )
                    dcrating = KPIs.findPlantsDcrating(self,plants,entry.plant_id)
                    yfList.append( KpiTimeseriesElement(entry.plant_id,entry.timestamp.date(),entry.WH_DIFF,dcrating) )
                if entry.HPOA_DIFF is not None:
                    yrList.append( KpiTimeseriesElement(entry.plant_id,entry.timestamp.date(),entry.HPOA_DIFF,1000) )
        except:
            print "ERROR building kpi lists"
            return None

        result = collections.defaultdict(dict)

        # 1. GHI (daily insolation)
        result['MonthlyInsolation'] = KPIs.buildKpi(self,ghiList,'MonthlyInsolation')

        # 2. WH (daily generated energy)
        result['MonthlyGeneratedEnergy'] = KPIs.buildKpi(self,whList,'MonthlyGeneratedEnergy')

        # 3. YF (generated yield kWh/kWp)
        result['MonthlyYield'] = KPIs.buildKpi(self,yfList,'MonthlyYield')
        
        # 4. YR (hpoa yield kWh/kWp)
        if len(yrList) > 0:
            denom = KPIs.buildKpi(self,yrList,'')
            result['PerformanceRatio'] = KPIs.divide(self,result['MonthlyYield'],denom)
            result['PerformanceRatio']['name'] = 'PerformanceRatio'

        return result

    def calculateKPIs(self,plants,timeseries):

        plantResult = KPIs.calculatePlantKPIs(self,plants)
        if plantResult == None:
            return None
        timeseriesResult = KPIs.calculateTimeseriesKPIs(self,plants,timeseries)
        if timeseriesResult == None:
            result = dict(plantResult.items())
        else:
            result = dict(plantResult.items() + timeseriesResult.items())

        return result

