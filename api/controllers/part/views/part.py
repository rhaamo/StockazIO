from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from controllers.part.models import Part
from controllers.part.forms import PartForm


@login_required
def part_list(request, template_name="parts/part_list.html"):
    sort = request.GET.get("sort", "name")
    page = request.GET.get("page", 1)
    ctx = {}

    if sort == "name":
        ctx["sort_arg"] = "-name"
        ctx["sort_by"] = "name"
    elif sort == "-name":
        ctx["sort_arg"] = "name"
        ctx["sort_by"] = "-name"

    base_queryset = Part.objects.values("id", "name")

    ctx["object_list"] = base_queryset.order_by(ctx["sort_by"])
    paginator = Paginator(ctx["object_list"], settings.PAGINATION["PARTS"])
    ctx["paginator"] = paginator.page(page)
    ctx["page"] = page

    return render(request, template_name, ctx)


@login_required
def part_create(request, template_name="parts/part_create.html"):
    form = PartForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        obj.tags.add(*form.cleaned_data["tags"])
        form.save_m2m()
        messages.success(request, "Part successfully created.")
        return redirect("part_list")
    return render(request, template_name, {"form": form})


@login_required
def part_update(request, pk, template_name="parts/part_update.html"):
    part = get_object_or_404(Part, pk=pk)
    form = PartForm(request.POST or None, instance=part)
    if form.is_valid():
        form.save()
        messages.success(request, "Part successfully updated.")
        return redirect("part_list")
    return render(request, template_name, {"form": form, "object": part})
