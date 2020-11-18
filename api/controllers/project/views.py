from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from .models import Project
from .serializers import ProjectRetrieveSerializer, ProjectSerializer


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
            return ProjectSerializer

    def get_queryset(self):
        state = self.request.query_params.get("state", None)

        queryset = Project.objects.all()

        if state:
            queryset = queryset.filter(state=state)

        return queryset
