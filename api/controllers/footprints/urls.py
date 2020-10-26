from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", views.FootprintViewSet, basename="Footprint")

urlpatterns = router.urls + []
