from django.urls import path
from rest_framework import routers

from controllers.OrdersImporter import views

router = routers.DefaultRouter()
router.register(r"category_matcher", views.CategoryMatcherViewSet, basename="CategoryMatcher")
router.register(r"", views.OrderViewSet, basename="OrdersImporter")

urlpatterns = [
    path(
        r"import_to_inventory",
        views.OrderImporterToInventory.as_view(),
        name="import_to_inventory",
    ),
]

urlpatterns = router.urls + urlpatterns
