class Scope:
    def __init__(self, id, label="", children=None):
        self.id = id
        self.label = ""
        self.children = children or []

    def copy(self, prefix):
        return Scope("{}:{}".format(prefix, self.id))


BASE_SCOPES = [Scope("app"), Scope("categories")]

SCOPES = [
    Scope("read", children=[s.copy("read") for s in BASE_SCOPES]),
    Scope("write", children=[s.copy("write") for s in BASE_SCOPES]),
    Scope("admin"),
]


def flatten(*scopes):
    for scope in scopes:
        yield scope
        yield from flatten(*scope.children)


SCOPES_BY_ID = {s.id: s for s in flatten(*SCOPES)}

ANONYMOUS_SCOPES = {"read:app", "read:categories"}

LOGGED_IN_SCOPES = ANONYMOUS_SCOPES | {"read", "write"}

OAUTH_APP_SCOPES = ANONYMOUS_SCOPES | {"read", "write"}


def get_from_permissions(**permissions):
    from funkwhale_api.users import models

    final = LOGGED_IN_SCOPES
    for permission_name, value in permissions.items():
        if value is False:
            continue
        config = models.PERMISSIONS_CONFIGURATION[permission_name]
        final = final | config["scopes"]
    return final
