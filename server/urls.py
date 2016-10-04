from rest_framework.routers import DefaultRouter
from osparc.views import AccountViewSet,UploadActivityViewSet,PlantTypeViewSet,PlantViewSet
from osparc.views import PlantTimeSeriesViewSet
from django.conf.urls import url, include
from osparc.views import schema_view

router = DefaultRouter(trailing_slash=False)

router.register(prefix='accounts', viewset=AccountViewSet)
router.register(prefix='uploadactivities', viewset=UploadActivityViewSet)
router.register(prefix='planttypes', viewset=PlantTypeViewSet)
router.register(prefix='plants', viewset=PlantViewSet)
router.register(prefix='planttimeseries', viewset=PlantTimeSeriesViewSet)

urlpatterns = router.urls

urlpatterns = [
	url('^api/',include(router.urls)),
	url('^docs/',schema_view)
]

# urlpatterns = [
#     url(r'^api/', include(router.urls)),
#     url(r'^docs/', include('rest_framework_docs.urls'))
# ]
