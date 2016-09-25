from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class PlantType(models.Model):
    name = models.CharField(unique=True, max_length=45)
    description = models.CharField(max_length=254, blank=True, null=True)

    def __str__(self):
        return self.name

class Plant(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=254, blank=True, null=True)
    activationDate = models.DateField(auto_now_add=True)
    postalCode = models.CharField(max_length=6,default='')
    state = models.CharField(max_length=2,default='')
    county = models.CharField(max_length=32,default='')
    city = models.CharField(max_length=32,default='')
    latitude = models.CharField(max_length=16,default='none')
    longitude = models.CharField(max_length=16,default='none')
    timeZone = models.CharField(max_length=64,default='none')
    def __str__(self):
        return self.name
    # DCOptimized = models.CharField(max_length=32, blank=True, null=True)
    # inverterType = models.CharField(max_length=32, blank=True, null=True)
    # weatherSource = models.CharField(max_length=32, blank=True, null=True)
    # designModel = models.CharField(max_length=32, blank=True, null=True)
    # nominalACPowerRating = models.FloatField(blank=True, null=True)
    # ACCapacity = models.FloatField(blank=True, null=True)
    # DCRating = models.FloatField(blank=True, null=True)
    # derate = models.FloatField(blank=True, null=True)
    # degradationRate = models.FloatField(blank=True, null=True)


"""
    postal = models.CharField(max_length=6)
    size = models.IntegerField(blank=True, null=True)
    type = models.ForeignKey('PlantType', models.SET_NULL, blank=True, null=True)
    analysis_period = models.IntegerField(blank=True, null=True)


    inverter_capacity = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    inverter_replacement_cost = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    inverter_type = models.ForeignKey(InverterType, on_delete=models.CASCADE)
    inverter_warranty = models.IntegerField(blank=True, null=True)
    modules_per_row = models.IntegerField(blank=True, null=True)
    module_encapsulant = models.ForeignKey(ModuleEncapsulant, on_delete=models.CASCADE)
    module_power = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    module_warranty = models.IntegerField(blank=True, null=True)
    module_type = models.ForeignKey(ModuleType, on_delete=models.CASCADE)
    modules_per_string = models.IntegerField(blank=True, null=True)
    no_of_combiner_boxes = models.IntegerField(blank=True, null=True)
    no_of_inverters = models.IntegerField(blank=True, null=True)
    no_of_modules = models.IntegerField(blank=True, null=True)
    no_of_strings = models.IntegerField(blank=True, null=True)
    no_of_transformers = models.IntegerField(blank=True, null=True)
    purchased_monitoring_contract = models.IntegerField(blank=True, null=True)
    rows_per_tracked_block = models.IntegerField(blank=True, null=True)
    site_area = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    strings_per_combiner_box = models.IntegerField(blank=True, null=True)
    truck_rental = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    working_hours = models.IntegerField(blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    costmodel = models.ManyToManyField(Costmodel)
"""

class PVArray(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=254, blank=True, null=True)
    plant = models.ForeignKey(Plant,null=True)
    arrayId = models.IntegerField()
    trackerType = models.CharField(max_length=32)
    tilt = models.IntegerField()
    azimuth = models.IntegerField()
    def __str__(self):
        return self.name
    

class StorageSystem(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=254, blank=True, null=True)
    plant = models.ForeignKey(Plant,null=True)
    activationDate = models.DateField(auto_now_add=True)
    originalCapacity = models.IntegerField(blank=True,null=True)
    currentCapacity  = models.IntegerField(blank=True,null=True)
    stateOfCharge = models.FloatField(blank=True,null=True)
    def __str__(self):
        return self.name

