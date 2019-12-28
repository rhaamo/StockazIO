import django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from controllers.part.models import Part

# Informations
@login_required
def other_informations(request, template_name="other/informations.html"):
    ctx = {"parts_count": Part.objects.values("id").count(), "django_version": django.get_version()}
    return render(request, template_name, ctx)
