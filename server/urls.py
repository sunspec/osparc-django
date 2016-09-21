from rest_framework.routers import DefaultRouter
from osparc.views import PlantTypeViewSet, PlantViewSet, StorageSystemViewSet

router = DefaultRouter()
router.register(prefix='planttypes', viewset=PlantTypeViewSet)
router.register(prefix='plants', viewset=PlantViewSet)
router.register(prefix='storagesystems', viewset=StorageSystemViewSet)

urlpatterns = router.urls

