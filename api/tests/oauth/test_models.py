import pytest
from controllers.oauth import models
from django import forms


@pytest.mark.parametrize(
    "uri",
    ["urn:ietf:wg:oauth:2.0:oob", "urn:ietf:wg:oauth:2.0:oob:auto", "http://test.com"],
)
def test_redirect_uris_oob(uri, db):
    app = models.Application(redirect_uris=uri)
    assert app.clean() is None


@pytest.mark.parametrize("uri", ["urn:ietf:wg:oauth:2.0:invalid", "noop"])
def test_redirect_uris_invalid(uri, db):
    app = models.Application(redirect_uris=uri)
    with pytest.raises(forms.ValidationError):
        app.clean()
