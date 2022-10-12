import json

from oauth2_provider.oauth2_backends import OAuthLibCore


class JsonAndHtml(OAuthLibCore):
    """
    Extends the default OAuthLibCore to properly handle both JSON and classic HTML
    """

    def extract_body(self, request):
        """
        Extracts the JSON body from the Django request object
        :param request: The current django.http.HttpRequest object
        :return: provided POST parameters "urlencodable"
        """
        try:
            body = json.loads(request.body.decode("utf-8")).items()
        except AttributeError:
            body = request.POST.items()
        except ValueError:
            body = request.POST.items()

        return body
