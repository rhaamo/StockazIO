from rest_framework import views
from rest_framework.response import Response
from django.conf import settings
from controllers import __version__


class AppSettings(views.APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        data = {
            "version": __version__,
            "part_attachment_allowed_types": settings.PART_ATTACHMENT_ALLOWED_TYPES,
            "pagination": settings.PAGINATION,
        }
        return Response(data, status=200)
