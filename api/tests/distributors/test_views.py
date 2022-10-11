from django.urls import reverse


def test_anonymous_cannot_get_distributors(api_client, db):
    url = reverse("api:v1:distributors:Distributors-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_distributors(logged_in_api_client, db):
    url = reverse("api:v1:distributors:Distributors-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0


def test_anonymous_cannot_get_distributor(api_client, db, factories):
    distributor1 = factories["distributor.Distributor"]()

    url = reverse("api:v1:distributors:Distributors-detail", kwargs={"pk": distributor1.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_manufacturer(logged_in_api_client, db, factories):
    distributor1 = factories["distributor.Distributor"]()

    url = reverse("api:v1:distributors:Distributors-detail", kwargs={"pk": distributor1.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == distributor1.name


def test_anonymous_cannot_create_distributors(api_client, db):
    url = reverse("api:v1:distributors:Distributors-list")
    response = api_client.post(url, {"name": "test distributor"})

    assert response.status_code == 401


def test_logged_in_can_create_distributors(logged_in_api_client, db):
    url = reverse("api:v1:distributors:Distributors-list")
    response = logged_in_api_client.post(url, {"name": "test distributor"})

    assert response.status_code == 201

    # check again (exists)
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "test distributor"


def test_logged_in_can_rename_distributor(logged_in_api_client, factories):
    distributor1 = factories["distributor.Distributor"]()

    url = reverse("api:v1:distributors:Distributors-detail", kwargs={"pk": distributor1.id})

    response = logged_in_api_client.put(url, {"name": "foobar"})

    assert response.status_code == 200
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_rename_distributor(api_client, factories):
    distributor1 = factories["distributor.Distributor"]()

    url = reverse("api:v1:distributors:Distributors-detail", kwargs={"pk": distributor1.id})

    response = api_client.put(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_delete_distributor(logged_in_api_client, factories):
    distributor1 = factories["distributor.Distributor"]()

    url = reverse("api:v1:distributors:Distributors-detail", kwargs={"pk": distributor1.id})

    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # check again (empty)
    url = reverse("api:v1:distributors:Distributors-list")
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


def test_anonymous_cannot_delete_distributor(api_client, factories):
    distributor1 = factories["distributor.Distributor"]()

    url = reverse("api:v1:distributors:Distributors-detail", kwargs={"pk": distributor1.id})

    response = api_client.delete(url)

    assert response.status_code == 401
