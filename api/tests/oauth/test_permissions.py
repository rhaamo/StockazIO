import pytest

from controllers.oauth import permissions


@pytest.mark.parametrize(
    "required_scope, request_scopes, expected",
    [
        (None, {}, True),
        ("write:parts", {"write"}, True),
        ("write:parts", {"read"}, False),
        ("write:parts", {"read:parts"}, False),
        ("write:parts", {"write:parts"}, True),
        ("read:parts", {"read"}, True),
        ("read:parts", {"write"}, False),
        ("read:parts", {"read:parts"}, True),
        ("read:parts", {"write:parts"}, False),
        ("write:parts", {"write"}, True),
        ("write:parts", {"read:parts"}, False),
        ("write:parts", {"write:parts"}, True),
        ("write:parts", {"write"}, True),
        ("write:parts", {"read:parts"}, False),
        ("write:parts", {"write:parts"}, True),
        ("write:parts", {"write"}, True),
        ("write:parts", {"read:parts"}, False),
        ("write:parts", {"write:parts"}, True),
    ],
)
def test_should_allow(required_scope, request_scopes, expected):
    assert permissions.should_allow(required_scope=required_scope, request_scopes=request_scopes) is expected
