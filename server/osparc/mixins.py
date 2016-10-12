import datetime
import sys
import collections
import math

class KpiMixin(object):
    def median(self,lst):
        sortedLst = sorted(lst)
        lstLen = len(lst)
        index = (lstLen - 1) // 2
        if (lstLen % 2):
            return sortedLst[index]
        else:
            return (sortedLst[index] + sortedLst[index + 1])/2.0

    def buildKpi(self,entryList):
        firstEntry = datetime.date.today()
        lastEntry = datetime.datetime.strptime('01012001', '%d%m%Y').date()
        total = 0
        minValue = sys.float_info.max
        maxValue = 0
        valueList = list()
        currentPlant = 0
        numberOfPlants = 0
        for entry in entryList:
            if entry.plantId != currentPlant:
                currentPlant = entry.plantId
                numberOfPlants = numberOfPlants+1 # there are multiple entries from the same plant
            # print( "currentPlant=%d, entry.plantId=%d, numberOfPlants=%d" % (currentPlant,entry.plantId,numberOfPlants))
            if entry.timeStamp.date() < firstEntry:
                firstEntry = entry.timeStamp.date()
            if entry.timeStamp.date() > lastEntry:
                lastEntry = entry.timeStamp.date()
            total += entry.value
            if entry.value < minValue:
                minValue = entry.value
            if entry.value > maxValue:
                maxValue = entry.value
            valueList.append(entry.value)

        kpi = collections.defaultdict(dict)
        kpi['plants'] = numberOfPlants
        kpi['firstDay'] = firstEntry
        kpi['lastDay'] = lastEntry
        kpi['min'] = math.ceil( minValue*10/10 )
        kpi['max'] = math.ceil( maxValue*10/10 )
        kpi['mean'] = math.ceil( (total/len(entryList)*10)/10 )
        kpi['median'] = math.ceil( (KpiMixin.median(self,valueList))*10/10 )

        return kpi

 