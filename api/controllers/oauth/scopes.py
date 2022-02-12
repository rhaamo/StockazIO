class Scope:
    def __init__(self, id, label="", children=None):
        self.id = id
        self.label = ""
        self.children = children or []

    def copy(self, prefix):
        return Scope("{}:{}".format(prefix, self.id))


BASE_SCOPES = [Scope("app"), Scope("categories"), Scope("parts"), Scope("projects"), Scope("storages")]

SCOPES = [
    Scope("read", children=[s.copy("read") for s in BASE_SCOPES]),
    Scope("write", children=[s.copy("write") for s in BASE_SCOPES]),
    # TODO FIXME why are thoses four ones required here ?
    Scope("read"),
    Scope("write"),
    Scope("read:check_oauth_token"),
    Scope("admin"),
]


def flatten(*scopes):
    for scope in scopes:
        yield scope
        yield from flatten(*scope.children)


SCOPES_BY_ID = {s.id: s for s in flatten(*SCOPES)}

ANONYMOUS_SCOPES = {"read:app", "read:categories"}

COMMON_SCOPES = ANONYMOUS_SCOPES | {
    "read",
    "write",
    "read:check_oauth_token",
    "read:parts",
    "write:parts",
    "read:projects",
    "write:projects",
    "read:storages",
    "write:storages"
}

OAUTH_APP_SCOPES = COMMON_SCOPES
