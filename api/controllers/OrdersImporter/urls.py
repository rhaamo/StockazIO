from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"category_matcher", views.CategoryMatcherViewSet, basename="CategoryMatcher")
router.register(r"", views.OrderViewSet, basename="OrdersImporter")

urlpatterns = [
    path(
        r"category_matcher/batch_update",
        views.CategoryMatcherBatchUpdater.as_view(),
        name="category_matcher_batch_update",
    ),
    path(
        r"category_matcher/rematch",
        views.CategoryMatcherBatchRematcher.as_view(),
        name="category_matcher_rematch",
    ),
    path(
        r"import_to_inventory",
        views.OrderImporterToInventory.as_view(),
        name="import_to_inventory",
    ),
]

urlpatterns = router.urls + urlpatterns
