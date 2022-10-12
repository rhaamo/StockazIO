from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import authentication


# Used for Swagger/Redoc
class BearerAuthentication(authentication.TokenAuthentication):
    """
    Simple token based authentication.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:
    Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = "Bearer"


class BearerSchema(OpenApiAuthenticationExtension):
    target_class = "controller.users.authentication.BearerAuthentication"
    name = "BearerAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Bearer",
            "description": "Bearer token after Oauth2 Auth flow",
        }
