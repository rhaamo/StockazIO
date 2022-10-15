from django.urls import path
from rest_framework import routers

from controllers.project import views

router = routers.DefaultRouter()
router.register(r"", views.ProjectsViewSet, basename="Projects")
router.register(
    r"(?P<project_id>[^/.]+)/attachments", views.ProjectAttachmentsStandalone, basename="projects_attachments"
)

urlpatterns = [
    path(r"<int:project_id>/parts/", views.ProjectPartsStandalone.as_view(), name="projects_parts"),
    path(
        r"<int:project_id>/parts/<int:pk>/",
        views.ProjectPartsStandalone.as_view(),
        name="project_part",
    ),
    path(r"<int:project_id>/exports/infos.txt", views.ExportTextInfos.as_view(), name="projects_export_infos"),
]

# NOTE: router.urls has to be last or it will override the urlpatterns in the lookup order
urlpatterns = urlpatterns + router.urls
