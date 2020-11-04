from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", views.OrderViewSet, basename="OrdersImporter")

urlpatterns = router.urls + []
