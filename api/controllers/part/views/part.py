from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from controllers.part.models import Part
from controllers.part.forms import PartForm, PartParameterFormSet
from controllers.categories.models import Category

from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db import transaction
from controllers.distributor.forms import DistributorSkuFormSet
from controllers.manufacturer.forms import PartManufacturerFormSet
from django.utils.decorators import method_decorator


@login_required
def part_list(request, category=None, template_name="parts/part_list.html"):
    sort = request.GET.get("sort", "name")
    page = request.GET.get("page", 1)
    q = request.GET.get("q", None)
    ctx = {}

    if sort == "name":
        ctx["sort_arg"] = "-name"
        ctx["sort_by"] = "name"
    elif sort == "-name":
        ctx["sort_arg"] = "name"
        ctx["sort_by"] = "-name"

    if category:
        cat = get_object_or_404(Category, id=category)
        base_queryset = Part.objects.prefetch_related("storage", "footprint", "part_unit").filter(category=cat)
    else:
        base_queryset = Part.objects.prefetch_related("storage", "footprint", "part_unit")

    if q:
        base_queryset = base_queryset.filter(name__icontains=q)

    ctx["object_list"] = base_queryset.order_by(ctx["sort_by"])
    paginator = Paginator(ctx["object_list"], settings.PAGINATION["PARTS"])
    ctx["paginator"] = paginator.page(page)
    ctx["page"] = page
    if category:
        ctx["category"] = cat
        ctx["category_path"] = cat.__str__().split("->")

    return render(request, template_name, ctx)


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
        except AttributeError:
            pass

        # Category
        try:
            initial["category"] = self.get_object().category.pk
        except AttributeError:
            pass

        # Storage Location
        try:
            initial["storage"] = self.get_object().storage.pk
        except AttributeError:
            pass

        # Footprint
        try:
            initial["footprint"] = self.get_object().footprint.pk
        except AttributeError:
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
