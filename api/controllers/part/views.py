import json

from django.conf import settings
from django.db.models import F
from django.shortcuts import get_list_or_404, get_object_or_404
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiParameter, OpenApiResponse

from rest_framework import generics, mixins, serializers
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from controllers.categories.models import Category
from controllers.part.models import ParametersUnit, Part, PartAttachment, PartParameter, PartParameterPreset, PartUnit
from controllers.part.serializers import (
    ParametersUnitSerializer,
    PartAttachmentCreateSerializer,
    PartCreateSeralizer,
    PartParametersPresetRetrieveSerializer,
    PartParametersPresetSerializer,
    PartRetrieveSerializer,
    PartSerializer,
    PartsUnitSerializer,
)
from controllers.storage.models import Storage


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
        "autocompletion": "read",
        "bulk_change_storage": "write",
        "bulk_change_category": "write",
        "get_parameters_names": "read",
        "get_parameter_values": "read",
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
        parameter_filters = self.request.query_params.get("parameter_filters", None)
        sortField = self.request.query_params.get("sortField", None)
        sortOrder = self.request.query_params.get("sortOrder", None)

        queryset = Part.objects.all()

        # category is recursive, thaks to .descendants()
        if category_id in ["0", 0]:
            queryset = queryset.filter(category_id__isnull=True)
        elif category_id:
            category = Category.objects.get(id=category_id).descendants(include_self=True)
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

        # Filtering but by part parameter
        if parameter_filters:
            filters = json.loads(parameter_filters)
            for filter in filters:
                # we get: name, matchMode and value
                name = filter["name"]
                value = filter["value"]
                if filter["matchMode"] == "startsWith":
                    queryset = queryset.filter(
                        **{"part_parameters_value__name": name, "part_parameters_value__value__istartswith": value}
                    )
                elif filter["matchMode"] == "contains":
                    queryset = queryset.filter(
                        **{"part_parameters_value__name": name, "part_parameters_value__value__icontains": value}
                    )
                elif filter["matchMode"] == "notContains":
                    queryset = queryset.exclude(
                        **{"part_parameters_value__name": name, "part_parameters_value__value__icontains": value}
                    )
                elif filter["matchMode"] == "endsWith":
                    queryset = queryset.filter(
                        **{"part_parameters_value__name": name, "part_parameters_value__value__iendswith": value}
                    )
                elif filter["matchMode"] == "equals":
                    queryset = queryset.filter(
                        **{"part_parameters_value__name": name, "part_parameters_value__value": value}
                    )
                elif filter["matchMode"] == "notEquals":
                    queryset = queryset.exclude(
                        **{"part_parameters_value__name": name, "part_parameters_value__value": value}
                    )
                elif filter["matchMode"] == "lt":
                    queryset = queryset.filter(
                        **{"part_parameters_value__name": name, "part_parameters_value__value__lt": value}
                    )
                elif filter["matchMode"] == "lte":
                    queryset = queryset.filter(
                        **{"part_parameters_value__name": name, "part_parameters_value__value__lte": value}
                    )
                elif filter["matchMode"] == "gt":
                    queryset = queryset.filter(
                        **{"part_parameters_value__name": name, "part_parameters_value__value__gt": value}
                    )
                elif filter["matchMode"] == "gte":
                    queryset = queryset.filter(
                        **{"part_parameters_value__name": name, "part_parameters_value__value__gte": value}
                    )

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
            queryset = Part.objects.all()
            obj = get_object_or_404(queryset, id=kwargs["pk"])
            serializer = PartRetrieveSerializer(obj, context={"request": request})
            return Response(serializer.data)
        else:
            # UUID
            queryset = Part.objects.all()
            obj = get_object_or_404(queryset, uuid=kwargs["pk"])
            serializer = PartRetrieveSerializer(obj, context={"request": request})
            return Response(serializer.data)

    @extend_schema(
        responses={200: PartRetrieveSerializer},
        parameters=[OpenApiParameter(name="name", type=str, required=True, description="name of the part")],
    )
    @action(
        detail=False,
        methods=["get"],
        url_path=r"autocomplete/quick_by_name",
        url_name="Autocompletion",
    )
    def autocompletion(self, request, *args, **kwargs):
        """
        Part autocompletion
        """
        name = request.query_params.get("name", None)
        obj = get_list_or_404(Part, name__iexact=name)
        serializer = PartRetrieveSerializer(obj, many=True)
        return Response(serializer.data, status=200)

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
    @action(
        detail=False,
        methods=["post"],
        url_path=r"bulk/change_category",
        url_name="Bulk-Change-Category",
    )
    def bulk_change_category(self, request, *args, **kwargs):
        """
        Bulk edit: change category
        """
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
    @action(
        detail=False,
        methods=["post"],
        url_path=r"bulk/change_storage_location",
        url_name="Bulk-Change-Storage",
    )
    def bulk_change_storage(self, request, *args, **kwargs):
        """
        Bulk edit: change storage location
        """
        if not request.data["storage_location"]:
            storage_location = None
        else:
            storage_location = get_object_or_404(Storage, id=request.data["storage_location"])
        for partId in request.data["parts"]:
            part = get_object_or_404(Part, id=partId)
            part.storage = storage_location
            part.save()

        return Response({"message": "ok", "parts": request.data["parts"]}, status=200)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=serializers.ListSerializer(child=serializers.CharField()),
            )
        },
    )
    @action(
        detail=False,
        methods=["get"],
        url_path=r"parameters/get/all_names",
        url_name="Get-Parameters-Names",
        pagination_class=[],
    )
    def get_parameters_names(self, request, *args, **kwargs):
        """
        Get list of all parameters names
        """
        names = PartParameter.objects.order_by().values_list("name", flat=True).distinct()
        return Response(names, status=200)

    @extend_schema(
        parameters=[OpenApiParameter(name="name", type=str, required=True, description="name of the parameter")],
        responses={
            200: OpenApiResponse(
                response=serializers.ListSerializer(child=serializers.CharField()),
            )
        },
    )
    @action(
        detail=False,
        methods=["get"],
        url_path=r"parameters/get/values",
        url_name="Get-Parameter-Values",
        pagination_class=[],
    )
    def get_parameter_values(self, request, *args, **kwargs):
        """
        Get list of all parameters values for a given name
        """
        name = request.query_params.get("name", None)
        values = PartParameter.objects.order_by().values_list("value", flat=True).distinct().filter(name=name)
        return Response(values, status=200)


class PartAttachmentsStandalone(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Part attachment (standalone)
    """

    required_scope = "parts"
    anonymous_policy = False

    serializer_class = PartAttachmentCreateSerializer

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

    def get_queryset(self):
        queryset = PartAttachment.objects.all()
        return queryset


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

        # category is recursive, thaks to .descendants()
        if category_id in ["0", 0]:
            queryset = queryset.filter(category_id__isnull=True)
        elif category_id:
            category = Category.objects.get(id=category_id).descendants(include_self=True)
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
