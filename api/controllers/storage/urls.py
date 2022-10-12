from rest_framework import routers

from controllers.storage import views

router = routers.DefaultRouter()
router.register(r"", views.StorageViewSet, basename="Storage")

urlpatterns = router.urls + []
