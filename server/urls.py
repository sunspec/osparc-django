from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from osparc import views

router = DefaultRouter(trailing_slash=False)

router.register(prefix='accounts',    viewset=views.AccountViewSet)
router.register(prefix='uploadactivities', viewset=views.UploadActivityViewSet)
router.register(prefix='planttypes',  viewset=views.PlantTypeViewSet)
router.register(prefix='plants',      viewset = views.PlantViewSet)
router.register(prefix='planttimeseries', viewset=views.PlantTimeSeriesViewSet)

urlpatterns = [
	url('^api/',include(router.urls)),
	url('^api/aggregates',views.StatsView.as_view()),
	url('^api/kpis/calc',views.KPIsView.as_view()),
	url('^docs/',views.schema_view)
]
