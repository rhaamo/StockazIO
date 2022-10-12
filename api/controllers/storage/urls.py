from controllers.storage import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", views.StorageViewSet, basename="Storage")

urlpatterns = router.urls + []
