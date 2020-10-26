from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"parameters/unit", views.parameters_unit.PartsParametersUnitViewSet, basename="PartsParametersUnit")

urlpatterns = router.urls + []
