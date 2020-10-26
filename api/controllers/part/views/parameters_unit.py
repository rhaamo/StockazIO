from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.viewsets import ModelViewSet

from controllers.part.forms import ParametersUnitForm
from controllers.part.models import ParametersUnit
from controllers.part.serializers import ParametersUnitSerializer


@login_required
def parameters_unit_list(request, template_name="parameters_units/parameters_unit_list.html"):
    sort = request.GET.get("sort", "name")
    page = request.GET.get("page", 1)
    ctx = {}

    if sort == "name":
        ctx["sort_arg"] = "-name"
        ctx["sort_by"] = "name"
    elif sort == "-name":
        ctx["sort_arg"] = "name"
        ctx["sort_by"] = "-name"

    ctx["object_list"] = ParametersUnit.objects.values("id", "name", "symbol", "prefix", "description").order_by(
        ctx["sort_by"]
    )
    paginator = Paginator(ctx["object_list"], settings.PAGINATION["PARAMETERS_UNITS"])
    ctx["paginator"] = paginator.page(page)
    ctx["page"] = page

    return render(request, template_name, ctx)


@login_required
def parameters_unit_create(request, template_name="parameters_units/parameters_unit_create.html"):
    form = ParametersUnitForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Parameters Unit successfully created.")
        return redirect("parameters_unit_list")
    return render(request, template_name, {"form": form})


@login_required
def parameters_unit_update(request, pk, template_name="parameters_units/parameters_unit_update.html"):
    parameter_unit = get_object_or_404(ParametersUnit, pk=pk)
    form = ParametersUnitForm(request.POST or None, instance=parameter_unit)
    if form.is_valid():
        form.save()
        messages.success(request, "Parameters Unit successfully updated.")
        return redirect("parameters_unit_list")
    return render(request, template_name, {"form": form, "object": parameter_unit})


class PartsParametersUnitViewSet(ModelViewSet):
    anonymous_policy = True
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    serializer_class = ParametersUnitSerializer

    def get_queryset(self):
        queryset = ParametersUnit.objects.all()
        return queryset
