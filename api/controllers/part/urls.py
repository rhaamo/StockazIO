from controllers.part import views
from rest_framework import routers
from django.urls import path

router = routers.DefaultRouter()
router.register(r"parameters/units", views.PartsParametersUnitViewSet, basename="PartsParametersUnit")
router.register(r"parameters/presets", views.PartsParametersPresetViewSet, basename="PartsParametersPreset")
router.register(r"units", views.PartsUnitViewSet, basename="PartsParametersUnit")
router.register(r"", views.PartViewSet, basename="Part")
router.register(r"<int:part_id>/attachments", views.PartAttachmentsStandalone, basename="PartsAttachment")

urlpatterns = [
    path(
        r"autocomplete/quick_by_name/<str:name>",
        views.PartQuickAutocompletion.as_view(),
        name="parts_autocompletion",
    ),
    path(r"bulk/change_category", views.BulkEditChangeCategory.as_view(), name="bulk_edit_change_category"),
    path(
        r"bulk/change_storage_location",
        views.BulkEditChangeStorageLocation.as_view(),
        name="bulk_edit_change_storage_location",
    ),
    path(r"public/", views.PartsPublic.as_view({"get": "list"}), name="parts_public"),
    path(r"public/<str:pk>/", views.PartsPublic.as_view({"get": "retrieve"}), name="parts_public_pk"),
    path(
        r"<int:part_id>/attachments/<int:pk>/set_default",
        views.PartAttachmentsSetDefault.as_view(),
        name="parts_attachments_set_default",
    ),
]

# NOTE: router.urls has to be last or it will override the urlpatterns in the lookup order
urlpatterns = urlpatterns + router.urls
