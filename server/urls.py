from rest_framework.routers import DefaultRouter
from osparc.views import AccountViewSet,UploadActivityViewSet,PlantTypeViewSet,PlantViewSet,StorageSystemViewSet,PVArrayViewSet
from osparc.views import PlantTimeSeriesViewSet,PVArrayTimeSeriesViewSet
from django.conf.urls import url, include
from osparc.views import schema_view

router = DefaultRouter(trailing_slash=False)

router.register(prefix='accounts', viewset=AccountViewSet)
router.register(prefix='uploadactivities', viewset=UploadActivityViewSet)
router.register(prefix='planttypes', viewset=PlantTypeViewSet)
router.register(prefix='plants', viewset=PlantViewSet)
router.register(prefix='storagesystems', viewset=StorageSystemViewSet)
router.register(prefix='pvarrays', viewset=PVArrayViewSet)
router.register(prefix='planttimeseries', viewset=PlantTimeSeriesViewSet)
router.register(prefix='pvarraytimeseries', viewset=PVArrayTimeSeriesViewSet)

urlpatterns = router.urls

urlpatterns = [
	url('^api/',include(router.urls)),
	url('^docs/',schema_view)
]

# urlpatterns = [
#     url(r'^api/', include(router.urls)),
#     url(r'^docs/', include('rest_framework_docs.urls'))
# ]
