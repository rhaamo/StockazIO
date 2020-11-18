from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, views
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Project, ProjectAttachment, ProjectPart
from .serializers import (
    ProjectPartStandaloneSerializer,
    ProjectRetrieveSerializer,
    ProjectSerializer,
    ProjectAttachmentsSerializer,
)


class ProjectViewSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"


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

    def post(self, request, project_id, format=None):
        serializer = ProjectPartStandaloneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, project_id, pk, format=None):
        attachment = get_object_or_404(ProjectPart, id=pk)
        attachment.delete()
        return Response(status=204)
