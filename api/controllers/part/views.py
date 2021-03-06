from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import F

from controllers.categories.models import Category
from controllers.part.models import Part, PartUnit, ParametersUnit, PartAttachment, PartParameterPreset

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters, views
from rest_framework.response import Response

from controllers.part.serializers import (
    PartSerializer,
    PartCreateSeralizer,
    PartRetrieveSerializer,
    PartsUnitSerializer,
    ParametersUnitSerializer,
    PartAttachmentCreateSerializer,
    PartParametersPresetSerializer,
    PartParametersPresetRetrieveSerializer,
)


class PartViewSetPagination(PageNumberPagination):
    page_size = settings.PAGINATION["PARTS"]
    page_size_query_param = "size"


class PartParametersPresetsViewSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "size"


class PartViewSet(ModelViewSet):
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
    ordering_fields = ["name", "stock_qty", "stock_qty_min", "footprint", "part_unit", "storage"]
    ordering = ["name"]
    pagination_class = PartViewSetPagination
    lookup_fields = ("id", "uuid")
    # ^starts-with, =exact, @FTS, $regex
    search_fields = [
        "name",
        "description",
        "comment",
        "production_remarks",
        "status",
        "condition",
        "internal_part_number",
        "uuid",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return PartSerializer
        elif self.action == "retrieve":
            return PartRetrieveSerializer
        else:
            return PartCreateSeralizer

    def get_queryset(self):
        category_id = self.request.query_params.get("category_id", None)
        footprint_id = self.request.query_params.get("footprint_id", None)
        storage_id = self.request.query_params.get("storage_id", None)
        storage_uuid = self.request.query_params.get("storage_uuid", None)
        qty_type = self.request.query_params.get("qtyType", None)
        sellable = self.request.query_params.get("sellable", None)

        queryset = Part.objects.all()

        # category TODO/FIXME: recursivity ?
        if category_id in ["0", 0]:
            queryset = queryset.filter(category_id__isnull=True)
        elif category_id:
            category = Category.objects.get(id=category_id).get_descendants(include_self=True)
            if category is not None:
                queryset = queryset.filter(category__in=category)

        if footprint_id in ["0", 0]:
            queryset = queryset.filter(footprint_id__isnull=True)
        elif footprint_id:
            queryset = queryset.filter(footprint_id=footprint_id)

        if storage_id in ["0", 0]:
            queryset = queryset.filter(storage_id__isnull=True)
        elif storage_id:
            queryset = queryset.filter(storage_id=storage_id)

        if storage_uuid:
            queryset = queryset.filter(storage__uuid=storage_uuid)

        if qty_type == "qty":
            queryset = queryset.filter(stock_qty=0)

        if qty_type == "qtyMin":
            queryset = queryset.filter(stock_qty__lt=F("stock_qty_min"))

        if sellable:
            queryset = queryset.filter(can_be_sold=True)

        return queryset

    # Allows fetching a part by 'id' or 'uuid'
    def retrieve(self, request, *args, **kwargs):
        if kwargs["pk"].isdigit():
            # ID
            return super(PartViewSet, self).retrieve(self, *args, **kwargs)
        else:
            # UUID
            queryset = Part.objects.all()
            obj = get_object_or_404(queryset, uuid=kwargs["pk"])
            serializer = PartRetrieveSerializer(obj)
            return Response(serializer.data)


class PartQuickAutocompletion(views.APIView):
    required_scope = "parts"
    anonymous_policy = False

    def get(self, request, *args, **kwargs):
        obj = get_list_or_404(Part, name__iexact=kwargs["name"])
        serializer = PartRetrieveSerializer(obj, many=True)
        return Response(serializer.data, status=200)


class PartAttachmentsStandalone(views.APIView):
    required_scope = "parts"
    anonymous_policy = False

    def post(self, request, part_id, format=None):
        serializer = PartAttachmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, part_id, pk, format=None):
        attachment = get_object_or_404(PartAttachment, id=pk)
        attachment.delete()
        return Response(status=204)


class PartsPublic(ModelViewSet):
    anonymous_policy = True
    required_scope = {
        "retrieve": None,
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": None,
    }

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["name", "stock_qty", "stock_qty_min", "footprint", "part_unit", "storage"]
    ordering = ["name"]
    pagination_class = PartViewSetPagination
    lookup_fields = ("id", "uuid")
    # ^starts-with, =exact, @FTS, $regex
    search_fields = [
        "name",
        "description",
        "comment",
        "production_remarks",
        "status",
        "condition",
        "internal_part_number",
        "uuid",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return PartSerializer
        elif self.action == "retrieve":
            return PartRetrieveSerializer
        else:
            return PartSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get("category_id", None)
        footprint_id = self.request.query_params.get("footprint_id", None)
        storage_id = self.request.query_params.get("storage_id", None)
        storage_uuid = self.request.query_params.get("storage_uuid", None)
        qty_type = self.request.query_params.get("qtyType", None)
        sellable = self.request.query_params.get("sellable", None)

        queryset = Part.objects.all()
        # fixed field for public parts
        queryset = queryset.filter(private=False)

        # category TODO/FIXME: recursivity ?
        if category_id in ["0", 0]:
            queryset = queryset.filter(category_id__isnull=True)
        elif category_id:
            category = Category.objects.get(id=category_id).get_descendants(include_self=True)
            if category is not None:
                queryset = queryset.filter(category__in=category)

        if footprint_id:
            queryset = queryset.filter(footprint_id=footprint_id)

        if storage_id:
            queryset = queryset.filter(storage_id=storage_id)

        if storage_uuid:
            queryset = queryset.filter(storage__uuid=storage_uuid)

        if qty_type == "qty":
            queryset = queryset.filter(stock_qty=0)

        if qty_type == "qtyMin":
            queryset = queryset.filter(stock_qty__lt=F("stock_qty_min"))

        if sellable:
            queryset = queryset.filter(can_be_sold=True)

        return queryset

    # Allows fetching a part by 'id' or 'uuid'
    def retrieve(self, request, *args, **kwargs):
        if kwargs["pk"].isdigit():
            # ID
            return super(PartsPublic, self).retrieve(self, *args, **kwargs)
        else:
            # UUID
            queryset = Part.objects.all()
            # fixed field for public parts
            queryset = queryset.filter(private=False)

            obj = get_object_or_404(queryset, uuid=kwargs["pk"])
            serializer = PartRetrieveSerializer(obj)
            return Response(serializer.data)


class PartsUnitViewSet(ModelViewSet):
    anonymous_policy = True
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    serializer_class = PartsUnitSerializer

    def get_queryset(self):
        queryset = PartUnit.objects.all()
        return queryset


class PartsParametersUnitViewSet(ModelViewSet):
    anonymous_policy = True
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    serializer_class = ParametersUnitSerializer

    def get_queryset(self):
        queryset = ParametersUnit.objects.all()
        return queryset


class PartsParametersPresetViewSet(ModelViewSet):
    anonymous_policy = True
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    pagination_class = PartParametersPresetsViewSetPagination
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action == "list":
            return PartParametersPresetRetrieveSerializer
        elif self.action == "retrieve":
            return PartParametersPresetRetrieveSerializer
        else:
            return PartParametersPresetSerializer

    def get_queryset(self):
        queryset = PartParameterPreset.objects.all()
        return queryset
