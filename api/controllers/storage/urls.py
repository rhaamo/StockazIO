from controllers.storage import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"category", views.StorageCategoryViewSet, basename="Category")
router.register(r"location", views.StorageLocationViewSet, basename="Location")
router.register(r"", views.StorageViewSet, basename="Storage")

urlpatterns = router.urls + []
