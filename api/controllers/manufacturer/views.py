from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms.models import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ManufacturerForm, ManufacturerLogoForm
from .models import Manufacturer, ManufacturerLogo


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


@login_required
def manufacturer_create(request, template_name="manufacturers/manufacturer_create.html"):
    form = ManufacturerForm(request.POST or None, request.FILES or None)
    ml_formset = modelformset_factory(ManufacturerLogo, form=ManufacturerLogoForm, extra=1)

    if form.is_valid():
        formset = ml_formset(request.POST or None, request.FILES or None)
        form.save()
        for f in formset:
            f.empty_permitted = False
            if f.is_valid() and f.has_changed():
                f.instance.manufacturer_id = form.instance.id
                f.save()
        messages.success(request, "Manufacturer successfully created.")
        return redirect("manufacturer_list")

    formset = ml_formset(queryset=ManufacturerLogo.objects.none())
    return render(request, template_name, {"form": form, "formset": formset})


@login_required
def manufacturer_update(request, pk, template_name="manufacturers/manufacturer_update.html"):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)

    ml_formset = modelformset_factory(ManufacturerLogo, form=ManufacturerLogoForm, extra=1, can_delete=True)

    form = ManufacturerForm(request.POST or None, request.FILES or None, instance=manufacturer)
    formset = ml_formset(request.POST or None, request.FILES or None)

    if form.is_valid() and formset.is_valid():
        form.save()
        # Save new or updated formsets
        for f in formset:
            f.empty_permitted = False
            if f.is_valid() and f.has_changed():
                f.instance.manufacturer_id = manufacturer.id
                f.save()
        # Clear deleted ones
        for form in formset.deleted_forms:
            form.instance.delete()
        messages.success(request, "Manufacturer successfully updated.")
        return redirect("manufacturer_list")

    formset = ml_formset(queryset=ManufacturerLogo.objects.filter(manufacturer=manufacturer.id))
    return render(request, template_name, {"form": form, "object": manufacturer, "formset": formset})
