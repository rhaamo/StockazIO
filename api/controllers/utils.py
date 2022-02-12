import re

from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.urls import re_path
from django.views.static import serve
from rest_framework import serializers


def join_url(start, end):
    if end.startswith("http://") or end.startswith("https://"):
        # alread a full URL, joining makes no sense
        return end
    if start.endswith("/") and end.startswith("/"):
        return start + end[1:]

    if not start.endswith("/") and not end.startswith("/"):
        return start + "/" + end

    return start + end


# We always serve static, even in production, sorry for the best practices...
def static(prefix, view=serve, **kwargs):
    """
    Return a URL pattern for serving files in debug mode.
    from django.conf import settings
    from controllers.utils import static
    urlpatterns = [
        # ... the rest of your URLconf goes here ...
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    """
    if not prefix:
        raise ImproperlyConfigured("Empty static prefix not permitted")
    return [
        re_path(r"^%s(?P<path>.*)$" % re.escape(prefix.lstrip("/")), view, kwargs=kwargs),
    ]


# Fix from https://github.com/axnsan12/drf-yasg/issues/632
class RecursiveField(serializers.BaseSerializer):
    def to_representation(self, value):
        depth = self.context.get("depth", 0)
        self.context["depth"] = depth + 1
        ParentSerializer = self.parent.parent.__class__
        serializer = ParentSerializer(value, context=self.context, depth=self.context["depth"])

        return serializer.data

    def to_internal_value(self, data):
        ParentSerializer = self.parent.parent.__class__
        Model = ParentSerializer.Meta.model
        try:
            instance = Model.objects.get(pk=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Objeto {0} does not exists".format(Model().__class__.__name__))
        return instance
