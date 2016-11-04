# XXX TBD TODO Heinosity Alert:
# This, i.e. the script that runs reports, uses models that are very similar, but different,
# from the models used in the django web services.
# They should be combined; meanwhile, tread carefully!

class Plant:
    def __init__(self,id,actdate,dcrating,storageoriginalcapacity,storagecurrentcapacity):
        self.id = id
        self.activationdate = actdate
        self.dcrating = dcrating
        self.storageoriginalcapacity = storageoriginalcapacity
        self.storagecurrentcapacity = storagecurrentcapacity

class PlantTimeSeries:
    def __init__(self,id,timestamp,sampleinterval,WH_DIFF,GHI_DIFF,TMPAMB_AVG,HPOA_DIFF,plant_id):
        self.timestamp = timestamp
        self.sampleinterval = sampleinterval
        self.WH_DIFF = WH_DIFF
        self.GHI_DIFF = GHI_DIFF
        self.TMPAMB_AVG = TMPAMB_AVG
        self.HPOA_DIFF = HPOA_DIFF
        self.plant_id = plant_id    # NB this is the id, not a foreign key to the plant (as in the web services version)

class KpiTimeseriesElement:
    def __init__(self,plantId,timestamp,numerator,denominator):
        # print "KpiTimeseriesElement init: ",plantId,timestamp,numerator,denominator
        self.plantId = plantId
        self.timestamp = timestamp
        self.value = numerator/denominator

