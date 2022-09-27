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

    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


def test_logged_in_can_create_categories(logged_in_api_client, db):
    url = reverse("api:v1:categories:Category-list")
    response = logged_in_api_client.post(url, {"name": "test category"})
    
    assert response.status_code == 201

    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "test category"


# test_anonymous_cannot_rename_category
# test_logged_in_can_rename_category

# test_anonymous_cannot_delete_category
# test_logged_in_can_delete_category
