from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, views
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from datetime import datetime
from controllers.app.renderers import PlainTextRenderer
from rest_framework_csv.renderers import CSVRenderer
from drf_renderer_xlsx.renderers import XLSXRenderer
import urllib

from .models import Project, ProjectAttachment, ProjectPart
from .serializers import (
    ProjectPartSerializer,
    ProjectPartStandaloneSerializer,
    ProjectRetrieveSerializer,
    ProjectSerializer,
    ProjectAttachmentsSerializer,
)


class ProjectViewSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "size"


class ProjectsViewSet(ModelViewSet):
    anonymous_policy = True
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["name", "state", "public"]
    ordering = ["-created_at"]
    pagination_class = ProjectViewSetPagination
    # ^starts-with, =exact, @FTS, $regex
    search_fields = ["name", "description", "notes"]

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectSerializer
        elif self.action == "retrieve":
            return ProjectRetrieveSerializer
        else:
            return ProjectRetrieveSerializer

    def get_queryset(self):
        state = self.request.query_params.get("state", None)

        queryset = Project.objects.all()

        if state:
            queryset = queryset.filter(state=state)

        return queryset


class ProjectAttachmentsStandalone(views.APIView):
    required_scope = "projects"
    anonymous_policy = False

    def post(self, request, project_id, format=None):
        serializer = ProjectAttachmentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, project_id, pk, format=None):
        attachment = get_object_or_404(ProjectAttachment, id=pk)
        attachment.delete()
        return Response(status=204)


class ProjectPartsStandalone(views.APIView):
    required_scope = "projects"
    anonymous_policy = False

    def post(self, request, project_id, pk=None, format=None):
        if pk:
            project_part = get_object_or_404(ProjectPart, id=pk)
            serializer = ProjectPartStandaloneSerializer(project_part, data=request.data)
        else:
            serializer = ProjectPartStandaloneSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, project_id, pk, format=None):
        attachment = get_object_or_404(ProjectPart, id=pk)
        attachment.delete()
        return Response(status=204)


class ExportTextInfos(views.APIView):
    required_scope = "projects"
    anonymous_policy = False

    renderer_classes = [PlainTextRenderer]

    def get(self, request, project_id, format=None):
        project = get_object_or_404(Project, id=project_id)
        txt = f"""File generated on {datetime.now()}

Name: {project.name}
State: {dict(Project.STATES)[project.state]}
External BOM URL: {project.ibom_url}
Public project: {'yes' if project.public else 'no'}

Description:
{project.description or 'No description'}

Notes:
{project.notes or 'No notes'}
"""
        return Response(txt)


class ExportBomCSV(views.APIView):
    required_scope = "projects"
    anonymous_policy = False

    renderer_classes = [CSVRenderer]

    # def get_renderer_context(self):
    #     context = super().get_renderer_context()
    #     context['header'] = ('id', 'part.id', 'part_name',)
    #     return context

    def get(self, request, project_id, format=None):
        project = get_object_or_404(Project, id=project_id)
        serializer = ProjectPartSerializer(project.project_parts, many=True)
        return Response(serializer.data)


class ExportBomXLSX(views.APIView):
    required_scope = "projects"
    anonymous_policy = False

    renderer_classes = [XLSXRenderer]

    def get(self, request, project_id, format=None):
        project = get_object_or_404(Project, id=project_id)
        serializer = ProjectPartSerializer(project.project_parts, many=True)
        filename = f"{urllib.parse.quote(project.name)}.xlsx"
        r = Response(serializer.data)
        r["Content-Disposition"] = f"attachment; filename={filename}"
        return r
