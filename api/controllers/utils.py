import re

from django.core.exceptions import ImproperlyConfigured
from django.urls import re_path
from django.views.static import serve


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
