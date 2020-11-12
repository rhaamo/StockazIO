from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.viewsets import ModelViewSet

from controllers.part.forms import PartUnitForm
from controllers.part.models import PartUnit
from controllers.part.serializers import PartsUnitSerializer


@login_required
def part_unit_list(request, template_name="part_units/part_unit_list.html"):
    sort = request.GET.get("sort", "name")
    page = request.GET.get("page", 1)
    ctx = {}

    if sort == "name":
        ctx["sort_arg"] = "-name"
        ctx["sort_by"] = "name"
    elif sort == "-name":
        ctx["sort_arg"] = "name"
        ctx["sort_by"] = "-name"

    ctx["object_list"] = PartUnit.objects.values("id", "name", "short_name", "description").order_by(ctx["sort_by"])
    paginator = Paginator(ctx["object_list"], settings.PAGINATION["PART_UNITS"])
    ctx["paginator"] = paginator.page(page)
    ctx["page"] = page

    return render(request, template_name, ctx)


@login_required
def part_unit_create(request, template_name="part_units/part_unit_create.html"):
    form = PartUnitForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Part Unit successfully created.")
        return redirect("part_unit_list")
    return render(request, template_name, {"form": form})


@login_required
def part_unit_update(request, pk, template_name="part_units/part_unit_update.html"):
    part_unit = get_object_or_404(PartUnit, pk=pk)
    form = PartUnitForm(request.POST or None, instance=part_unit)
    if form.is_valid():
        form.save()
        messages.success(request, "Part Unit successfully updated.")
        return redirect("part_unit_list")
    return render(request, template_name, {"form": form, "object": part_unit})


class PartsUnitViewSet(ModelViewSet):
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
