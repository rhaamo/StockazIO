
from rest_framework import views
from rest_framework.response import Response
from django.conf import settings
from controllers import __version__
from controllers.part.models import Part
from controllers.categories.models import Category
from drf_spectacular.utils import inline_serializer, extend_schema, OpenApiResponse
from rest_framework import serializers


class AppSettings(views.APIView):
    """
    Return app settings
    """

    required_scope = "app"
    anonymous_policy = True

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="AppSettings",
                    fields={
                        "version": serializers.CharField(default=__version__),
                        "part_attachment_allowed_types": serializers.ListField(default=settings.PART_ATTACHMENT_ALLOWED_FILES + settings.PART_ATTACHMENT_ALLOWED_IMAGES),
                        "pagination": serializers.DictField(default=settings.PAGINATION),
                        "parts_uncategorized_count": serializers.IntegerField(default=1)
                    },
                ),
            )
        }
    )
    def get(self, request, *args, **kwargs):
        if self.request.auth:
            parts_uncategorized_count = Part.objects.filter(category_id__isnull=True).values("id").count()
        else:
            parts_uncategorized_count = (
                Part.objects.filter(category_id__isnull=True, private=False).values("id").count()
            )

        data = {
            "version": __version__,
            "part_attachment_allowed_types": settings.PART_ATTACHMENT_ALLOWED_FILES
            + settings.PART_ATTACHMENT_ALLOWED_IMAGES,
            "pagination": settings.PAGINATION,
            "parts_uncategorized_count": parts_uncategorized_count,
        }
        return Response(data, status=200)


class AppInformations(views.APIView):
    """
    Return some app informations
    """

    required_scope = "app"
    anonymous_policy = True

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="AppInformations",
                    fields={
                        "parts_count": serializers.IntegerField(default=1),
                        "categories_count": serializers.IntegerField(default=1),
                        "version": serializers.CharField(default=__version__),
                    },
                ),
            )
        }
    )
    def get(self, request, *args, **kwargs):
        data = {
            "parts_count": Part.objects.values("id").count(),
            "categories_count": Category.objects.count(),
            "version": __version__,
        }
        return Response(data, status=200)
