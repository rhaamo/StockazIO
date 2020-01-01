from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

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
        else:
            base_queryset = base_queryset.filter(name__icontains=q)

    if category:
        cat = get_object_or_404(Category, id=category)
        base_queryset.filter(category=cat)

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
