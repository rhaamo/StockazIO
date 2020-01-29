from oauth2_provider import models as oauth2_models
from oauth2_provider import validators as oauth2_validators
from django.db import models


class Application(oauth2_models.AbstractApplication):
    scope = models.TextField(blank=True)

    @property
    def normalized_scopes(self):
        from .oauth import permissions

        raw_scopes = set(self.scope.split(" ") if self.scope else [])
        return permissions.normalize(*raw_scopes)


# oob schemes are not supported yet in oauth toolkit
# (https://github.com/jazzband/django-oauth-toolkit/issues/235)
# so in the meantime, we override their validation to add support
OOB_SCHEMES = ["urn:ietf:wg:oauth:2.0:oob", "urn:ietf:wg:oauth:2.0:oob:auto"]


class CustomRedirectURIValidator(oauth2_validators.RedirectURIValidator):
    def __call__(self, value):
        if value in OOB_SCHEMES:
            return value
        return super().__call__(value)


oauth2_models.RedirectURIValidator = CustomRedirectURIValidator


class Grant(oauth2_models.AbstractGrant):
    pass


class AccessToken(oauth2_models.AbstractAccessToken):
    pass


class RefreshToken(oauth2_models.AbstractRefreshToken):
    pass
