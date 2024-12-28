import csv
import datetime
import io

from django.db.models import Count
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from rest_framework import serializers as drf_serializers, views
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from controllers.categories.models import Category
from controllers.distributor.models import DistributorSku
from controllers.manufacturer.models import PartManufacturer
from controllers.OrdersImporter.models import CategoryMatcher, Item, Order

from controllers.OrdersImporter.serializers import (
    CategoryMatcherCreateSerializer,
    CategoryMatcherSerializer,
    OrderCreateSerializer,
    OrderListSerializer,
    OrderSerializer,
)
from controllers.OrdersImporter.utils import rematch_orders
from controllers.part.models import Part


class PrimeVuePagination(LimitOffsetPagination):
    limit_query_param = "rows"
    offset_query_param = "first"


class OrderViewSet(ModelViewSet):
    """
    Orders importer
    """

    anonymous_policy = False
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
        "import_to_inventory": "write",
    }
    pagination_class = PrimeVuePagination

    def get_serializer_class(self):
        if self.action in ["list"]:
            return OrderListSerializer
        elif self.action in ["retrieve"]:
            return OrderSerializer
        elif self.action in ["update", "partial_update"]:
            return OrderCreateSerializer
        else:
            return OrderCreateSerializer

    def get_queryset(self):
        sortField = self.request.query_params.get("sortField", None)
        sortOrder = self.request.query_params.get("sortOrder", None)

        queryset = Order.objects.all().annotate(items_count=Count("items"))

        if sortField and sortOrder:
            if sortOrder == 1:
                queryset = queryset.order_by(sortField)
            else:
                # -1
                queryset = queryset.order_by(f"-{sortField}")

        return queryset

    @extend_schema(
        request=inline_serializer(
            name="OrderImporterToInventory",
            fields={
                "id": drf_serializers.IntegerField(),
            },
        ),
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="OrderImporterToInventory",
                    fields={
                        "detail": drf_serializers.CharField(default="done"),
                        "stats": inline_serializer(
                            name="OrderImporterToInventoryStats",
                            fields={
                                "created": drf_serializers.IntegerField(),
                                "updated": drf_serializers.IntegerField(),
                            },
                        ),
                    },
                )
            )
        },
    )
    @action(
        detail=True,
        methods=["post"],
        url_path=r"import",
        url_name="Import",
    )
    def import_to_inventory(self, request, pk=None):
        """
        Orders importer to inventory
        """
        if not pk:
            return Response({"detail": "id is missing"}, 503)

        order = get_object_or_404(Order.objects.prefetch_related("items"), id=pk)

        if order.import_state != 1:  # refuse if import state isn't 1/fetched
            return Response({"detail": f"order import state {order.import_state} isn't valid for importing"})

        stats = {"created": 0, "updated": 0}

        for item in order.items.all():
            if item.ignore:
                continue

            # Try to see if we already have an item in db
            try:
                part = Part.objects.get(name=item.mfr_part_number)
            except Part.DoesNotExist:
                part = None

            if part:
                part.stock_qty += item.quantity
                if not part.category:
                    part.category = item.category
                if not part.description:
                    part.description = item.description
                part.save()

                try:
                    manuf_sku = part.manufacturers_sku.get(sku=item.mfr_part_number, manufacturer=item.manufacturer_db)
                except PartManufacturer.DoesNotExist:
                    manuf_sku = PartManufacturer(sku=item.mfr_part_number, manufacturer=item.manufacturer_db, part=part)
                    manuf_sku.save()

                if not manuf_sku:
                    part.manufacturers_sku.add(manuf_sku)

                try:
                    distri_sku = part.distributors_sku.get(sku=item.vendor_part_number, distributor=order.vendor_db)
                except DistributorSku.DoesNotExist:
                    distri_sku = DistributorSku(sku=item.vendor_part_number, distributor=order.vendor_db, part=part)
                    distri_sku.save()

                if not distri_sku:
                    part.distributors_sku.add(distri_sku)

                if not part.footprint:
                    part.footprint = item.footprint_db

                part.save()
                stats["updated"] += 1

                # Also reference the part to the item
                item.part_db = part
                item.new_in_stock = False
                item.save()

            else:
                part = Part(
                    name=item.mfr_part_number,
                    stock_qty=item.quantity,
                    description=item.description,
                    category=item.category,
                    footprint=item.footprint_db,
                )
                part.save()

                manuf_sku = PartManufacturer(sku=item.mfr_part_number, manufacturer=item.manufacturer_db, part=part)
                manuf_sku.save()
                part.manufacturers_sku.add(manuf_sku)

                distri_sku = DistributorSku(sku=item.vendor_part_number, distributor=order.vendor_db, part=part)
                distri_sku.save()
                part.distributors_sku.add(distri_sku)

                part.save()
                stats["created"] += 1

                # Also reference the part to the item
                item.part_db = part
                item.new_in_stock = True
                item.save()

        # finally, set import_state to 2
        order.import_state = 2
        order.save()

        return Response({"detail": "done", "stats": stats})


class CategoryMatcherViewSet(ModelViewSet):
    """
    Categories Matcher
    """

    anonymous_policy = False
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
        "batch_update": "write",
        "rematch": "write",
    }
    serializer_class = CategoryMatcherSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CategoryMatcherCreateSerializer
        else:
            return CategoryMatcherSerializer

    def get_queryset(self):
        queryset = CategoryMatcher.objects.all()
        return queryset

    @extend_schema(
        request=drf_serializers.ListSerializer(
            child=inline_serializer(
                name="CategoryMatcherBatchUpdater",
                fields={
                    "id": drf_serializers.IntegerField(),
                    "regexp": drf_serializers.CharField(),
                    "category": drf_serializers.IntegerField(),
                },
            )
        ),
        responses={200: CategoryMatcherSerializer},
    )
    @action(
        detail=False,
        methods=["patch"],
        url_path=r"batch_update",
        url_name="Batch-Update",
    )
    def batch_update(self, request, *args, **kwargs):
        # update or create
        # Missing elements will be created
        new_items = []
        if len(request.data.get("update", [])) <= 0:
            return Response({"detail": "Not found."}, 404)
        for item in request.data.get("update", []):
            if "id" in item:
                # Update
                db_item = CategoryMatcher.objects.get(id=item["id"])
                if db_item:
                    db_item.regexp = item["regexp"]
                    category = Category.objects.get(id=item["category"])
                    if not category:
                        continue
                    db_item.category = category
                    db_item.save()
            else:
                # Create
                category = Category.objects.get(id=item["category"])
                if not category:
                    continue
                db_item = CategoryMatcher(regexp=item["regexp"], category=category)
                db_item.save()
            new_items.append(db_item)
        # deletes
        for item in request.data.get("delete", []):
            i = CategoryMatcher.objects.get(id=item)
            i.delete()
        serializer = CategoryMatcherSerializer(new_items, many=True)
        return Response(serializer.data, status=200)

    @extend_schema(
        request=drf_serializers.ListSerializer(
            child=inline_serializer(
                name="CategoryMatcherBatchRematcher",
                fields={
                    "id": drf_serializers.IntegerField(),
                    "regexp": drf_serializers.CharField(),
                    "category": drf_serializers.IntegerField(),
                },
            )
        ),
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="CategoryMatcherBatchRematcher", fields={"details": drf_serializers.CharField(default="done")}
                )
            )
        },
    )
    @action(
        detail=False,
        methods=["get"],
        url_path=r"rematch",
        url_name="Rematch",
    )
    def rematch(self, request, *args, **kwargs):
        # fetch orders
        orders = Order.objects.all().filter(import_state=1).prefetch_related("items")
        if not orders:
            return Response({"details": "no orders"}, 200)

        # rematch
        rematch_orders(orders)

        return Response({"detail": "done"})


class LcscCsvImporter(views.APIView):
    """
    LCSC CSV Import endpoint
    """

    anonymous_policy = False
    required_scope = "parts"  # should create a dedicated scope maybe

    http_method_names = ["post"]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="LcscCsvImporter",
                    fields={
                        "parts_count": drf_serializers.FileField(),
                    },
                ),
            )
        }
    )
    def post(self, request):
        if "file" not in request.data:
            return Response(status=400)

        # now uh, process it I guess
        print(request.data)

        order = Order(
            date=datetime.datetime.now(),
            order_number=f"LCSC-{datetime.datetime.now().timestamp()}",
            status="Lossy CSV Import",
            vendor="LCSC",
            import_state=0,
        )
        order.save()

        csv_file = request.FILES["file"]
        csv_file.seek(0)

        csvreader = csv.DictReader(io.StringIO(csv_file.read().decode("utf-8")), delimiter=",")
        for row in csvreader:
            order_item, _ = Item.objects.get_or_create(
                vendor_part_number=row["LCSC Part Number"],
                mfr_part_number=row["Manufacture Part Number"],
                manufacturer=row["Manufacturer"],
                description=row["Description"],
                quantity=row["Order Qty."],
                order=order,
            )

        # Update order and save
        order.import_state = 1  # fetched
        order.save()

        return Response(status=200)
