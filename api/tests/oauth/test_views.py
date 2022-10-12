from controllers.oauth import models, serializers
from django.urls import reverse

_OAUTH_APPNAME = "Test app"
_OAUTH_CALLBACK = "http://test.app/oauth-callback"
_OAUTH_SCOPES = "read write read:check_oauth_token read:app read:parts write:parts"


def test_apps_post(api_client, db):
    url = reverse("oauth:apps-list")
    data = {
        "name": _OAUTH_APPNAME,
        "redirect_uris": _OAUTH_CALLBACK,
        "scopes": _OAUTH_SCOPES,
    }
    response = api_client.post(url, data)

    assert response.status_code == 201

    app = models.Application.objects.get(name=data["name"])

    assert app.client_type == models.Application.CLIENT_CONFIDENTIAL
    assert app.authorization_grant_type == models.Application.GRANT_PASSWORD
    assert app.redirect_uris == data["redirect_uris"]
    assert response.data == serializers.CreateApplicationSerializer(app).data
    assert app.scope == _OAUTH_SCOPES
    assert app.user is None


def test_apps_post_logged_in_user(logged_in_api_client, db):
    url = reverse("oauth:apps-list")
    data = {
        "name": _OAUTH_APPNAME,
        "redirect_uris": _OAUTH_CALLBACK,
        "scopes": _OAUTH_SCOPES,
    }
    response = logged_in_api_client.post(url, data)

    assert response.status_code == 201

    app = models.Application.objects.get(name=data["name"])

    assert app.client_type == models.Application.CLIENT_CONFIDENTIAL
    assert app.authorization_grant_type == models.Application.GRANT_PASSWORD
    assert app.redirect_uris == data["redirect_uris"]
    assert response.data == serializers.CreateApplicationSerializer(app).data
    assert app.scope == _OAUTH_SCOPES
    assert app.user == logged_in_api_client.user


def test_apps_list_anonymous(api_client, db):
    url = reverse("oauth:apps-list")
    response = api_client.get(url)

    assert response.status_code == 401


# broken oauth
# def test_apps_list_logged_in(factories, logged_in_api_client, db):
#     app = factories["oauth.Application"](user=logged_in_api_client.user)
#     factories["oauth.Application"]()
#     url = reverse("oauth:apps-list")
#     response = logged_in_api_client.get(url)

#     assert response.status_code == 200
#     assert response.data["results"] == [serializers.ApplicationSerializer(app).data]

# broken oauth
# def test_apps_delete_not_owner(factories, logged_in_api_client, db):
#     app = factories["oauth.Application"]()
#     url = reverse("oauth:apps-detail", kwargs={"client_id": app.client_id})
#     response = logged_in_api_client.delete(url)

#     assert response.status_code == 404

# broken oauth
# def test_apps_delete_owner(factories, logged_in_api_client, db):
#     app = factories["oauth.Application"](user=logged_in_api_client.user)
#     url = reverse("oauth:apps-detail", kwargs={"client_id": app.client_id})
#     response = logged_in_api_client.delete(url)

#     assert response.status_code == 204

#     with pytest.raises(app.DoesNotExist):
#         app.refresh_from_db()

# broken oauth
# def test_apps_update_not_owner(factories, logged_in_api_client, db):
#     app = factories["oauth.Application"]()
#     url = reverse("oauth:apps-detail", kwargs={"client_id": app.client_id})
#     response = logged_in_api_client.patch(url, {"name": "Hello"})

#     assert response.status_code == 404

# broken oauth
# def test_apps_update_owner(factories, logged_in_api_client, db):
#     app = factories["oauth.Application"](user=logged_in_api_client.user)
#     url = reverse("oauth:apps-detail", kwargs={"client_id": app.client_id})
#     response = logged_in_api_client.patch(url, {"name": "Hello"})

#     assert response.status_code == 200
#     app.refresh_from_db()

#     assert app.name == "Hello"


def test_apps_get(logged_in_api_client, factories):
    app = factories["oauth.Application"]()
    url = reverse("oauth:apps-detail", kwargs={"client_id": app.client_id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data == serializers.ApplicationSerializer(app).data


def test_apps_get_owner(logged_in_api_client, factories):
    app = factories["oauth.Application"](user=logged_in_api_client.user)
    url = reverse("oauth:apps-detail", kwargs={"client_id": app.client_id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data == serializers.CreateApplicationSerializer(app).data


# TODO: test token, revoke, etc.
