from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404

from .forms import FootprintCategoryForm, FootprintForm
from .models import FootprintCategory, Footprint


# Footprint Categories
@login_required
def footprint_category_list(request, template_name="footprints/footprint_category_list.html"):
    sort = request.GET.get("sort", "name")
    ctx = {}

    if sort == "name":
        ctx["sort_arg"] = "-name"
        ctx["sort_by"] = "name"
    elif sort == "-name":
        ctx["sort_arg"] = "name"
        ctx["sort_by"] = "-name"

    ctx["object_list"] = (
        FootprintCategory.objects.values("id", "name", "description")
        .annotate(footprints_count=models.Count("footprint"))
        .order_by(ctx["sort_by"])
    )

    return render(request, template_name, ctx)


@login_required
def footprint_category_create(request, template_name="footprints/footprint_category_create.html"):
    form = FootprintCategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Footprint Category successfully created.")
        return redirect("footprint_category_list")
    return render(request, template_name, {"form": form})


@login_required
def footprint_category_update(request, pk, template_name="footprints/footprint_category_update.html"):
    footprint = get_object_or_404(FootprintCategory, pk=pk)
    form = FootprintCategoryForm(request.POST or None, instance=footprint)
    if form.is_valid():
        form.save()
        messages.success(request, "Footprint Category successfully updated.")
        return redirect("footprint_category_list")
    return render(request, template_name, {"form": form, "object": footprint})


# Footprints
@login_required
def footprint_list(request, pk_category, template_name="footprints/footprint_list.html"):
    footprint_category = get_object_or_404(FootprintCategory, pk=pk_category)
    sort = request.GET.get("sort", "name")
    page = request.GET.get("page", 1)
    ctx = {}

    if sort == "name":
        ctx["sort_arg"] = "-name"
        ctx["sort_by"] = "name"
    elif sort == "-name":
        ctx["sort_arg"] = "name"
        ctx["sort_by"] = "-name"

    ctx["object_list"] = footprint_category.footprint_set.order_by(ctx["sort_by"])
    ctx["footprint_category_name"] = footprint_category.name
    ctx["footprint_category_id"] = footprint_category.id
    paginator = Paginator(ctx["object_list"], settings.PAGINATION["FOOTPRINTS"])
    ctx["paginator"] = paginator.page(page)
    ctx["page"] = page

    return render(request, template_name, ctx)


@login_required
def footprint_create(request, pk_category, template_name="footprints/footprint_create.html"):
    footprint_category = get_object_or_404(FootprintCategory, pk=pk_category)
    form = FootprintForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.instance.footprint_id = footprint_category.id
        form.save()
        messages.success(request, "Footprint successfully created.")
        return redirect("footprint_list", pk_category=footprint_category.id)
    ctx = {
        "form": form,
        "footprint_category_name": footprint_category.name,
        "footprint_category_id": footprint_category.id,
    }
    return render(request, template_name, ctx)


@login_required
def footprint_update(request, pk_category, pk, template_name="footprints/footprint_update.html"):
    footprint_category = get_object_or_404(FootprintCategory, pk=pk_category)
    footprint = get_object_or_404(Footprint, pk=pk)
    form = FootprintForm(request.POST or None, instance=footprint)
    if form.is_valid():
        form.instance.footprint_id = footprint_category.id
        form.save()
        messages.success(request, "Footprint successfully updated.")
        return redirect("footprint_list", pk_category=footprint_category.id)
    ctx = {
        "form": form,
        "object": footprint,
        "footprint_category_name": footprint_category.name,
        "footprint_category_id": footprint_category.id,
    }
    return render(request, template_name, ctx)
