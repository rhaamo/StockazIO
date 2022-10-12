from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"", views.LabelTemplateViewSet, basename="LabelTemplate")

urlpatterns = router.urls + []
