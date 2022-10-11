from django.urls import reverse


def test_anonymous_can_get_storage_tree(api_client, db, factories):
    category = factories["storage.StorageCategory"]()
    location = factories["storage.StorageLocation"](category=category)

    url = reverse("api:v1:storages:Storage-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == category.name
    assert len(response.data[0]["storage_locations"]) == 1
    assert response.data[0]["storage_locations"][0]["name"] == location.name


def test_logged_in_can_get_storage_tree(logged_in_api_client, db, factories):
    category = factories["storage.StorageCategory"]()
    location = factories["storage.StorageLocation"](category=category)

    url = reverse("api:v1:storages:Storage-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == category.name
    assert len(response.data[0]["storage_locations"]) == 1
    assert response.data[0]["storage_locations"][0]["name"] == location.name


# ######


def test_anonymous_cannot_get_storage_categories(api_client, db, factories):
    factories["storage.StorageCategory"]()

    url = reverse("api:v1:storages:Category-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_storage_categories(logged_in_api_client, db, factories):
    factories["storage.StorageCategory"]()
    factories["storage.StorageCategory"]()

    url = reverse("api:v1:storages:Category-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2


def test_anonymous_cannot_get_storage_category(api_client, db, factories):
    storage_category = factories["storage.StorageCategory"]()

    url = reverse("api:v1:storages:Category-detail", kwargs={"pk": storage_category.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_storage_category(logged_in_api_client, db, factories):
    storage_category = factories["storage.StorageCategory"]()

    url = reverse("api:v1:storages:Category-detail", kwargs={"pk": storage_category.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == storage_category.id
    assert response.data["name"] == storage_category.name


def test_anonymous_cannot_create_storage_category(api_client, db):
    storage_category = {
        "name": "foobar",
    }

    url = reverse("api:v1:storages:Category-list")
    response = api_client.post(url, storage_category)

    assert response.status_code == 401


def test_logged_in_can_create_storage_category(logged_in_api_client, db):
    storage_category = {
        "name": "foobar",
    }

    url = reverse("api:v1:storages:Category-list")
    response = logged_in_api_client.post(url, storage_category)

    assert response.status_code == 201
    assert response.data["id"]
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_rename_storage_category(api_client, db, factories):
    storage_category = factories["storage.StorageCategory"]()

    url = reverse("api:v1:storages:Category-detail", kwargs={"pk": storage_category.id})
    response = api_client.put(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_rename_storage_category(logged_in_api_client, db, factories):
    storage_category = factories["storage.StorageCategory"]()

    url = reverse("api:v1:storages:Category-detail", kwargs={"pk": storage_category.id})
    response = logged_in_api_client.put(url, {"name": "foobar"})

    assert response.status_code == 200
    assert response.data["id"] == storage_category.id
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_update_storage_category(api_client, db, factories):
    storage_category = factories["storage.StorageCategory"]()

    url = reverse("api:v1:storages:Category-detail", kwargs={"pk": storage_category.id})
    response = api_client.patch(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_update_storage_category(logged_in_api_client, db, factories):
    storage_category = factories["storage.StorageCategory"]()

    url = reverse("api:v1:storages:Category-detail", kwargs={"pk": storage_category.id})
    response = logged_in_api_client.patch(url, {"name": "foobar"})

    assert response.status_code == 200
    assert response.data["id"] == storage_category.id
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_delete_storage_category(api_client, db, factories):
    storage_category = factories["storage.StorageCategory"]()

    url = reverse("api:v1:storages:Category-detail", kwargs={"pk": storage_category.id})
    response = api_client.delete(url)

    assert response.status_code == 401


def test_logged_in_can_delete_storage_category(logged_in_api_client, db, factories):
    storage_category = factories["storage.StorageCategory"]()

    url = reverse("api:v1:storages:Category-detail", kwargs={"pk": storage_category.id})
    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # fetch again
    url = reverse("api:v1:storages:Category-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0


# ######


def test_anonymous_cannot_get_storage_locations(api_client, db, factories):
    factories["storage.StorageLocation"]()

    url = reverse("api:v1:storages:Category-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_storage_locations(logged_in_api_client, db, factories):
    factories["storage.StorageLocation"]()

    url = reverse("api:v1:storages:Location-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1


def test_anonymous_cannot_get_storage_location(api_client, db, factories):
    storage_location = factories["storage.StorageLocation"]()

    url = reverse("api:v1:storages:Location-detail", kwargs={"pk": storage_location.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_storage_location(logged_in_api_client, db, factories):
    storage_location = factories["storage.StorageLocation"]()

    url = reverse("api:v1:storages:Location-detail", kwargs={"pk": storage_location.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == storage_location.id
    assert response.data["name"] == storage_location.name
    assert response.data["category"] == storage_location.category.id


def test_anonymous_cannot_create_storage_location(api_client, db):
    storage_location = {
        "name": "foobar",
    }

    url = reverse("api:v1:storages:Location-list")
    response = api_client.post(url, storage_location)

    assert response.status_code == 401


def test_logged_in_can_create_storage_location(logged_in_api_client, db, factories):
    category = factories["storage.StorageCategory"]()

    storage_location = {"name": "foobar", "category": category.id}

    url = reverse("api:v1:storages:Location-list")
    response = logged_in_api_client.post(url, storage_location)

    assert response.status_code == 201
    assert response.data["id"]
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_rename_storage_location(api_client, db, factories):
    storage_location = factories["storage.StorageLocation"]()

    url = reverse("api:v1:storages:Location-detail", kwargs={"pk": storage_location.id})
    response = api_client.put(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_rename_storage_location(logged_in_api_client, db, factories):
    storage_location = factories["storage.StorageLocation"]()

    url = reverse("api:v1:storages:Location-detail", kwargs={"pk": storage_location.id})
    response = logged_in_api_client.put(url, {"name": "foobar", "category": storage_location.category.id})

    assert response.status_code == 200
    assert response.data["id"] == storage_location.id
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_update_storage_location(api_client, db, factories):
    storage_location = factories["storage.StorageLocation"]()

    url = reverse("api:v1:storages:Location-detail", kwargs={"pk": storage_location.id})
    response = api_client.patch(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_update_storage_location(logged_in_api_client, db, factories):
    storage_location = factories["storage.StorageLocation"]()

    url = reverse("api:v1:storages:Location-detail", kwargs={"pk": storage_location.id})
    response = logged_in_api_client.patch(url, {"name": "foobar"})

    assert response.status_code == 200
    assert response.data["id"] == storage_location.id
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_delete_storage_location(api_client, db, factories):
    storage_location = factories["storage.StorageLocation"]()

    url = reverse("api:v1:storages:Location-detail", kwargs={"pk": storage_location.id})
    response = api_client.delete(url)

    assert response.status_code == 401


def test_logged_in_can_delete_storage_location(logged_in_api_client, db, factories):
    storage_location = factories["storage.StorageLocation"]()

    url = reverse("api:v1:storages:Location-detail", kwargs={"pk": storage_location.id})
    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # fetch again
    url = reverse("api:v1:storages:Location-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0
