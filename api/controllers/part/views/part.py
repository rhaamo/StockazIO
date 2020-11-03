from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import F

from controllers.part.models import Part, PartUnit
from controllers.footprints.models import Footprint
from controllers.storage.models import StorageLocation
from controllers.part.forms import PartForm, PartParameterFormSet, PartQuickAddForm
from controllers.categories.models import Category

from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db import transaction
from controllers.distributor.forms import DistributorSkuFormSet
from controllers.manufacturer.forms import PartManufacturerFormSet
from django.utils.decorators import method_decorator
from .common import query_reverse
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters, views
from rest_framework.response import Response

from controllers.part.serializers import PartSerializer, PartCreateSeralizer, PartRetrieveSerializer


@login_required
def part_list(request, category=None, template_name="parts/part_list.html"):
    sort = request.GET.get("sort", "name")
    page = request.GET.get("page", 1)
    storage_location = request.GET.get("storageLocation", None)
    q = request.GET.get("q", None)
    ctx = {"search_query": q}

    if sort == "name":
        ctx["sort_arg"] = "-name"
        ctx["sort_by"] = "name"
    elif sort == "-name":
        ctx["sort_arg"] = "name"
        ctx["sort_by"] = "-name"

    base_queryset = Part.objects.prefetch_related("storage", "footprint", "part_unit")

    if q:
        if q.startswith("stockazio://storageLocation/"):
            storage_location = q.replace("stockazio://storageLocation/", "")
        elif q.startswith("stockazio://part/"):
            part_id = q.replace("stockazio://part/", "")
            return redirect("part_details", pk=part_id)
        else:
            base_queryset = base_queryset.filter(name__icontains=q)

    if category:
        cat = get_object_or_404(Category, id=category)
        base_queryset = base_queryset.filter(category=cat)

    if storage_location:
        storloc = get_object_or_404(StorageLocation, id=storage_location)
        base_queryset = base_queryset.filter(storage=storloc)
        ctx["storageLocation"] = storloc

    ctx["object_list"] = base_queryset.order_by(ctx["sort_by"])
    paginator = Paginator(ctx["object_list"], settings.PAGINATION["PARTS"])
    ctx["paginator"] = paginator.page(page)
    ctx["page"] = page
    if category:
        ctx["category"] = cat
        ctx["category_path"] = cat.__str__().split("->")

    return render(request, template_name, ctx)


@login_required
def part_details_json(request, pk=None):
    part = get_object_or_404(Part, id=pk)
    return JsonResponse(
        {
            "id": part.id,
            "name": part.name,
            "qty": part.stock_qty,
            "qty-min": part.stock_qty_min,
            "unit": part.part_unit.__str__() if part.part_unit else None,
            "footprint": part.footprint.__str__() if part.footprint else None,
            "description": part.description,
            "storage": part.storage.__str__() if part.storage else None,
            "category": part.category.__str__() if part.category else None,
            "internal-pn": part.internal_part_number,
            "comment": part.comment,
            "production-remarks": part.production_remarks,
            "need-review": part.needs_review,
            "sheet-status": part.status,
            "condition": part.condition,
            "can-be-sold": part.can_be_sold,
            "private": part.private,
            "parameters": [
                {
                    "name": a.name,
                    "description": a.description,
                    "value": a.value,
                    "unit": a.unit.__str__() if a.unit else None,
                }
                for a in part.part_parameters_value.all()
            ],
            "distributors": [
                {
                    "distributor_id": a.distributor.id,
                    "sku": a.sku,
                    "distributor": a.distributor.name,
                    "distributor_www": a.distributor.url if a.distributor else None,
                }
                for a in part.distributors_sku.all()
            ],
            "manufacturers": [
                {
                    "manufacturer_id": a.manufacturer.id if a.manufacturer else None,
                    "sku": a.sku,
                    "manufacturer": a.manufacturer.name if a.manufacturer else None,
                    "manufacturer_www": a.manufacturer.url if a.manufacturer else None,
                }
                for a in part.manufacturers_sku.all()
            ],
        }
    )


@login_required
def part_details(request, pk=None, template_name="parts/part_details.html"):
    part = get_object_or_404(Part, id=pk)

    return render(request, template_name, {"part": part})


class PartQuickAdd(SuccessMessageMixin, CreateView):
    model = Part
    template_name = "parts/part_create.html"
    form_class = PartQuickAddForm
    success_message = "Part successfully created."

    def get_context_data(self, **kwargs):
        data = super(PartQuickAdd, self).get_context_data(**kwargs)
        return data

    def form_valid(self, form):
        with transaction.atomic():
            # Save without commit
            self.object = form.save(commit=False)
            # Fill FKs
            self.object.part_unit = form.cleaned_data["part_unit"]
            self.object.category = form.cleaned_data["category"]
            self.object.footprint = form.cleaned_data["footprint"]
            self.object.storage = form.cleaned_data["storage"]

            # Save for real
            self.object.save()
            form.save_m2m()

        return super(PartQuickAdd, self).form_valid(form)

    def get_success_url(self):
        quack = {
            "part_unit": self.object.part_unit.id if self.object.part_unit else "None",
            "category": self.object.category.id if self.object.category else "None",
            "footprint": self.object.footprint.id if self.object.footprint else "None",
            "storage": self.object.storage.id if self.object.storage else "None",
        }
        return query_reverse("part_quick_add", query=quack)

    def get_initial(self):
        initial = super(PartQuickAdd, self).get_initial()
        # Part unit
        try:
            initial["part_unit"] = PartUnit.objects.get(id=self.request.GET.get("part_unit")).id
        except (AttributeError, PartUnit.DoesNotExist, ValueError):
            pass

        # Category
        try:
            initial["category"] = Category.objects.get(id=self.request.GET.get("category")).id
        except (AttributeError, Category.DoesNotExist, ValueError):
            pass

        # Storage Location
        try:
            initial["storage"] = StorageLocation.objects.get(id=self.request.GET.get("storage")).id
        except (AttributeError, StorageLocation.DoesNotExist, ValueError):
            pass

        # Footprint
        try:
            initial["footprint"] = Footprint.objects.get(id=self.request.GET.get("footprint")).id
        except (AttributeError, Footprint.DoesNotExist, ValueError):
            pass

        return initial

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(PartQuickAdd, self).dispatch(*args, **kwargs)


class PartCreate(SuccessMessageMixin, CreateView):
    model = Part
    template_name = "parts/part_create.html"
    form_class = PartForm
    success_url = reverse_lazy("part_list")
    success_message = "Part successfully created."

    def get_context_data(self, **kwargs):
        data = super(PartCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data["part_parameters"] = PartParameterFormSet(self.request.POST)
            data["distributors_sku"] = DistributorSkuFormSet(self.request.POST)
            data["part_manufacturers"] = PartManufacturerFormSet(self.request.POST)
        else:
            data["part_parameters"] = PartParameterFormSet()
            data["distributors_sku"] = DistributorSkuFormSet()
            data["part_manufacturers"] = PartManufacturerFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        distributors_sku = context["distributors_sku"]
        part_manufacturers = context["part_manufacturers"]
        part_parameters = context["part_parameters"]

        with transaction.atomic():
            # Save without commit
            self.object = form.save(commit=False)
            # Fill FKs
            self.object.part_unit = form.cleaned_data["part_unit"]
            self.object.category = form.cleaned_data["category"]
            self.object.footprint = form.cleaned_data["footprint"]
            self.object.storage = form.cleaned_data["storage"]

            # Save for real
            self.object.save()
            form.save_m2m()

            # Handle inline forms
            if distributors_sku.is_valid():
                distributors_sku.instance = self.object
                distributors_sku.save()
            if part_manufacturers.is_valid():
                part_manufacturers.instance = self.object
                part_manufacturers.save()
            if part_parameters.is_valid():
                part_parameters.instance = self.object
                part_parameters.save()
        return super(PartCreate, self).form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(PartCreate, self).dispatch(*args, **kwargs)


class PartUpdate(SuccessMessageMixin, UpdateView):
    model = Part
    template_name = "parts/part_update.html"
    form_class = PartForm
    success_url = reverse_lazy("part_list")
    success_message = "Part successfully updated."

    def get_context_data(self, **kwargs):
        data = super(PartUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data["part_parameters"] = PartParameterFormSet(self.request.POST, instance=self.object)
            data["distributors_sku"] = DistributorSkuFormSet(self.request.POST, instance=self.object)
            data["part_manufacturers"] = PartManufacturerFormSet(self.request.POST, instance=self.object)
        else:
            data["part_parameters"] = PartParameterFormSet(instance=self.object)
            data["distributors_sku"] = DistributorSkuFormSet(instance=self.object)
            data["part_manufacturers"] = PartManufacturerFormSet(instance=self.object)
        return data

    def get_initial(self):
        initial = super(PartUpdate, self).get_initial()
        # Part unit
        try:
            initial["part_unit"] = self.get_object().part_unit.pk
        except (AttributeError, PartUnit.DoesNotExist):
            pass

        # Category
        try:
            initial["category"] = self.get_object().category.pk
        except (AttributeError, Category.DoesNotExist):
            pass

        # Storage Location
        try:
            initial["storage"] = self.get_object().storage.pk
        except (AttributeError, StorageLocation.DoesNotExist):
            pass

        # Footprint
        try:
            initial["footprint"] = self.get_object().footprint.pk
        except (AttributeError, Footprint.DoesNotExist):
            pass

        return initial

    def form_valid(self, form):
        context = self.get_context_data()
        distributors_sku = context["distributors_sku"]
        part_manufacturers = context["part_manufacturers"]
        part_parameters = context["part_parameters"]

        with transaction.atomic():
            # Save without commit
            self.object = form.save(commit=False)
            # Fill FKs
            self.object.part_unit = form.cleaned_data["part_unit"]
            self.object.category = form.cleaned_data["category"]
            self.object.footprint = form.cleaned_data["footprint"]
            self.object.storage = form.cleaned_data["storage"]

            # Save for real
            self.object.save()
            form.save_m2m()

            # Handle inline forms
            if distributors_sku.is_valid():
                distributors_sku.instance = self.object
                distributors_sku.save()
            if part_manufacturers.is_valid():
                part_manufacturers.instance = self.object
                part_manufacturers.save()
            if part_parameters.is_valid():
                part_parameters.instance = self.object
                part_parameters.save()
        return super(PartUpdate, self).form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(PartUpdate, self).dispatch(*args, **kwargs)


class PartViewSetPagination(PageNumberPagination):
    page_size = settings.PAGINATION["PARTS"]
    page_size_query_param = "page_size"


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
        print(f"action: {self.action}")
        if self.action == "list":
            return PartSerializer
        elif self.action == "retrieve":
            return PartRetrieveSerializer
        else:
            print("using default serializer")
            return PartCreateSeralizer

    def get_queryset(self):
        category_id = self.request.query_params.get("category_id", None)
        footprint_id = self.request.query_params.get("footprint_id", None)
        storage_id = self.request.query_params.get("storage_id", None)
        storage_uuid = self.request.query_params.get("storage_uuid", None)
        qty_type = self.request.query_params.get("qtyType", None)

        queryset = Part.objects.all()

        # category TODO/FIXME: recursivity ?
        if category_id in ["0", 0]:
            queryset = queryset.filter(category_id__isnull=True)
        else:
            category = self.request.query_params.get("category_id", None)
            if category is not None:
                queryset = queryset.filter(category_id=category)

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

        return queryset

    # Allows fetching a part by 'id' or 'uuid'
    def retrieve(self, request, *args, **kwargs):
        if kwargs["pk"].isdigit():
            print("Lookup default")
            # ID
            return super(PartViewSet, self).retrieve(self, *args, **kwargs)
        else:
            print("Lookup by UUID")
            # UUID
            queryset = Part.objects.all()
            obj = get_object_or_404(queryset, uuid=kwargs["pk"])
            serializer = PartRetrieveSerializer(obj)
            return Response(serializer.data)


class PartQuickAutocompletion(views.APIView):
    required_scope = "parts"
    anonymous_policy = False

    def get(self, request, *args, **kwargs):
        obj = get_list_or_404(Part, name=kwargs["name"])
        serializer = PartRetrieveSerializer(obj, many=True)
        return Response(serializer.data, status=200)
