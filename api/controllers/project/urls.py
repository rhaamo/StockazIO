from controllers.project import views
from rest_framework import routers
from django.urls import path

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
    path(r"<int:project_id>/exports/bom.csv", views.ExportBomCSV.as_view(), name="projects_export_bom_csv"),
    path(r"<int:project_id>/exports/bom.xlsx", views.ExportBomXLSX.as_view(), name="projects_export_bom_xlsx"),
]

# NOTE: router.urls has to be last or it will override the urlpatterns in the lookup order
urlpatterns = urlpatterns + router.urls
