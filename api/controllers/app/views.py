from rest_framework import views
from rest_framework.response import Response
from django.conf import settings
from controllers import __version__
from controllers.part.models import Part
from controllers.categories.models import Category


class AppSettings(views.APIView):
    required_scope = "app"
    anonymous_policy = True

    def get(self, request, *args, **kwargs):
        if self.request.auth:
            parts_uncategorized_count = Part.objects.filter(category_id__isnull=True).values("id").count()
        else:
            parts_uncategorized_count = (
                Part.objects.filter(category_id__isnull=True, private=False).values("id").count()
            )

        data = {
            "version": __version__,
            "part_attachment_allowed_types": settings.PART_ATTACHMENT_ALLOWED_TYPES,
            "pagination": settings.PAGINATION,
            "parts_uncategorized_count": parts_uncategorized_count,
        }
        return Response(data, status=200)


class AppInformations(views.APIView):
    required_scope = "app"
    anonymous_policy = True

    def get(self, request, *args, **kwargs):
        data = {
            "parts_count": Part.objects.values("id").count(),
            "categories_count": Category.objects.count(),
            "version": __version__,
        }
        return Response(data, status=200)
