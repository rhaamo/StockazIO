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
    category = factories["storage.Storage"]()
    storage1 = factories["storage.Storage"](parent=category)
    storage2 = factories["storage.Storage"](parent=category)
    part = factories["part.Part"](storage=storage1)

    # change storage
    url = reverse("api:v1:parts:bulk_edit_change_storage_location")
    response = api_client.post(url, {"storage_location": storage2.id, "parts": [part.id]}, format="json")

    assert response.status_code == 401


def test_logged_in_can_bulk_change_storage(logged_in_api_client, db, factories):
    category = factories["storage.Storage"]()
    storage1 = factories["storage.Storage"](parent=category)
    storage2 = factories["storage.Storage"](parent=category)
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


def test_anonymous_cannot_get_part_parameter_presets(api_client, db, factories):
    ppp = factories["part.PartParameterPreset"]()
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)

    url = reverse("api:v1:parts:PartsParametersPreset-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_part_parameter_presets(logged_in_api_client, db, factories):
    ppp = factories["part.PartParameterPreset"]()
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)

    url = reverse("api:v1:parts:PartsParametersPreset-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    # response is paginated
    assert response.data["count"] == 1
    assert not response.data["next"]
    assert not response.data["previous"]
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["id"] == ppp.id
    assert response.data["results"][0]["name"] == ppp.name
    assert len(response.data["results"][0]["part_parameters_presets"]) == 2


def test_anonymous_cannot_create_part_parameter_preset(api_client, db, factories):
    unit = factories["part.ParametersUnit"]()
    ppp = {"name": "foobar", "part_parameters_presets": [{"name": "xxx1", "description": "yyy1", "unit": unit.id}]}
    url = reverse("api:v1:parts:PartsParametersPreset-list")
    response = api_client.post(url, ppp, format="json")

    assert response.status_code == 401


def test_logged_in_can_create_part_parameter_preset(logged_in_api_client, db, factories):
    unit = factories["part.ParametersUnit"]()
    ppp = {"name": "foobar", "part_parameters_presets": [{"name": "xxx1", "description": "yyy1", "unit": unit.id}]}
    url = reverse("api:v1:parts:PartsParametersPreset-list")
    response = logged_in_api_client.post(url, ppp, format="json")

    assert response.status_code == 201
    assert response.data["id"]
    assert response.data["name"] == ppp["name"]
    assert response.data["part_parameters_presets"][0]["id"]
    assert response.data["part_parameters_presets"][0]["name"] == ppp["part_parameters_presets"][0]["name"]


def test_anonymous_cannot_get_part_parameter_preset(api_client, db, factories):
    ppp = factories["part.PartParameterPreset"]()
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)

    url = reverse("api:v1:parts:PartsParametersPreset-detail", kwargs={"pk": ppp.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_part_parameter_preset(logged_in_api_client, db, factories):
    ppp = factories["part.PartParameterPreset"]()
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)

    url = reverse("api:v1:parts:PartsParametersPreset-detail", kwargs={"pk": ppp.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == ppp.id
    assert response.data["name"] == ppp.name
    assert len(response.data["part_parameters_presets"]) == 3


def test_anonymous_cannot_rename_part_parameter_preset(api_client, db, factories):
    ppp = factories["part.PartParameterPreset"]()
    pppi = factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)

    ppp_updated = {
        "name": "foobar",
        "part_parameters_presets": [
            {"id": pppi.id, "name": pppi.name, "description": pppi.description, "unit": pppi.unit.id}
        ],
    }

    url = reverse("api:v1:parts:PartsParametersPreset-detail", kwargs={"pk": ppp.id})
    response = api_client.put(url, ppp_updated, format="json")

    assert response.status_code == 401


def test_logged_in_can_rename_part_parameter_preset(logged_in_api_client, db, factories):
    ppp = factories["part.PartParameterPreset"]()
    pppi = factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)

    ppp_updated = {
        "name": "foobar",
        "part_parameters_presets": [
            {"id": pppi.id, "name": pppi.name, "description": pppi.description, "unit": pppi.unit.id}
        ],
    }

    url = reverse("api:v1:parts:PartsParametersPreset-detail", kwargs={"pk": ppp.id})
    response = logged_in_api_client.put(url, ppp_updated, format="json")

    assert response.status_code == 200
    assert response.data["id"] == ppp.id
    assert response.data["name"] == "foobar"
    assert len(response.data["part_parameters_presets"]) == 1


def test_anonymous_cannot_patch_part_parameter_preset(api_client, db, factories):
    ppp = factories["part.PartParameterPreset"]()
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)

    url = reverse("api:v1:parts:PartsParametersPreset-detail", kwargs={"pk": ppp.id})
    response = api_client.patch(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_patch_part_parameter_preset(logged_in_api_client, db, factories):
    ppp = factories["part.PartParameterPreset"]()
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)

    url = reverse("api:v1:parts:PartsParametersPreset-detail", kwargs={"pk": ppp.id})
    response = logged_in_api_client.patch(url, {"name": "foobar"})

    assert response.status_code == 200
    assert response.data["id"] == ppp.id
    assert response.data["name"] == "foobar"
    assert len(response.data["part_parameters_presets"]) == 3


def test_anonymous_cannot_delete_part_parameter_preset(api_client, db, factories):
    ppp = factories["part.PartParameterPreset"]()
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)

    url = reverse("api:v1:parts:PartsParametersPreset-detail", kwargs={"pk": ppp.id})
    response = api_client.delete(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_delete_part_parameter_preset(logged_in_api_client, db, factories):
    ppp = factories["part.PartParameterPreset"]()
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)
    factories["part.PartParameterPresetItem"](part_parameter_preset=ppp)

    url = reverse("api:v1:parts:PartsParametersPreset-detail", kwargs={"pk": ppp.id})
    response = logged_in_api_client.delete(url, {"name": "foobar"})

    assert response.status_code == 204

    # fetch again
    url = reverse("api:v1:parts:PartsParametersPreset-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    # response is paginated
    assert response.data["count"] == 0
    assert not response.data["next"]
    assert not response.data["previous"]
    assert len(response.data["results"]) == 0


# ##########


def test_anonymous_cannot_get_part_parameter_units(api_client, db, factories):
    factories["part.ParametersUnit"]()

    url = reverse("api:v1:parts:PartsParametersUnit-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_part_parameter_units(logged_in_api_client, db, factories):
    ppu = factories["part.ParametersUnit"]()

    url = reverse("api:v1:parts:PartsParametersUnit-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == ppu.id
    assert response.data[0]["name"] == ppu.name


def test_anonymous_cannot_create_part_parameter_unit(api_client, db, factories):
    ppu = {"name": "foobar", "symbol": "xxx", "description": "yyy"}
    url = reverse("api:v1:parts:PartsParametersUnit-list")
    response = api_client.post(url, ppu, format="json")

    assert response.status_code == 401


def test_logged_in_can_create_part_parameter_unit(logged_in_api_client, db, factories):
    ppu = {"name": "foobar", "symbol": "xxx", "description": "yyy"}
    url = reverse("api:v1:parts:PartsParametersUnit-list")
    response = logged_in_api_client.post(url, ppu, format="json")

    assert response.status_code == 201
    assert response.data["id"]
    assert response.data["name"] == ppu["name"]
    assert response.data["symbol"] == ppu["symbol"]


def test_anonymous_cannot_get_part_parameter_unit(api_client, db, factories):
    ppu = factories["part.ParametersUnit"]()

    url = reverse("api:v1:parts:PartsParametersUnit-detail", kwargs={"pk": ppu.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_part_parameter_unit(logged_in_api_client, db, factories):
    ppu = factories["part.ParametersUnit"]()

    url = reverse("api:v1:parts:PartsParametersUnit-detail", kwargs={"pk": ppu.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == ppu.id
    assert response.data["name"] == ppu.name


def test_anonymous_cannot_rename_part_parameter_unit(api_client, db, factories):
    ppu = factories["part.ParametersUnit"]()

    ppu_updated = {
        "name": "foobar",
    }

    url = reverse("api:v1:parts:PartsParametersUnit-detail", kwargs={"pk": ppu.id})
    response = api_client.put(url, ppu_updated, format="json")

    assert response.status_code == 401


def test_logged_in_can_rename_part_parameter_unit(logged_in_api_client, db, factories):
    ppu = factories["part.ParametersUnit"]()

    ppu_updated = {
        "name": "foobar",
    }

    url = reverse("api:v1:parts:PartsParametersUnit-detail", kwargs={"pk": ppu.id})
    response = logged_in_api_client.put(url, ppu_updated, format="json")

    assert response.status_code == 200
    assert response.data["id"] == ppu.id
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_patch_part_parameter_unit(api_client, db, factories):
    ppu = factories["part.ParametersUnit"]()

    url = reverse("api:v1:parts:PartsParametersUnit-detail", kwargs={"pk": ppu.id})
    response = api_client.patch(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_patch_part_parameter_unit(logged_in_api_client, db, factories):
    ppu = factories["part.ParametersUnit"]()

    url = reverse("api:v1:parts:PartsParametersUnit-detail", kwargs={"pk": ppu.id})
    response = logged_in_api_client.patch(url, {"name": "foobar"})

    assert response.status_code == 200
    assert response.data["id"] == ppu.id
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_delete_part_parameter_unit(api_client, db, factories):
    ppu = factories["part.ParametersUnit"]()

    url = reverse("api:v1:parts:PartsParametersUnit-detail", kwargs={"pk": ppu.id})
    response = api_client.delete(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_delete_part_parameter_unit(logged_in_api_client, db, factories):
    ppu = factories["part.ParametersUnit"]()

    url = reverse("api:v1:parts:PartsParametersUnit-detail", kwargs={"pk": ppu.id})
    response = logged_in_api_client.delete(url, {"name": "foobar"})

    assert response.status_code == 204

    # fetch again
    url = reverse("api:v1:parts:PartsParametersUnit-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0


# ##########


def test_anonymous_can_get_public_parts(api_client, db, factories):
    part = factories["part.Part"](private=False)

    url = reverse("api:v1:parts:parts_public")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == part.name
    assert response.data[0]["stock_qty"] == part.stock_qty
    assert response.data[0]["category"]["id"] == part.category.id


def test_anonymous_can_get_public_part(api_client, db, factories):
    part = factories["part.Part"](private=False)

    url = reverse("api:v1:parts:parts_public_pk", kwargs={"pk": part.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == part.name
    assert response.data["stock_qty"] == part.stock_qty
    assert response.data["category"]["id"] == part.category.id


# ##########


def test_anonymous_cannot_get_part_units(api_client, db, factories):
    factories["part.PartUnit"]()

    url = reverse("api:v1:parts:PartsUnit-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_part_units(logged_in_api_client, db, factories):
    part_unit = factories["part.PartUnit"]()

    url = reverse("api:v1:parts:PartsUnit-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == part_unit.id
    assert response.data[0]["name"] == part_unit.name


def test_anonymous_cannot_get_part_unit(api_client, db, factories):
    part_unit = factories["part.PartUnit"]()

    url = reverse("api:v1:parts:PartsUnit-detail", kwargs={"pk": part_unit.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_part_unit(logged_in_api_client, db, factories):
    part_unit = factories["part.PartUnit"]()

    url = reverse("api:v1:parts:PartsUnit-detail", kwargs={"pk": part_unit.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == part_unit.id
    assert response.data["name"] == part_unit.name


def test_anonymous_cannot_create_part_unit(api_client, db, factories):
    url = reverse("api:v1:parts:PartsUnit-list")
    part_unit = {"name": "quack", "short_name": "foo", "description": "bar"}
    response = api_client.post(url, part_unit, format="json")

    assert response.status_code == 401


def test_logged_in_can_create_part_unit(logged_in_api_client, db, factories):
    url = reverse("api:v1:parts:PartsUnit-list")
    part_unit = {"name": "quack", "short_name": "foo", "description": "bar"}
    response = logged_in_api_client.post(url, part_unit, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "quack"
    assert response.data["short_name"] == "foo"


def test_anonymous_cannot_rename_part_unit(api_client, db, factories):
    part_unit = factories["part.PartUnit"]()

    url = reverse("api:v1:parts:PartsUnit-detail", kwargs={"pk": part_unit.id})
    response = api_client.put(url, {"name": "foobar"}, format="json")

    assert response.status_code == 401


def test_logged_in_can_rename_part_unit(logged_in_api_client, db, factories):
    part_unit = factories["part.PartUnit"]()

    url = reverse("api:v1:parts:PartsUnit-detail", kwargs={"pk": part_unit.id})
    response = logged_in_api_client.put(
        url, {"name": "foobar", "short_name": part_unit.short_name, "description": part_unit.description}, format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "foobar"
    assert response.data["short_name"] == part_unit.short_name


def test_anonymous_cannot_update_part_unit(api_client, db, factories):
    part_unit = factories["part.PartUnit"]()

    url = reverse("api:v1:parts:PartsUnit-detail", kwargs={"pk": part_unit.id})
    response = api_client.patch(url, {"name": "foobar"}, format="json")

    assert response.status_code == 401


def test_logged_in_can_update_part_unit(logged_in_api_client, db, factories):
    part_unit = factories["part.PartUnit"]()

    url = reverse("api:v1:parts:PartsUnit-detail", kwargs={"pk": part_unit.id})
    response = logged_in_api_client.patch(url, {"name": "foobar", "short_name": "quack"}, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "foobar"
    assert response.data["short_name"] == "quack"


def test_anonymous_cannot_delete_part_unit(api_client, db, factories):
    part_unit = factories["part.PartUnit"]()

    url = reverse("api:v1:parts:PartsUnit-detail", kwargs={"pk": part_unit.id})
    response = api_client.delete(url)

    assert response.status_code == 401


def test_logged_in_can_delete_part_unit(logged_in_api_client, db, factories):
    part_unit = factories["part.PartUnit"]()

    url = reverse("api:v1:parts:PartsUnit-detail", kwargs={"pk": part_unit.id})
    response = logged_in_api_client.delete(url)

    assert response.status_code == 204
    url = reverse("api:v1:parts:PartsUnit-list")
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0
