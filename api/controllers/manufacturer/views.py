from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet

from .forms import ManufacturerForm, ManufacturerLogoFormSet
from .models import Manufacturer
from .serializers import ManufacturersSerializer


@login_required
def manufacturer_list(request, template_name="manufacturers/manufacturer_list.html"):
    sort = request.GET.get("sort", "name")
    page = request.GET.get("page", 1)
    ctx = {}

    if sort == "name":
        ctx["sort_arg"] = "-name"
        ctx["sort_by"] = "name"
    elif sort == "-name":
        ctx["sort_arg"] = "name"
        ctx["sort_by"] = "-name"

    ctx["object_list"] = Manufacturer.objects.prefetch_related("logos").order_by(ctx["sort_by"])
    paginator = Paginator(ctx["object_list"], settings.PAGINATION["MANUFACTURERS"])
    ctx["paginator"] = paginator.page(page)
    ctx["page"] = page

    return render(request, template_name, ctx)


class ManufacturerCreate(SuccessMessageMixin, CreateView):
    model = Manufacturer
    template_name = "manufacturers/manufacturer_create.html"
    form_class = ManufacturerForm
    success_url = reverse_lazy("manufacturer_list")
    success_message = "Manufacturer successfully created."

    def get_context_data(self, **kwargs):
        data = super(ManufacturerCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data["manufacturer_logos"] = ManufacturerLogoFormSet(self.request.POST, self.request.FILES)
        else:
            data["manufacturer_logos"] = ManufacturerLogoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        manufacturer_logos = context["manufacturer_logos"]

        with transaction.atomic():
            # Save without commit
            self.object = form.save()

            # Handle inline forms
            if manufacturer_logos.is_valid():
                manufacturer_logos.instance = self.object
                manufacturer_logos.save()
        return super(ManufacturerCreate, self).form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(ManufacturerCreate, self).dispatch(*args, **kwargs)


class ManufacturerUpdate(SuccessMessageMixin, UpdateView):
    model = Manufacturer
    template_name = "manufacturers/manufacturer_update.html"
    form_class = ManufacturerForm
    success_url = reverse_lazy("manufacturer_list")
    success_message = "Manufacturer successfully updated."

    def get_context_data(self, **kwargs):
        data = super(ManufacturerUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data["manufacturer_logos"] = ManufacturerLogoFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["manufacturer_logos"] = ManufacturerLogoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        manufacturer_logos = context["manufacturer_logos"]

        with transaction.atomic():
            # Save without commit
            self.object = form.save()

            # Handle inline forms
            if manufacturer_logos.is_valid():
                manufacturer_logos.instance = self.object
                manufacturer_logos.save()
        return super(ManufacturerUpdate, self).form_valid(form)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(ManufacturerUpdate, self).dispatch(*args, **kwargs)


class ManufacturersViewSet(ModelViewSet):
    anonymous_policy = True
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": None,
    }
    serializer_class = ManufacturersSerializer

    def get_queryset(self):
        queryset = Manufacturer.objects.all()
        return queryset