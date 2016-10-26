from rest_framework import serializers
from osparc import models

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ("accountID","role","name","companyName","companyAddress","companyCityState","companyPostalCode","email","password")

class UploadActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UploadActivity
        fields = ("account","requestTime","responseTime","plantUUID","status","errorDetail","s3Key")

class PlantTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.PlantType
        fields = ("name", "description")

# class ShortListSerializerMixin(object):
#     def get_fields(self):
        
#         use_list_fields = self.context['view'].action == u'list' \
#                             and getattr(self.Meta, 'list_fields')
#         if use_list_fields:
#             detail_fields = self.opts.fields

#             print detail_fields

#             # self.fields = self.Meta.list_fields

#         fields = super(ShortListSerializerMixin, self).get_fields()

#         if use_list_fields:
#             self.fields = detail_fields
#         return fields

class PlantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Plant
        fields = ("uuid","name","activationdate","dcrating","postalcode","state")

class PlantDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plant
        fields = ("description","county","city",
            "latitude","longitude","timezone","weathersource","derate","trackertype","tilt","azimuth",
            "storageoriginalcapacity","storagecurrentcapacity","storagestateofcharge","accountid",
            "versioncreationtime","versionid","solaranywheresite")

# class PlantSummarySerializer(PlantSerializer):
#     def __init__(self,*args,**kwargs):
#         super(PlantSummarySerializer,self).__init__(*args,**kwargs)
#         self.fields.pop("description")
#         self.fields.pop("activationdate")
#         self.fields.pop("postalcode")
#         self.fields.pop("state")
#         self.fields.pop("county")
#         self.fields.pop("city")
#         self.fields.pop("latitude")
#         self.fields.pop("longitude")
#         self.fields.pop("timezone")
#         self.fields.pop("weathersource")
#         self.fields.pop("dcrating")
#         self.fields.pop("derate")
#         self.fields.pop("trackertype")
#         self.fields.pop("tilt")
#         self.fields.pop("azimuth")
#         self.fields.pop("storageoriginalcapacity")
#         self.fields.pop("storagecurrentcapacity")
#         self.fields.pop("storagestateofcharge")
#         self.fields.pop("accountid")
#         self.fields.pop("versioncreationtime")
#         self.fields.pop("versionid")
#         self.fields.pop("solaranywheresite")

#     class Meta:
#         model = models.Plant
#         fields = ("plantuuid","name")

class PlantTimeSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlantTimeSeries
        fields = ("timestamp","sampleinterval","WH_DIFF","GHI_DIFF","TMPAMB_AVG","HPOA_DIFF","plant","recordstatus")

class KPISerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.KPI
        fields = ("name","plants","firstday","lastday","mean","median","minimum","maximum")


class ReportDefinitionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = models.ReportDefinition
        fields = ("id","name","observationstartdate","observationenddate","plantpostalcode",
                "plantstate","plantminsize","plantmaxsize","plantlatestactivationdate")

class ReportRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReportRun
        fields = ("reportdefinition","runsubmittime","runstarttime","runscompletetime","observationstartdate",
                "observationenddate","numberofobservations","numberofplants","totaldccapacity","totalstoragecapacity")



# class KPISerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.KPI
#         fields = ("dcratingplants","dcratingfirstday","dcratinglastday","dcratingmean","dcratingmed","dcratingmin","dcratingmax",
#                   "insolplants","insolfirstday","insollastday","insolmean","insolmed","insolmin","insolmax",
#                   "generatedplants","generatedfirstday","generatedlastday","generatedmean","generatedmed","generatedmin","generatedmax",
#                   "yieldplants","yieldfirstday","yieldlastday","yieldmean","yieldmed","yieldmin","yieldmax",
#                   "prplants","prfirstday","prlastday","prmean","prmed","prmin","prmax",
#                   "storcapplants","storcapfirstday","storcaplastday","storcapmean","storcapmed","storcapmin","storcapmax",
#                   "storsohplants","storsohfirstday","storsohlastday","storsohmean","storsohmed","storsohmin","storsohmax",
#                 )


# class TotalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Total
#         fields = ("totaldcrating","totalstoragecapacity")
