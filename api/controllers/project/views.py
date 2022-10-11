from rest_framework import filters, views, mixins
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from datetime import datetime
from controllers.app.renderers import PlainTextRenderer
from rest_framework_csv.renderers import CSVRenderer
from drf_excel.renderers import XLSXRenderer
import urllib
import json
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from controllers.project.models import Project, ProjectAttachment, ProjectPart
from controllers.project.serializers import (
    ProjectPartSerializer,
    ProjectPartStandaloneSerializer,
    ProjectRetrieveSerializer,
    ProjectSerializer,
    ProjectAttachmentsCreateSerializer,
)


class ProjectViewSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "size"


class PrimeVuePagination(LimitOffsetPagination):
    limit_query_param = "rows"
    offset_query_param = "first"


class ProjectsViewSet(ModelViewSet):
    """
    Projects
    """

    anonymous_policy = True
    required_scope = {
        "retrieve": None,
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": None,
    }
    filter_backends = [filters.SearchFilter]
    pagination_class = PrimeVuePagination
    lookup_fields = ("id",)
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
        filters = self.request.query_params.get("filters", None)
        sortField = self.request.query_params.get("sortField", None)
        sortOrder = self.request.query_params.get("sortOrder", None)

        queryset = Project.objects.all()

        # Filtering
        # See in controllers/part/views.py class PartViewSet for documentation on the PrimeVue pagination/sorting
        if filters:
            filters = json.loads(filters)
            for field in ["name", "state"]:
                # not implemented: in, between, and dates
                if filters[field]["value"] is not None:
                    if filters[field]["matchMode"] == "startsWith":
                        queryset = queryset.filter(**{f"{field}__istartswith": filters[field]["value"]})
                    elif filters[field]["matchMode"] == "contains":
                        queryset = queryset.filter(**{f"{field}__icontains": filters[field]["value"]})
                    elif filters[field]["matchMode"] == "notContains":
                        queryset = queryset.exclude(**{f"{field}__icontains": filters[field]["value"]})
                    elif filters[field]["matchMode"] == "endsWith":
                        queryset = queryset.filter(**{f"{field}__iendswith": filters[field]["value"]})
                    elif filters[field]["matchMode"] == "equals":
                        queryset = queryset.filter(**{field: filters[field]["value"]})
                    elif filters[field]["matchMode"] == "notEquals":
                        queryset = queryset.exclude(**{field: filters[field]["value"]})
                    elif filters[field]["matchMode"] == "lt":
                        queryset = queryset.filter(**{f"{field}__lt": filters[field]["value"]})
                    elif filters[field]["matchMode"] == "lte":
                        queryset = queryset.filter(**{f"{field}__lte": filters[field]["value"]})
                    elif filters[field]["matchMode"] == "gt":
                        queryset = queryset.filter(**{f"{field}__gt": filters[field]["value"]})
                    elif filters[field]["matchMode"] == "gte":
                        queryset = queryset.filter(**{f"{field}__gte": filters[field]["value"]})

        if sortField and sortOrder:
            if sortOrder == 1:
                queryset = queryset.order_by(sortField)
            else:
                # -1
                queryset = queryset.order_by(f"-{sortField}")

        # And finally, auth
        if self.request.user.is_anonymous:
            queryset = queryset.filter(public=True)

        return queryset


class ProjectAttachmentsStandalone(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Project attachments (standalone)
    """

    required_scope = "projects"
    anonymous_policy = False

    serializer_class = ProjectAttachmentsCreateSerializer

    def post(self, request, project_id, format=None):
        serializer = ProjectAttachmentsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, project_id, pk, format=None):
        attachment = get_object_or_404(ProjectAttachment, id=pk)
        attachment.delete()
        return Response(status=204)

    def get_queryset(self):
        queryset = ProjectAttachment.objects.all()
        return queryset


class ProjectPartsStandalone(views.APIView):
    """
    Project parts (standalone)
    """

    required_scope = "projects"
    anonymous_policy = False

    http_method_names = ["post", "delete"]

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
    """
    Export project infos (text)
    """

    # Auth is handled in get()
    permission_classes = (AllowAny,)

    http_method_names = ["get"]

    renderer_classes = [PlainTextRenderer]

    @extend_schema(responses=bytes)
    def get(self, request, project_id, format=None):
        if self.request.user.is_anonymous:
            project = get_object_or_404(Project, id=project_id, public=True)
        else:
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
    """
    Export project BOM (csv)
    """

    # Auth is handled in get()
    permission_classes = (AllowAny,)

    http_method_names = ["get"]

    renderer_classes = [CSVRenderer]

    # def get_renderer_context(self):
    #     context = super().get_renderer_context()
    #     context['header'] = ('id', 'part.id', 'part_name',)
    #     return context

    @extend_schema(responses=bytes)
    def get(self, request, project_id, format=None):
        if self.request.user.is_anonymous:
            project = get_object_or_404(Project, id=project_id, public=True)
        else:
            project = get_object_or_404(Project, id=project_id)
        serializer = ProjectPartSerializer(project.project_parts, many=True)
        return Response(serializer.data)


class ExportBomXLSX(GenericAPIView):
    """
    Export project BOM (Excel)
    """

    # Auth is handled in get()
    permission_classes = (AllowAny,)

    http_method_names = ["get"]

    renderer_classes = [XLSXRenderer]

    serializer_class = ProjectPartSerializer

    @extend_schema(responses=bytes)
    def get(self, request, project_id, format=None):
        if self.request.user.is_anonymous:
            project = get_object_or_404(Project, id=project_id, public=True)
        else:
            project = get_object_or_404(Project, id=project_id)
        serializer = ProjectPartSerializer(project.project_parts, many=True)
        filename = f"{urllib.parse.quote(project.name)}.xlsx"
        r = Response(serializer.data)
        r["Content-Disposition"] = f"attachment; filename={filename}"
        return r
