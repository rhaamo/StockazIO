from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import F
import json

from controllers.categories.models import Category
from controllers.storage.models import StorageLocation
from controllers.part.models import Part, PartUnit, ParametersUnit, PartAttachment, PartParameterPreset

from rest_framework import views
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from rest_framework import serializers
from rest_framework import generics

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


class PrimeVuePagination(LimitOffsetPagination):
    limit_query_param = "rows"
    offset_query_param = "first"


# Query content:
# originalEvent {isTrusted: true}
#               it will also contains {page: 1, first: 20, rows: 20, pageCount: 2} when using the paginator
#
# page 0 will have first 0, page 1 first 20 etc. assumming we have a perPage of 20 (we have)
# first: number  # start at row X
# rows: number  # of rows to return
# pageCount: number
# page: number
#
# LimitOffsetPagination will uses rows (limit) and first (offset)
#
# filters:
#  filters={
#           "name":{"constraints":[{"value":"das","matchMode":"startsWith"}]},
#           "storage.name":{"constraints":[{"value":null,"matchMode":"equals"}]},
#           "stock_qty":{"constraints":[{"value":null,"matchMode":"equals"}]},
#           "footprint.name":{"constraints":[{"value":null,"matchMode":"equals"}]}}
# due to some weirdness of the "menu" type of datatables, and that we have only *one* constraint, the match and value are in constraints[0]
# Filtering will change the value to a value and matchMode to wanted one
# matchMode: startsWith, contains, notContains, endsWith, equals, notEquals, in, between, lt, lte, gt, gte, dateIs, dateIsNot, dateBefore, dateAfter
# Front can request for fields:
# name: startsWith, contains, notContains, endsWith, equals, notEquals
# storage and footprint: equals, notEquals
# qty: equals, lt, lte, gt, gte
# Ordering adds a "sortField" with a sortOrder (1 or -1)


class PartViewSet(ModelViewSet):
    """
    Parts
    """

    anonymous_policy = True
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    filter_backends = [SearchFilter]
    pagination_class = PrimeVuePagination
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
        storage_uuid = self.request.query_params.get("storage_uuid", None)
        qty_type = self.request.query_params.get("qtyType", None)
        sellable = self.request.query_params.get("sellable", None)

        filters = self.request.query_params.get("filters", None)
        sortField = self.request.query_params.get("sortField", None)
        sortOrder = self.request.query_params.get("sortOrder", None)

        queryset = Part.objects.all()

        # category is recursive, thaks to .get_descendants()
        if category_id in ["0", 0]:
            queryset = queryset.filter(category_id__isnull=True)
        elif category_id:
            category = Category.objects.get(id=category_id).get_descendants(include_self=True)
            if category is not None:
                queryset = queryset.filter(category__in=category)

        if storage_uuid:
            queryset = queryset.filter(storage__uuid=storage_uuid)

        if sellable:
            queryset = queryset.filter(can_be_sold=True)

        if qty_type == "qty":
            queryset = queryset.filter(stock_qty=0)

        if qty_type == "qtyMin":
            queryset = queryset.filter(stock_qty__lt=F("stock_qty_min"))

        # Filtering
        if filters:
            filters = json.loads(filters)
            for field in ["name", "storage_id", "stock_qty", "footprint_id"]:
                # not implemented: in, between, and dates
                if filters[field]["value"] is not None:
                    # if field = (storage_id|footprint_id) and value == 0
                    if (field == "storage_id" or field == "footprint_id") and int(filters[field]["value"]) == 0:
                        # They need to have 0 handled properly
                        if filters[field]["matchMode"] == "equals":
                            queryset = queryset.filter(**{f"{field}__isnull": True})
                        elif filters[field]["matchMode"] == "notEquals":
                            queryset = queryset.exclude(**{f"{field}__isnull": True})
                    else:
                        # any other field or value != 0 (for storage and footprint)
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
            serializer = PartRetrieveSerializer(obj, context={"request": request})
            return Response(serializer.data)


class PartQuickAutocompletion(views.APIView):
    """
    Parts name autocompleter
    """

    required_scope = "parts"
    anonymous_policy = False

    @extend_schema(responses={200: PartRetrieveSerializer})
    def get(self, request, *args, **kwargs):
        obj = get_list_or_404(Part, name__iexact=kwargs["name"])
        serializer = PartRetrieveSerializer(obj, many=True)
        return Response(serializer.data, status=200)


class PartAttachmentsStandalone(views.APIView):
    """
    Part attachment (standalone)
    """

    required_scope = "parts"
    anonymous_policy = False

    http_method_names = ["post", "delete"]

    @extend_schema(
        request={
            "multipart/form-data": PartAttachmentCreateSerializer,
        },
    )
    def post(self, request, part_id, format=None):
        serializer = PartAttachmentCreateSerializer(data=request.data)
        # We need at least a file or picture to be uploaded
        if "file" not in request.data and "picture" not in request.data:
            print("no file or picture")
            return Response(serializer.data, status=400)
        if "file" in request.data and "picture" in request.data:
            print("both file and picture")
            return Response(serializer.data, status=400)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    @extend_schema(
        request={
            "pk": PartAttachment,
        },
    )
    def delete(self, request, part_id, pk, format=None):
        attachment = get_object_or_404(PartAttachment, id=pk)
        attachment.delete()
        return Response(status=204)


class PartsPublic(ModelViewSet):
    """
    Public Parts
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

    filter_backends = [SearchFilter]
    pagination_class = PrimeVuePagination
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
        storage_uuid = self.request.query_params.get("storage_uuid", None)
        qty_type = self.request.query_params.get("qtyType", None)
        sellable = self.request.query_params.get("sellable", None)

        filters = self.request.query_params.get("filters", None)
        sortField = self.request.query_params.get("sortField", None)
        sortOrder = self.request.query_params.get("sortOrder", None)

        queryset = Part.objects.all()
        # fixed field for public parts
        queryset = queryset.filter(private=False)

        # category is recursive, thaks to .get_descendants()
        if category_id in ["0", 0]:
            queryset = queryset.filter(category_id__isnull=True)
        elif category_id:
            category = Category.objects.get(id=category_id).get_descendants(include_self=True)
            if category is not None:
                queryset = queryset.filter(category__in=category)

        if storage_uuid:
            queryset = queryset.filter(storage__uuid=storage_uuid)

        if sellable:
            queryset = queryset.filter(can_be_sold=True)

        if qty_type == "qty":
            queryset = queryset.filter(stock_qty=0)

        if qty_type == "qtyMin":
            queryset = queryset.filter(stock_qty__lt=F("stock_qty_min"))

        # Filtering
        if filters:
            filters = json.loads(filters)
            for field in ["name", "storage_id", "stock_qty", "footprint_id"]:
                # not implemented: in, between, and dates
                if filters[field]["value"] is not None:
                    # if field = (storage_id|footprint_id) and value == 0
                    if (field == "storage_id" or field == "footprint_id") and int(filters[field]["value"]) == 0:
                        # They need to have 0 handled properly
                        if filters[field]["matchMode"] == "equals":
                            queryset = queryset.filter(**{f"{field}__isnull": True})
                        elif filters[field]["matchMode"] == "notEquals":
                            queryset = queryset.exclude(**{f"{field}__isnull": True})
                    else:
                        # any other field or value != 0 (for storage and footprint)
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
    """
    Part units
    """

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
    """
    Part parameters units
    """

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
    """
    Part parameters presets
    """

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


class PartAttachmentsSetDefault(generics.CreateAPIView):
    """
    Set part attachment as default
    """

    required_scope = "parts"
    anonymous_policy = False

    http_method_names = ["post"]

    def post(self, request, part_id, pk, format=None):
        attachment = get_object_or_404(PartAttachment, id=pk)

        # Get old default and set to False
        old_default = PartAttachment.objects.all().filter(part_id=part_id, picture_default=True)
        for opa in old_default:
            opa.picture_default = False
            opa.save()

        # Set new default to true
        attachment.picture_default = True
        attachment.save()

        return Response("ok", status=200)


@extend_schema(
    request=inline_serializer(
        name="BulkEditChangeCategory",
        fields={
            "parts": serializers.ListSerializer(child=serializers.IntegerField()),
            "category": serializers.IntegerField(),
        },
    ),
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="BulkEditChangeCategory",
                fields={
                    "message": serializers.CharField(default="ok"),
                    "parts": serializers.ListSerializer(child=serializers.IntegerField()),
                },
            ),
        )
    },
)
class BulkEditChangeCategory(views.APIView):
    """
    Bulk edit: change category
    """

    required_scope = "parts"
    anonymous_policy = False

    def post(self, request, format=None):
        category = get_object_or_404(Category, id=request.data["category"])
        for partId in request.data["parts"]:
            part = get_object_or_404(Part, id=partId)
            part.category = category
            part.save()

        return Response({"message": "ok", "parts": request.data["parts"]}, status=200)


@extend_schema(
    request=inline_serializer(
        name="BulkEditChangeStorageLocation",
        fields={
            "parts": serializers.ListSerializer(child=serializers.IntegerField()),
            "storage_location": serializers.IntegerField(),
        },
    ),
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="BulkEditChangeStorageLocation",
                fields={
                    "message": serializers.CharField(default="ok"),
                    "parts": serializers.ListSerializer(child=serializers.IntegerField()),
                },
            ),
        )
    },
)
class BulkEditChangeStorageLocation(views.APIView):
    """
    Bulk edit: change storage location
    """

    required_scope = "parts"
    anonymous_policy = False

    def post(self, request, format=None):
        if not request.data["storage_location"]:
            storage_location = None
        else:
            storage_location = get_object_or_404(StorageLocation, id=request.data["storage_location"])
        for partId in request.data["parts"]:
            part = get_object_or_404(Part, id=partId)
            part.storage = storage_location
            part.save()

        return Response({"message": "ok", "parts": request.data["parts"]}, status=200)
