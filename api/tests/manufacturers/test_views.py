from django.urls import reverse


def test_anonymous_cannot_get_manufacturers(api_client, db):
    url = reverse("api:v1:manufacturers:Manufacturers-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_manufacturers(logged_in_api_client, db):
    url = reverse("api:v1:manufacturers:Manufacturers-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0


def test_anonymous_cannot_get_manufacturer(api_client, db, factories):
    manufacturer1 = factories["manufacturer.Manufacturer"]()

    url = reverse("api:v1:manufacturers:Manufacturers-detail", kwargs={"pk": manufacturer1.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_manufacturer(logged_in_api_client, db, factories):
    manufacturer1 = factories["manufacturer.Manufacturer"]()

    url = reverse("api:v1:manufacturers:Manufacturers-detail", kwargs={"pk": manufacturer1.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == manufacturer1.name


def test_anonymous_cannot_create_manufacturers(api_client, db):
    url = reverse("api:v1:manufacturers:Manufacturers-list")
    response = api_client.post(url, {"name": "test manufacturer"})

    assert response.status_code == 401


def test_logged_in_can_create_manufacturers(logged_in_api_client, db):
    url = reverse("api:v1:manufacturers:Manufacturers-list")
    response = logged_in_api_client.post(url, {"name": "test manufacturer", "parts_manufacturers_alias": [{"alias": "foo"}]}, format="json")

    assert response.status_code == 201

    # check again (exists)
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "test manufacturer"
    assert response.data[0]["parts_manufacturers_alias"][0]["id"]
    assert response.data[0]["parts_manufacturers_alias"][0]["alias"] == "foo"


def test_logged_in_can_rename_manufacturer(logged_in_api_client, factories):
    manufacturer1 = factories["manufacturer.Manufacturer"]()

    url = reverse("api:v1:manufacturers:Manufacturers-detail", kwargs={"pk": manufacturer1.id})

    response = logged_in_api_client.put(url, {"name": "foobar"})

    assert response.status_code == 200
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_rename_manufacturer(api_client, factories):
    manufacturer1 = factories["manufacturer.Manufacturer"]()

    url = reverse("api:v1:manufacturers:Manufacturers-detail", kwargs={"pk": manufacturer1.id})

    response = api_client.put(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_delete_manufacturer(logged_in_api_client, factories):
    manufacturer1 = factories["manufacturer.Manufacturer"]()

    url = reverse("api:v1:manufacturers:Manufacturers-detail", kwargs={"pk": manufacturer1.id})

    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # check again (empty)
    url = reverse("api:v1:manufacturers:Manufacturers-list")
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


def test_anonymous_cannot_delete_manufacturer(api_client, factories):
    manufacturer1 = factories["manufacturer.Manufacturer"]()

    url = reverse("api:v1:manufacturers:Manufacturers-detail", kwargs={"pk": manufacturer1.id})

    response = api_client.delete(url)

    assert response.status_code == 401
