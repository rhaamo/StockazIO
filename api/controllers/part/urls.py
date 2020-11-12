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
    ),
    path(r"public/", views.part.PartsPublic.as_view({"get": "list"}), name="parts_public"),
    path(r"public/<str:pk>/", views.part.PartsPublic.as_view({"get": "retrieve"}), name="parts_public_pk"),
]

# NOTE: router.urls has to be last or it will override the urlpatterns in the lookup order
urlpatterns = urlpatterns + router.urls
