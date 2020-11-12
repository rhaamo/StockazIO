from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .forms import DistributorForm
from .models import Distributor
from .serializers import DistributorsSerializer


@login_required
def distributor_list(request, template_name="distributors/distributor_list.html"):
    sort = request.GET.get("sort", "name")
    page = request.GET.get("page", 1)
    ctx = {}

    if sort == "name":
        ctx["sort_arg"] = "-name"
        ctx["sort_by"] = "name"
    elif sort == "-name":
        ctx["sort_arg"] = "name"
        ctx["sort_by"] = "-name"

    ctx["object_list"] = Distributor.objects.values("id", "name", "url", "email", "phone").order_by(ctx["sort_by"])
    paginator = Paginator(ctx["object_list"], settings.PAGINATION["DISTRIBUTORS"])
    ctx["paginator"] = paginator.page(page)
    ctx["page"] = page

    return render(request, template_name, ctx)


@login_required
def distributor_create(request, template_name="distributors/distributor_create.html"):
    form = DistributorForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Distributor successfully created.")
        return redirect("distributor_list")
    return render(request, template_name, {"form": form})


@login_required
def distributor_update(request, pk, template_name="distributors/distributor_update.html"):
    distributor = get_object_or_404(Distributor, pk=pk)
    form = DistributorForm(request.POST or None, instance=distributor)
    if form.is_valid():
        form.save()
        messages.success(request, "Distributor successfully updated.")
        return redirect("distributor_list")
    return render(request, template_name, {"form": form, "object": distributor})


class DistributorsViewSet(ModelViewSet):
    anonymous_policy = True
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    serializer_class = DistributorsSerializer

    def get_queryset(self):
        queryset = Distributor.objects.all()
        return queryset
