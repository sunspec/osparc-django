from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from osparc.views import AccountViewSet,UploadActivityViewSet,PlantTypeViewSet,PlantViewSet
from osparc.views import PlantTimeSeriesViewSet
from osparc.views import schema_view, PlantCountView,PlantDCCapacityView

router = DefaultRouter(trailing_slash=False)

router.register(prefix='accounts', viewset=AccountViewSet)
router.register(prefix='uploadactivities', viewset=UploadActivityViewSet)
router.register(prefix='planttypes', viewset=PlantTypeViewSet)
router.register(prefix='plants', viewset=PlantViewSet)
router.register(prefix='planttimeseries', viewset=PlantTimeSeriesViewSet)

urlpatterns = [
	url('^api/plant_count/',PlantCountView.as_view()),
	url('^api/plant_dc_capacity/',PlantDCCapacityView.as_view()),
	url('^api/',include(router.urls)),
	url('^docs/',schema_view)
]
