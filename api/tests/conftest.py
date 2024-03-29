import os

import factory
import pytest
from rest_framework.test import APIClient


@pytest.fixture(scope="session", autouse=True)
def factories_autodiscover():
    from controllers import factories
    from django.apps import apps

    app_names = [app.name for app in apps.app_configs.values()]
    factories.registry.autodiscover(app_names)


@pytest.fixture
def api_client(client):
    """
    Return an API client without any authentication
    """
    return APIClient()


@pytest.fixture
def factories(db):
    """
    Returns a dict containing all registered factories with keys such as users.User or parts.Part
    """
    from controllers import factories

    for v in factories.registry.values():
        try:
            v._meta.strategy = factory.CREATE_STRATEGY
        except AttributeError:
            # probably not a class based factory
            pass
    yield factories.registry


@pytest.fixture
def nodb_factories():
    """
    Returns a dictionnary containing all registered factories with a build strategy
    that does not require access to the database
    """
    from controllers import factories

    for v in factories.registry.values():
        try:
            v._meta.strategy = factory.BUILD_STRATEGY
        except AttributeError:
            # probably not a class based factory
            pass
    yield factories.registry


@pytest.fixture
def logged_in_client(db, factories, client):
    """
    Returns a logged-in, non-API client with an authenticated ``User`` stored in the ``user`` attribute
    """
    user = factories["users.User"]()
    assert client.login(username=user.username, password="test")
    setattr(client, "user", user)
    yield client
    delattr(client, "user")


@pytest.fixture
def logged_in_api_client(db, factories, api_client):
    """
    Return a logged-in API client with an authenticated ``User`` stored in the ``user`` attribute
    """
    user = factories["users.User"]()
    assert api_client.login(username=user.username, password="test")
    api_client.force_authenticate(user=user)
    setattr(api_client, "user", user)
    yield api_client
    delattr(api_client, "user")


@pytest.fixture
def image_file():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../setup-data/manufacturers/images/")
    path = os.path.join(data_dir, "st.png")
    assert os.path.exists(path)
    with open(path, "rb") as f:
        yield f
