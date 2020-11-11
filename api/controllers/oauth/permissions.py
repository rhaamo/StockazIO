import logging
from rest_framework import permissions
from django.core.exceptions import ImproperlyConfigured

from . import models
from . import scopes

log = logging.getLogger("oauth2_provider")


def normalize(*scope_ids):
    """
    Given an iterable containing scopes ids such as {read, write:playlists}
    will return a set containing all the leaf scopes (and no parent scopes)
    """
    final = set()
    for scope_id in scope_ids:
        try:
            scope_obj = scopes.SCOPES_BY_ID[scope_id]
        except KeyError:
            continue

        if scope_obj.children:
            final = final | {s.id for s in scope_obj.children}
        else:
            final.add(scope_obj.id)
    return final


def should_allow(required_scope, request_scopes):
    if not required_scope:
        return True

    if not request_scopes:
        return False

    return required_scope in normalize(*request_scopes)


METHOD_SCOPE_MAPPING = {
    "get": "read",
    "post": "write",
    "patch": "write",
    "put": "write",
    "delete": "write",
}


class ScopePermission(permissions.BasePermission):
    def has_permission(self, request, view):

        # Allow OPTIONS and HEAD methods
        if request.method.lower() in ["options", "head"]:
            return True

        # Check if required_scope is defined
        try:
            scope_config = getattr(view, "required_scope")
        except AttributeError:
            raise ImproperlyConfigured("ScopePermission requires the view to define the required_scope attribute")

        # Get the Anonymous Policy value and check if valid
        anonymous_policy = getattr(view, "anonymous_policy", False)
        if anonymous_policy not in [True, False]:
            raise ImproperlyConfigured("{} is not a valid value for anonymous_policy".format(anonymous_policy))

        # Generate the right scope_config depending if string or dict
        if isinstance(scope_config, str):
            scope_config = {
                "read": "read:{}".format(scope_config),
                "write": "write:{}".format(scope_config),
            }
            action = METHOD_SCOPE_MAPPING[request.method.lower()]
            required_scope = scope_config[action]
        else:
            # we have a dict with explicit viewset actions / scopes
            if not view.action:
                print("`view.action` is None")
                return False
            required_scope = scope_config[view.action]

        # Fetch token
        token = request.auth

        if isinstance(token, models.AccessToken):
            # Check scopes against token scope
            has_perms = self.has_permission_token(token, required_scope)
            if not has_perms:
                print(f"DENIED, has token; required_scopes={required_scope!r} token={token.scopes.keys()!r}")
            return has_perms
        else:
            # Is it an anonymous policy ?
            if anonymous_policy is False:
                return False

            # Define default anonymous scopes and if the scope are allowed
            user_scopes = getattr(view, "anonymous_scopes", set()) | scopes.ANONYMOUS_SCOPES
            allowed = should_allow(required_scope=required_scope, request_scopes=user_scopes)
            if not allowed:
                print(f"DENIED, no token; required_scopes={required_scope!r}, user_scopes={user_scopes!r}")
            else:
                print(f"ALLOWED, no token; required_scopes={required_scope!r}, user_scopes={user_scopes!r}")
            return allowed

    def has_permission_token(self, token, required_scope):

        if token.is_expired():
            print("TOKEN: expired")
            return False

        # if not token.user:
        #     return False

        token_scopes = set(token.scopes.keys())
        final_scopes = normalize(*token_scopes) & token.application.normalized_scopes & scopes.OAUTH_APP_SCOPES
        print(f"Token scopes: {normalize(*token_scopes)!r}, scopes: {token_scopes!r}")
        print(f"token app normal: {token.application.normalized_scopes!r}")
        print(f"Oauth scopes app: {scopes.OAUTH_APP_SCOPES!r}")
        print(f"Final scopes: {final_scopes!r}")

        print(f"required_scope={required_scope!r} vs request_scopes={final_scopes!r}")
        return should_allow(required_scope=required_scope, request_scopes=final_scopes)
