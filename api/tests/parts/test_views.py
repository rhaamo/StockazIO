from django.urls import reverse


def test_anonymous_cannot_get_parts(api_client, db, factories):
    factories["part.Part"]()

    url = reverse("api:v1:parts:Part-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_parts(logged_in_api_client, db, factories):
    part = factories["part.Part"]()

    url = reverse("api:v1:parts:Part-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == part.name
    assert response.data[0]["stock_qty"] == part.stock_qty
    assert response.data[0]["category"]["id"] == part.category.id


def test_anonymous_cannot_get_part(api_client, db, factories):
    part = factories["part.Part"]()

    url = reverse("api:v1:parts:Part-detail", kwargs={"pk": part.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_part(logged_in_api_client, db, factories):
    part = factories["part.Part"]()

    url = reverse("api:v1:parts:Part-detail", kwargs={"pk": part.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == part.name
    assert response.data["stock_qty"] == part.stock_qty
    assert response.data["category"]["id"] == part.category.id


def test_anonymous_cannot_create_part(api_client, db, factories):
    url = reverse("api:v1:parts:Part-list")
    part = {"name": "quack", "stock_qty": 42}
    response = api_client.post(url, part, format="json")

    assert response.status_code == 401


def test_logged_in_can_create_part(logged_in_api_client, db, factories):
    url = reverse("api:v1:parts:Part-list")
    part = {"name": "quack", "stock_qty": 42}
    response = logged_in_api_client.post(url, part, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "quack"
    assert response.data["stock_qty"] == 42


def test_anonymous_cannot_rename_part(api_client, db, factories):
    part = factories["part.Part"]()

    url = reverse("api:v1:parts:Part-detail", kwargs={"pk": part.id})
    response = api_client.put(url, {"name": "foobar"}, format="json")

    assert response.status_code == 401


def test_logged_in_can_rename_part(logged_in_api_client, db, factories):
    part = factories["part.Part"]()

    url = reverse("api:v1:parts:Part-detail", kwargs={"pk": part.id})
    response = logged_in_api_client.put(url, {"name": "foobar"}, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "foobar"
    assert response.data["stock_qty"] == part.stock_qty


def test_anonymous_cannot_update_part(api_client, db, factories):
    part = factories["part.Part"]()

    url = reverse("api:v1:parts:Part-detail", kwargs={"pk": part.id})
    response = api_client.patch(url, {"name": "foobar"}, format="json")

    assert response.status_code == 401


def test_logged_in_can_update_part(logged_in_api_client, db, factories):
    part = factories["part.Part"]()

    url = reverse("api:v1:parts:Part-detail", kwargs={"pk": part.id})
    response = logged_in_api_client.patch(url, {"name": "foobar", "stock_qty": 69}, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "foobar"
    assert response.data["stock_qty"] == 69


def test_anonymous_cannot_delete_part(api_client, db, factories):
    part = factories["part.Part"]()

    url = reverse("api:v1:parts:Part-detail", kwargs={"pk": part.id})
    response = api_client.delete(url)

    assert response.status_code == 401


def test_logged_in_can_delete_part(logged_in_api_client, db, factories):
    part = factories["part.Part"]()

    url = reverse("api:v1:parts:Part-detail", kwargs={"pk": part.id})
    response = logged_in_api_client.delete(url)

    assert response.status_code == 204
    url = reverse("api:v1:parts:Part-list")
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


# part attachment create api:v1:parts:PartsAttachment-list part_id
# part attachment rename api:v1:parts:PartsAttachment-detail part_id pk
# part attachment patch
# part attachment delete
# part attachment set default api:v1:parts:parts_attachments_set_default part_id pk

# part autocomplete quick by name api:v1:parts:parts_autocompletion name

# part bulk change category api:v1:parts:bulk_edit_change_category
# part bulk change storage api:v1:parts:bulk_edit_change_storage_location

# part parameter preset gets api:v1:parts:PartsParametersPreset-list
# part parameter preset create
# part parameter preset get api:v1:parts:PartsParametersPreset-detail pk
# part parameter preset rename
# part parameter preset patch
# part parameter preset delete

# part parameters units gets api:v1:parts:PartsParametersUnit-list
# part parameters units create
# part parameters units get api:v1:parts:PartsParametersUnit-detail pk
# part parameters units rename
# part parameters units patch
# part parameters units delete

# part public gets api:v1:parts:parts_public
# part public get api:v1:parts:parts_public_pk pk

# part unit gets api:v1:parts:PartsParametersUnit-list
# part unit get api:v1:parts:PartsParametersUnit-detail pk
# part unit create
# part unit patch
# part unit rename
# part unit delete
