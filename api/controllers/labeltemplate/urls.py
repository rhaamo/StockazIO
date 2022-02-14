from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", views.LabelTemplateViewSet, basename="LabelTemplate")

urlpatterns = router.urls + []
