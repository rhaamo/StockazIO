from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .forms import StorageCategoryForm, StorageForm
from .models import StorageCategory, StorageLocation
from .serializers import StorageSerializer


# Storage Tree
@login_required
def storage_tree(request, template_name="storages/tree.html"):
    ctx = {}
    ctx["storage_categories"] = StorageCategory.objects.prefetch_related(
        "storage_locations", "storage_locations__part_set"
    ).all()

    return render(request, template_name, ctx)


# Storage Categories
@login_required
def storage_category_list(request, template_name="storages/storage_category_list.html"):
    sort = request.GET.get("sort", "name")
    ctx = {}

    if sort == "name":
        ctx["sort_arg"] = "-name"
        ctx["sort_by"] = "name"
    elif sort == "-name":
        ctx["sort_arg"] = "name"
        ctx["sort_by"] = "-name"

    ctx["object_list"] = (
        StorageCategory.objects.all()
        .annotate(storages_count=models.Count("storage_locations"))
        .order_by(ctx["sort_by"])
    )

    return render(request, template_name, ctx)


@login_required
def storage_category_create(request, template_name="storages/storage_category_create.html"):
    form = StorageCategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Storage Category successfully created.")
        return redirect("storage_category_list")
    return render(request, template_name, {"form": form})


@login_required
def storage_category_update(request, pk, template_name="storages/storage_category_update.html"):
    storage = get_object_or_404(StorageCategory, pk=pk)
    form = StorageCategoryForm(request.POST or None, instance=storage)
    if form.is_valid():
        form.save()
        messages.success(request, "Storage Category successfully updated.")
        return redirect("storage_category_list")
    return render(request, template_name, {"form": form, "object": storage})


# Storage locations
@login_required
def storage_list(request, pk_category, template_name="storages/storage_list.html"):
    storage_category = get_object_or_404(StorageCategory, pk=pk_category)
    sort = request.GET.get("sort", "name")
    page = request.GET.get("page", 1)
    ctx = {}

    if sort == "name":
        ctx["sort_arg"] = "-name"
        ctx["sort_by"] = "name"
    elif sort == "-name":
        ctx["sort_arg"] = "name"
        ctx["sort_by"] = "-name"

    ctx["object_list"] = storage_category.storage_locations.order_by(ctx["sort_by"])
    ctx["storage_category_name"] = storage_category.name
    ctx["storage_category_id"] = storage_category.id
    paginator = Paginator(ctx["object_list"], settings.PAGINATION["STORAGES"])
    ctx["paginator"] = paginator.page(page)
    ctx["page"] = page

    return render(request, template_name, ctx)


@login_required
def storage_create(request, pk_category, template_name="storages/storage_create.html"):
    storage_category = get_object_or_404(StorageCategory, pk=pk_category)
    form = StorageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.instance.category_id = storage_category.id
        form.save()
        messages.success(request, "Storage successfully created.")
        return redirect("storage_list", pk_category=storage_category.id)
    ctx = {"form": form, "storage_category_name": storage_category.name, "storage_category_id": storage_category.id}
    return render(request, template_name, ctx)


@login_required
def storage_update(request, pk_category, pk, template_name="storages/storage_update.html"):
    storage_category = get_object_or_404(StorageCategory, pk=pk_category)
    storage = get_object_or_404(StorageLocation, pk=pk)
    form = StorageForm(request.POST or None, instance=storage)
    if form.is_valid():
        form.instance.storage_id = storage_category.id
        form.save()
        messages.success(request, "Storage successfully updated.")
        return redirect("storage_list", pk_category=storage_category.id)
    ctx = {
        "form": form,
        "object": storage,
        "storage_category_name": storage_category.name,
        "storage_category_id": storage_category.id,
    }
    return render(request, template_name, ctx)


class StorageViewSet(ModelViewSet):
    anonymous_policy = True
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    serializer_class = StorageSerializer

    def get_queryset(self):
        queryset = StorageCategory.objects.all()
        queryset = queryset.get_cached_trees()
        return queryset
