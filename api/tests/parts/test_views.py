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


# ##########


def test_anonymous_cannot_create_part_attachment(api_client, db, factories, image_file):
    part = factories["part.Part"]()

    part_attachment = {"description": "foobar", "part": part.id, "picture": image_file}

    url = reverse("api:v1:parts:PartsAttachment-list", kwargs={"part_id": part.id})
    response = api_client.post(url, part_attachment)

    assert response.status_code == 401


def test_logged_in_can_create_part_attachment(logged_in_api_client, db, factories, image_file):
    part = factories["part.Part"]()

    part_attachment = {"description": "foobar", "part": part.id, "picture": image_file}

    url = reverse("api:v1:parts:PartsAttachment-list", kwargs={"part_id": part.id})
    response = logged_in_api_client.post(url, part_attachment)

    assert response.status_code == 201
    assert response.data["description"] == "foobar"
    assert response.data["part"] == part.id
    assert "png" in response.data["picture"]
    assert not response.data["file"]


def test_anonymous_cannot_rename_part_attachment(api_client, db, factories):
    part_attachment = factories["part.PartAttachment"]()

    url = reverse(
        "api:v1:parts:PartsAttachment-detail", kwargs={"pk": part_attachment.id, "part_id": part_attachment.part.id}
    )
    response = api_client.put(url, {"description": "foobar"}, format="json")

    assert response.status_code == 401


def test_logged_in_can_rename_part_attachment(logged_in_api_client, db, factories):
    part_attachment = factories["part.PartAttachment"]()

    url = reverse(
        "api:v1:parts:PartsAttachment-detail", kwargs={"pk": part_attachment.id, "part_id": part_attachment.part.id}
    )
    response = logged_in_api_client.put(url, {"description": "foobar", "part": part_attachment.part.id}, format="json")

    assert response.status_code == 200
    assert response.data["description"] == "foobar"


def test_anonymous_cannot_update_part_attachment(api_client, db, factories):
    part_attachment = factories["part.PartAttachment"]()

    url = reverse(
        "api:v1:parts:PartsAttachment-detail", kwargs={"part_id": part_attachment.part.id, "pk": part_attachment.id}
    )
    response = api_client.patch(url, {"description": "foobar"}, format="json")

    assert response.status_code == 401


def test_logged_in_can_update_part_attachment(logged_in_api_client, db, factories):
    part_attachment = factories["part.PartAttachment"]()

    url = reverse(
        "api:v1:parts:PartsAttachment-detail", kwargs={"pk": part_attachment.id, "part_id": part_attachment.part.id}
    )
    response = logged_in_api_client.patch(url, {"description": "foobar"}, format="json")

    assert response.status_code == 200
    assert response.data["description"] == "foobar"


def test_anonymous_cannot_delete_part_attachment(api_client, db, factories):
    part_attachment = factories["part.PartAttachment"]()

    url = reverse(
        "api:v1:parts:PartsAttachment-detail", kwargs={"pk": part_attachment.id, "part_id": part_attachment.part.id}
    )
    response = api_client.delete(url)

    assert response.status_code == 401


def test_logged_in_can_delete_part_attachment(logged_in_api_client, db, factories):
    part_attachment = factories["part.PartAttachment"]()

    url = reverse(
        "api:v1:parts:PartsAttachment-detail", kwargs={"pk": part_attachment.id, "part_id": part_attachment.part.id}
    )
    response = logged_in_api_client.delete(url)

    assert response.status_code == 204
    url = reverse(
        "api:v1:parts:PartsAttachment-detail", kwargs={"pk": part_attachment.id, "part_id": part_attachment.part.id}
    )
    response = logged_in_api_client.delete(url)
    assert response.status_code == 404


def test_anonymous_cannot_set_default_part_attachment(api_client, db, factories):
    part = factories["part.Part"]()
    factories["part.PartAttachment"](part=part, picture_default=False)
    part_attachment2 = factories["part.PartAttachment"](part=part, picture_default=False)

    url = reverse("api:v1:parts:parts_attachments_set_default", kwargs={"pk": part_attachment2.id, "part_id": part.id})
    response = api_client.post(url)

    assert response.status_code == 401


def test_logged_in_can_set_default_part_attachment(logged_in_api_client, db, factories):
    part = factories["part.Part"]()
    factories["part.PartAttachment"](part=part, picture_default=False)
    part_attachment2 = factories["part.PartAttachment"](part=part, picture_default=False)

    url = reverse("api:v1:parts:parts_attachments_set_default", kwargs={"pk": part_attachment2.id, "part_id": part.id})
    response = logged_in_api_client.post(url)

    assert response.status_code == 200

    # get part
    url = reverse("api:v1:parts:Part-detail", kwargs={"pk": part.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == part.name
    assert response.data["stock_qty"] == part.stock_qty
    assert response.data["category"]["id"] == part.category.id

    # Get all attachments
    has_default_part_attachment = None
    for pa in response.data["part_attachments"]:
        if pa["picture_default"]:
            has_default_part_attachment = pa
    # and validate there is one, and it is the one we wanted
    assert has_default_part_attachment
    assert has_default_part_attachment["id"] == part_attachment2.id


# ##########


def test_anonymous_cannot_autocomplete_part(api_client, db, factories):
    factories["part.Part"](name="cap-1")
    factories["part.Part"](name="cap-2")
    factories["part.Part"](name="res-1")

    url = reverse("api:v1:parts:parts_autocompletion", kwargs={"name": "cap-2"})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_autocomplete_part(logged_in_api_client, db, factories):
    factories["part.Part"](name="cap-1")
    part = factories["part.Part"](name="cap-2")
    factories["part.Part"](name="res-1")

    url = reverse("api:v1:parts:parts_autocompletion", kwargs={"name": "cap-2"})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200

    assert response.data[0]["id"] == part.id
    assert response.data[0]["name"] == part.name


# ##########


def test_anonymous_cannot_bulk_change_category(api_client, db, factories):
    category = factories["categories.Category"]()
    category1 = factories["categories.Category"](parent=category)
    category2 = factories["categories.Category"](parent=category)
    part = factories["part.Part"](category=category1)

    # change category
    url = reverse("api:v1:parts:bulk_edit_change_category")
    response = api_client.post(url, {"category": category2.id, "parts": [part.id]}, format="json")

    assert response.status_code == 401


def test_logged_in_can_bulk_change_category(logged_in_api_client, db, factories):
    category = factories["categories.Category"]()
    category1 = factories["categories.Category"](parent=category)
    category2 = factories["categories.Category"](parent=category)
    part = factories["part.Part"](category=category1)

    # fetch part initial
    url = reverse("api:v1:parts:Part-detail", kwargs={"pk": part.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == part.name
    assert response.data["category"]["id"] == category1.id

    # change category
    url = reverse("api:v1:parts:bulk_edit_change_category")
    response = logged_in_api_client.post(url, {"category": category2.id, "parts": [part.id]}, format="json")

    assert response.status_code == 200
    assert response.data["message"] == "ok"
    assert response.data["parts"] == [part.id]

    # fetch part
    url = reverse("api:v1:parts:Part-detail", kwargs={"pk": part.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == part.name
    assert response.data["category"]["id"] == category2.id


def test_anonymous_cannot_bulk_change_storage(api_client, db, factories):
    category = factories["storage.StorageCategory"]()
    storage1 = factories["storage.StorageLocation"](category=category)
    storage2 = factories["storage.StorageLocation"](category=category)
    part = factories["part.Part"](storage=storage1)

    # change storage
    url = reverse("api:v1:parts:bulk_edit_change_storage_location")
    response = api_client.post(url, {"storage_location": storage2.id, "parts": [part.id]}, format="json")

    assert response.status_code == 401


def test_logged_in_can_bulk_change_storage(logged_in_api_client, db, factories):
    category = factories["storage.StorageCategory"]()
    storage1 = factories["storage.StorageLocation"](category=category)
    storage2 = factories["storage.StorageLocation"](category=category)
    part = factories["part.Part"](storage=storage1)

    # fetch part initial
    url = reverse("api:v1:parts:Part-detail", kwargs={"pk": part.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == part.name
    assert response.data["storage"]["id"] == storage1.id

    # change storage
    url = reverse("api:v1:parts:bulk_edit_change_storage_location")
    response = logged_in_api_client.post(url, {"storage_location": storage2.id, "parts": [part.id]}, format="json")

    assert response.status_code == 200
    assert response.data["message"] == "ok"
    assert response.data["parts"] == [part.id]

    # fetch part
    url = reverse("api:v1:parts:Part-detail", kwargs={"pk": part.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == part.name
    assert response.data["storage"]["id"] == storage2.id


# ##########

# part parameter preset gets api:v1:parts:PartsParametersPreset-list
# part parameter preset create
# part parameter preset get api:v1:parts:PartsParametersPreset-detail pk
# part parameter preset rename
# part parameter preset patch
# part parameter preset delete

# ##########

# part parameters units gets api:v1:parts:PartsParametersUnit-list
# part parameters units create
# part parameters units get api:v1:parts:PartsParametersUnit-detail pk
# part parameters units rename
# part parameters units patch
# part parameters units delete

# ##########

# part public gets api:v1:parts:parts_public
# part public get api:v1:parts:parts_public_pk pk

# ##########

# part unit gets api:v1:parts:PartsParametersUnit-list
# part unit get api:v1:parts:PartsParametersUnit-detail pk
# part unit create
# part unit patch
# part unit rename
# part unit delete
