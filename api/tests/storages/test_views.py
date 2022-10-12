from django.urls import reverse


def test_anonymous_can_get_storage_tree(api_client, db, factories):
    category = factories["storage.Storage"]()
    location = factories["storage.Storage"](parent=category)

    url = reverse("api:v1:storages:Storage-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == category.name
    assert len(response.data[0]["children"]) == 1
    assert response.data[0]["children"][0]["name"] == location.name


def test_logged_in_can_get_storage_tree(logged_in_api_client, db, factories):
    category = factories["storage.Storage"]()
    location = factories["storage.Storage"](parent=category)

    url = reverse("api:v1:storages:Storage-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == category.name
    assert len(response.data[0]["children"]) == 1
    assert response.data[0]["children"][0]["name"] == location.name


# ######


def test_anonymous_can_get_storages(api_client, db, factories):
    factories["storage.Storage"]()

    url = reverse("api:v1:storages:Storage-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1


def test_logged_in_can_get_storages(logged_in_api_client, db, factories):
    factories["storage.Storage"]()

    url = reverse("api:v1:storages:Storage-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1


def test_anonymous_cannot_get_storage(api_client, db, factories):
    storage_location = factories["storage.Storage"]()

    url = reverse("api:v1:storages:Storage-detail", kwargs={"pk": storage_location.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_storage(logged_in_api_client, db, factories):
    storage_location = factories["storage.Storage"]()

    url = reverse("api:v1:storages:Storage-detail", kwargs={"pk": storage_location.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == storage_location.id
    assert response.data["name"] == storage_location.name


def test_anonymous_cannot_create_storage(api_client, db):
    storage_location = {
        "name": "foobar",
    }

    url = reverse("api:v1:storages:Storage-list")
    response = api_client.post(url, storage_location)

    assert response.status_code == 401


def test_logged_in_can_create_storage(logged_in_api_client, db, factories):
    category = factories["storage.Storage"]()

    storage_location = {"name": "foobar", "parent": category.id}

    url = reverse("api:v1:storages:Storage-list")
    response = logged_in_api_client.post(url, storage_location)

    assert response.status_code == 201
    assert response.data["id"]
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_rename_storage(api_client, db, factories):
    storage_location = factories["storage.Storage"]()

    url = reverse("api:v1:storages:Storage-detail", kwargs={"pk": storage_location.id})
    response = api_client.put(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_rename_storage(logged_in_api_client, db, factories):
    category = factories["storage.Storage"]()
    storage_location = factories["storage.Storage"](parent=category)

    url = reverse("api:v1:storages:Storage-detail", kwargs={"pk": storage_location.id})
    response = logged_in_api_client.put(url, {"name": "foobar", "parent": storage_location.parent.id})

    assert response.status_code == 200
    assert response.data["id"] == storage_location.id
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_update_storage(api_client, db, factories):
    storage_location = factories["storage.Storage"]()

    url = reverse("api:v1:storages:Storage-detail", kwargs={"pk": storage_location.id})
    response = api_client.patch(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_update_storage(logged_in_api_client, db, factories):
    storage_location = factories["storage.Storage"]()

    url = reverse("api:v1:storages:Storage-detail", kwargs={"pk": storage_location.id})
    response = logged_in_api_client.patch(url, {"name": "foobar"})

    assert response.status_code == 200
    assert response.data["id"] == storage_location.id
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_delete_storage(api_client, db, factories):
    storage_location = factories["storage.Storage"]()

    url = reverse("api:v1:storages:Storage-detail", kwargs={"pk": storage_location.id})
    response = api_client.delete(url)

    assert response.status_code == 401


def test_logged_in_can_delete_storage(logged_in_api_client, db, factories):
    storage_location = factories["storage.Storage"]()

    url = reverse("api:v1:storages:Storage-detail", kwargs={"pk": storage_location.id})
    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # fetch again
    url = reverse("api:v1:storages:Storage-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0
