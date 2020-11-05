from . import views
from rest_framework import routers
from django.urls import path

router = routers.DefaultRouter()
router.register(r"category_matcher", views.CategoryMatcherViewSet, basename="CategoryMatcher")
router.register(r"", views.OrderViewSet, basename="OrdersImporter")

urlpatterns = [
    path(
        r"category_matcher/batch_update",
        views.CategoryMatcherBatchUpdater.as_view(),
        name="category_matcher_batch_update",
    )
]

urlpatterns = router.urls + urlpatterns
