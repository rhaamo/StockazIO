import os
import urllib.parse
import requests
import html

from django import urls, http
from django.conf import settings
from django.core.cache import caches

from . import utils

EXCLUDED_PATHS = ["/api", "/admin", "/oauth", "/silk", "/static", "/media"]


def should_fallback_to_spa(path):
    if path == "/":
        return True
    return not any([path.startswith(m) for m in EXCLUDED_PATHS])


def get_spa_file(spa_url, name):
    if spa_url.startswith("/") or spa_url.startswith("../"):
        # spa_url is an absolute path to index.html, on the local disk.
        # However, we may want to access manifest.json or other files as well, so we
        # strip the filename
        path = os.path.join(os.path.dirname(spa_url), name)
        # we try to open a local file
        with open(path, "rb") as f:
            return f.read().decode("utf-8")
    cache_key = f"spa-file:{spa_url}:{name}"
    cached = caches["local"].get(cache_key)
    if cached:
        return cached

    response = requests.Session().get(
        utils.join_url(spa_url, name),
    )
    response.raise_for_status()
    content = response.text
    caches["local"].set(cache_key, content, settings.STOCKAZIO_SPA_HTML_CACHE_DURATION)
    return content


def get_spa_html(spa_url):
    return get_spa_file(spa_url, "index.html")


def serve_spa(request):
    html = get_spa_html(settings.STOCKAZIO_SPA_HTML_ROOT)
    head, tail = html.split("</head>", 1)

    final_tags = {}

    # let's inject our meta tags in the HTML
    head += "\n" + "\n".join(render_tags(final_tags)) + "\n</head>"

    return http.HttpResponse(head + tail)


def render_tags(tags):
    """
    Given a dict like {'tag': 'meta', 'hello': 'world'}
    return a html ready tag like
    <meta hello="world" />
    """
    for tag in tags:

        yield "<{tag} {attrs} />".format(
            tag=tag.pop("tag"),
            attrs=" ".join(['{}="{}"'.format(a, html.escape(str(v))) for a, v in sorted(tag.items()) if v]),
        )


class ApiRedirect(Exception):
    def __init__(self, url):
        self.url = url


class SPAFallbackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404 and should_fallback_to_spa(request.path):
            try:
                return serve_spa(request)
            except ApiRedirect as e:
                return get_api_response(request, e.url)

        return response


def get_api_response(request, url):
    """
    Quite ugly but we have no choice. When Accept header is set to application/activity+json
    some clients expect to get a JSON payload (instead of the HTML we return). Since
    redirecting to the URL does not work (because it makes the signature verification fail),
    we grab the internal view corresponding to the URL, call it and return this as the
    response
    """
    path = urllib.parse.urlparse(url).path

    try:
        match = urls.resolve(path)
    except urls.exceptions.Resolver404:
        return http.HttpResponseNotFound()
    response = match.func(request, *match.args, **match.kwargs)
    if hasattr(response, "render"):
        response.render()
    return response
