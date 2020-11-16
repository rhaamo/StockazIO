from controllers.part import views
from rest_framework import routers
from django.urls import path

router = routers.DefaultRouter()
router.register(r"parameters/units", views.PartsParametersUnitViewSet, basename="PartsParametersUnit")
router.register(r"units", views.PartsUnitViewSet, basename="PartsParametersUnit")
router.register(r"", views.PartViewSet, basename="Part")

urlpatterns = [
    path(
        r"autocomplete/quick_by_name/<name>",
        views.PartQuickAutocompletion.as_view(),
        name="parts_autocompletion",
    ),
    path(r"public/", views.PartsPublic.as_view({"get": "list"}), name="parts_public"),
    path(r"public/<str:pk>/", views.PartsPublic.as_view({"get": "retrieve"}), name="parts_public_pk"),
    path(r"<int:part_id>/attachments/", views.PartAttachmentsStandalone.as_view(), name="parts_attachments"),
    path(r"<int:part_id>/attachments/<int:pk>", views.PartAttachmentsStandalone.as_view(), name="parts_attachments"),
]

# NOTE: router.urls has to be last or it will override the urlpatterns in the lookup order
urlpatterns = urlpatterns + router.urls
