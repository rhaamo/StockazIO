from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from controllers.part.models import Part
from controllers.part.forms import PartForm
from controllers.categories.models import Category
from controllers.distributor.models import DistributorSku
from controllers.distributor.forms import DistributorSkuForm

from django.forms.models import inlineformset_factory


@login_required
def part_list(request, category=None, template_name="parts/part_list.html"):
    sort = request.GET.get("sort", "name")
    page = request.GET.get("page", 1)
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

    ctx["object_list"] = base_queryset.order_by(ctx["sort_by"])
    paginator = Paginator(ctx["object_list"], settings.PAGINATION["PARTS"])
    ctx["paginator"] = paginator.page(page)
    ctx["page"] = page
    if category:
        ctx["category"] = cat
        ctx["category_path"] = cat.__str__().split("->")

    return render(request, template_name, ctx)


@login_required
def part_create(request, template_name="parts/part_create.html"):
    form = PartForm(request.POST or None)
    distributor_sku_inline_formset = inlineformset_factory(
        Part, DistributorSku, can_delete=True, extra=1, form=DistributorSkuForm
    )

    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            form.save_m2m()
            formset = distributor_sku_inline_formset(request.POST, instance=obj)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Part successfully created.")
                return redirect("part_list")
    return render(
        request, template_name, {"form": form, "distributor_sku_inline_formset": distributor_sku_inline_formset}
    )


@login_required
def part_update(request, pk, template_name="parts/part_update.html"):
    part = get_object_or_404(Part, pk=pk)
    form = PartForm(request.POST or None, instance=part)
    if form.is_valid():
        form.save()
        messages.success(request, "Part successfully updated.")
        return redirect("part_list")
    return render(request, template_name, {"form": form, "object": part})
