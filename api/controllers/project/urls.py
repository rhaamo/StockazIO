from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", views.ProjectsViewSet, basename="Projects")

urlpatterns = router.urls + []
