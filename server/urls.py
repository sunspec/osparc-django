from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from osparc import views

router = DefaultRouter(trailing_slash=False)

router.register(prefix='accounts',    viewset=views.AccountViewSet)
router.register(prefix='uploadactivities', viewset=views.UploadActivityViewSet)
router.register(prefix='planttypes',  viewset=views.PlantTypeViewSet)
# router.register(prefix='plants',      viewset = views.PlantViewSet)
router.register(prefix='planttimeseries', viewset=views.PlantTimeSeriesViewSet)

urlpatterns = [
	url('^api/',include(router.urls)),
    url('^api/plants$', views.PlantList.as_view()),
    url('^api/plants/(?P<pk>[0-9]+)$', views.PlantDetail.as_view()),
    url('^api/queries$', views.ReportDefinitionList.as_view()),
    url('^api/queries/(?P<pk>[0-9]+)$', views.ReportDefinitionDetail.as_view()),
    url('^api/reports$', views.ReportRunList.as_view()),
    url('^api/reports/(?P<pk>[0-9]+)$', views.ReportRunDetail.as_view()),
	url('^api/aggregates',views.AggregatesView.as_view()),
	url('^api/kpis/calc',views.KPIsView.as_view()),
	url('^docs/',views.schema_view)
]
