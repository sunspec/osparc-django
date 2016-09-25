from rest_framework.routers import DefaultRouter
from osparc.views import PlantTypeViewSet,PlantViewSet,StorageSystemViewSet,PVArrayViewSet

router = DefaultRouter(trailing_slash=False)

router.register(prefix='planttypes', viewset=PlantTypeViewSet)
router.register(prefix='plants', viewset=PlantViewSet)
router.register(prefix='storagesystems', viewset=StorageSystemViewSet)
router.register(prefix='pvarrays', viewset=PVArrayViewSet)

urlpatterns = router.urls

# router.register(r'planttypes', views.PlantTypeViewSet)
# router.register(r'plants', views.PlantViewSet)
# router.register(r'storagesystems', views.StorageSystemViewSet)

# urlpatterns = [
#     url(r'^api/', include(router.urls)),
#     url(r'^docs/', include('rest_framework_docs.urls'))
# ]
