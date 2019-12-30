from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from controllers.part.models import Part
from controllers.part.forms import PartForm
from controllers.categories.models import Category

from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db import transaction
from controllers.distributor.forms import DistributorSkuFormSet
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
        base_queryset = Part.objects.prefetch_related("storage", "footprint").filter(category=cat)
    else:
        base_queryset = Part.objects.prefetch_related("storage", "footprint")

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
            data["distributors_sku"] = DistributorSkuFormSet(self.request.POST)
        else:
            data["distributors_sku"] = DistributorSkuFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        distributors_sku = context["distributors_sku"]
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
            data["distributors_sku"] = DistributorSkuFormSet(self.request.POST, instance=self.object)
        else:
            data["distributors_sku"] = DistributorSkuFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        distributors_sku = context["distributors_sku"]
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
        return super(PartUpdate, self).form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(PartUpdate, self).dispatch(*args, **kwargs)
