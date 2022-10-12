from controllers import __version__
from django.conf import settings
from django.urls import reverse


def test_informations(api_client, db):
    url = reverse("api:v1:app:informations")
    response = api_client.get(url)

    assert response.status_code == 200
    assert "version" in response.data
    assert "parts_count" in response.data
    assert "categories_count" in response.data

    assert response.data["version"] == __version__
    assert response.data["parts_count"] == 0
    assert response.data["categories_count"] == 0


def test_settings(api_client, db):
    url = reverse("api:v1:app:settings")
    response = api_client.get(url)

    assert response.status_code == 200
    assert "version" in response.data
    assert "part_attachment_allowed_types" in response.data
    assert "pagination" in response.data
    assert "parts_uncategorized_count" in response.data

    assert response.data["version"] == __version__
    assert (
        response.data["part_attachment_allowed_types"]
        == settings.PART_ATTACHMENT_ALLOWED_FILES + settings.PART_ATTACHMENT_ALLOWED_IMAGES
    )
    assert response.data["pagination"] == settings.PAGINATION
    assert response.data["parts_uncategorized_count"] == 0
