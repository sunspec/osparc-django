from rest_framework.routers import DefaultRouter
from osparc.views import PlantTypeViewSet, PlantViewSet

router = DefaultRouter()
router.register(prefix='planttypes', viewset=PlantTypeViewSet)
router.register(prefix='plants', viewset=PlantViewSet)

urlpatterns = router.urls

