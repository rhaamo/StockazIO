from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"parameters/units", views.parameters_unit.PartsParametersUnitViewSet, basename="PartsParametersUnit")
router.register(r"units", views.part_unit.PartsUnitViewSet, basename="PartsParametersUnit")

urlpatterns = router.urls + []
