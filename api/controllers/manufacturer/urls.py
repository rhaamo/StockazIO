from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"", views.ManufacturersViewSet, basename="Manufacturers")

urlpatterns = router.urls + []
