from rest_framework.routers import DefaultRouter
from osparc.views import PlantTypeViewSet,PlantViewSet,StorageSystemViewSet,PVArrayViewSet

router = DefaultRouter(trailing_slash=False)

router.register(prefix='api/planttypes', viewset=PlantTypeViewSet)
router.register(prefix='api/plants', viewset=PlantViewSet)
router.register(prefix='api/storagesystems', viewset=StorageSystemViewSet)
router.register(prefix='api/pvarrays', viewset=PVArrayViewSet)

urlpatterns = router.urls

# router.register(r'planttypes', views.PlantTypeViewSet)
# router.register(r'plants', views.PlantViewSet)
# router.register(r'storagesystems', views.StorageSystemViewSet)

# urlpatterns = [
#     url(r'^api/', include(router.urls)),
#     url(r'^docs/', include('rest_framework_docs.urls'))
# ]
