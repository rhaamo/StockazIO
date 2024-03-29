from django.urls import path
from rest_framework import routers

from controllers.part import views

router = routers.DefaultRouter()
router.register(r"parameters/units", views.PartsParametersUnitViewSet, basename="PartsParametersUnit")
router.register(r"parameters/presets", views.PartsParametersPresetViewSet, basename="PartsParametersPreset")
router.register(r"units", views.PartsUnitViewSet, basename="PartsUnit")
router.register(r"", views.PartViewSet, basename="Part")
router.register(r"(?P<part_id>[^/.]+)/attachments", views.PartAttachmentsStandalone, basename="PartsAttachment")

urlpatterns = [
    path(r"public/", views.PartsPublic.as_view({"get": "list"}), name="parts_public"),
    path(r"public/<pk>/", views.PartsPublic.as_view({"get": "retrieve"}), name="parts_public_pk"),
    path(
        r"<part_id>/attachments/<int:pk>/set_default",
        views.PartAttachmentsSetDefault.as_view(),
        name="parts_attachments_set_default",
    ),
]

# NOTE: router.urls has to be last or it will override the urlpatterns in the lookup order
urlpatterns = urlpatterns + router.urls
