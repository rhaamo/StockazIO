from django.urls import reverse


def test_anonymous_can_get_categories(api_client, db):
    url = reverse("api:v1:categories:Category-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0


def test_logged_in_can_get_categories(logged_in_api_client, db):
    url = reverse("api:v1:categories:Category-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0


def test_anonymous_cannot_create_categories(api_client, db):
    url = reverse("api:v1:categories:Category-list")
    response = api_client.post(url, {"name": "test category"})

    assert response.status_code == 401

    # check again (empty)
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


def test_logged_in_can_create_categories(logged_in_api_client, db):
    url = reverse("api:v1:categories:Category-list")
    response = logged_in_api_client.post(url, {"name": "test category"})

    assert response.status_code == 201

    # check again (exists)
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "test category"


def test_logged_in_can_rename_category(logged_in_api_client, factories):
    category1 = factories["categories.Category"]()

    url = reverse("api:v1:categories:Category-detail", kwargs={"pk": category1.id})

    response = logged_in_api_client.put(url, {"name": "foobar"})

    assert response.status_code == 200
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_rename_category(api_client, factories):
    category1 = factories["categories.Category"]()

    url = reverse("api:v1:categories:Category-detail", kwargs={"pk": category1.id})

    response = api_client.put(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_delete_category(logged_in_api_client, factories):
    category1 = factories["categories.Category"]()

    url = reverse("api:v1:categories:Category-detail", kwargs={"pk": category1.id})

    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # check again (empty)
    url = reverse("api:v1:categories:Category-list")
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


def test_anonymous_cannot_delete_category(api_client, factories):
    category1 = factories["categories.Category"]()

    url = reverse("api:v1:categories:Category-detail", kwargs={"pk": category1.id})

    response = api_client.delete(url)

    assert response.status_code == 401

    # check again (has one category)
    url = reverse("api:v1:categories:Category-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
