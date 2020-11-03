from . import views
from rest_framework import routers
from django.urls import path

router = routers.DefaultRouter()
router.register(r"parameters/units", views.parameters_unit.PartsParametersUnitViewSet, basename="PartsParametersUnit")
router.register(r"units", views.part_unit.PartsUnitViewSet, basename="PartsParametersUnit")
router.register(r"", views.part.PartViewSet, basename="Part")

urlpatterns = [
    path(
        r"autocomplete/quick_by_name/<str:name>",
        views.part.PartQuickAutocompletion.as_view(),
        name="parts_autocompletion",
    )
]

urlpatterns = router.urls + urlpatterns
