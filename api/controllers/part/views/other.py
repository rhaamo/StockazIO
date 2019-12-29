import django
from django.contrib.auth.decorators import login_required
from controllers.part.models import Part
from django.shortcuts import render, get_object_or_404
from controllers.categories.models import Category
from django.core.paginator import Paginator
from django.conf import settings

# Informations
@login_required
def other_informations(request, template_name="other/informations.html"):
    ctx = {"parts_count": Part.objects.values("id").count(), "django_version": django.get_version()}
    return render(request, template_name, ctx)


# Soldable
def soldable(request, category=None, template_name="other/public_listing.html"):
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
        base_queryset = Part.objects.prefetch_related("storage", "footprint").filter(
            category=cat, can_be_sold=True, private=False
        )
    else:
        base_queryset = Part.objects.prefetch_related("storage", "footprint").filter(can_be_sold=True, private=False)

    ctx["object_list"] = base_queryset.order_by(ctx["sort_by"])
    paginator = Paginator(ctx["object_list"], settings.PAGINATION["PARTS"])
    ctx["paginator"] = paginator.page(page)
    ctx["page"] = page
    ctx["title"] = "Soldable parts"
    if category:
        ctx["category"] = cat
        ctx["category_path"] = cat.__str__().split("->")

    return render(request, template_name, ctx)


# Public
def public(request, category=None, template_name="other/public_listing.html"):
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
        base_queryset = Part.objects.prefetch_related("storage", "footprint").filter(
            category=cat, can_be_sold=True, private=False
        )
    else:
        base_queryset = Part.objects.prefetch_related("storage", "footprint").filter(private=False)

    ctx["object_list"] = base_queryset.order_by(ctx["sort_by"])
    paginator = Paginator(ctx["object_list"], settings.PAGINATION["PARTS"])
    ctx["paginator"] = paginator.page(page)
    ctx["page"] = page
    ctx["title"] = "Public parts"
    if category:
        ctx["category"] = cat
        ctx["category_path"] = cat.__str__().split("->")

    return render(request, template_name, ctx)
