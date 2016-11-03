class Plant:
    def __init__(self,id,actdate,dcrating,storageoriginalcapacity,storagecurrentcapacity):
        self.id = id
        self.activationdate = actdate
        self.dcrating = dcrating
        self.storageoriginalcapacity = storageoriginalcapacity
        self.storagecurrentcapacity = storagecurrentcapacity

class PlantTimeSeries:
    def __init__(self,id,timestamp,sampleinterval,WH_DIFF,GHI_DIFF,TMPAMB_AVG,HPOA_DIFF,plant):
        self.timestamp = timestamp
        self.sampleinterval = sampleinterval
        self.WH_DIFF = WH_DIFF
        self.GHI_DIFF = GHI_DIFF
        self.TMPAMB_AVG = TMPAMB_AVG
        self.HPOA_DIFF = HPOA_DIFF
        self.plant = plant

class KpiTimeseriesElement:
    def __init__(self,plantId,timestamp,numerator,denominator):
        # print "KpiTimeseriesElement init: ",plantId,timestamp,numerator,denominator
        self.plantId = plantId
        self.timestamp = timestamp
        self.value = numerator/denominator

