import datetime
import sys
import collections

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
                if entry.timeStamp < firstEntry:
                    firstEntry = entry.timeStamp
                if entry.timeStamp > lastEntry:
                    lastEntry = entry.timeStamp
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
        kpi['min'] = round( minValue,1 )
        kpi['max'] = round( maxValue,1 )
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
        kpi['firstDay'] = max( dict1['firstDay'],dict2['firstDay'] )
        kpi['lastDay'] = min( dict1['lastDay'],dict2['lastDay'] )
        kpi['min'] = round(dict1['min'] / dict2['min'],2)
        kpi['max'] = round(dict1['max'] / dict2['max'],2)
        kpi['mean'] = round(dict1['mean'] / dict2['mean'],2)
        kpi['median'] = round(dict1['median'] / dict2['median'],2)
        return kpi


 