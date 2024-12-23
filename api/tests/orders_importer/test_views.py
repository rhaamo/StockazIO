from django.urls import reverse


def test_anonymous_cannot_get_orders(api_client, db):
    url = reverse("api:v1:orders_importer:OrdersImporter-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_orders(logged_in_api_client, db, factories):
    distributor = factories["distributor.Distributor"]()
    order1 = factories["OrdersImporter.Order"](vendor_db=distributor)

    url = reverse("api:v1:orders_importer:OrdersImporter-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["date"] == order1.date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    assert response.data[0]["order_number"] == order1.order_number
    assert response.data[0]["status"] == "Fetched"
    assert response.data[0]["import_state"] == 1


def test_anonymous_cannot_get_order(api_client, db, factories):
    distributor = factories["distributor.Distributor"]()
    order1 = factories["OrdersImporter.Order"](vendor_db=distributor)

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_order(logged_in_api_client, db, factories):
    distributor = factories["distributor.Distributor"]()
    order1 = factories["OrdersImporter.Order"](vendor_db=distributor)

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["date"] == order1.date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    assert response.data["order_number"] == order1.order_number
    assert response.data["status"] == "Fetched"
    assert response.data["import_state"] == 1


def test_anonymous_cannot_create_orders(api_client, db):
    url = reverse("api:v1:orders_importer:OrdersImporter-list")
    response = api_client.post(url, {"date": "2022-09-11T01:33:03Z", "order_number": "foo-bar-4242"})

    assert response.status_code == 401


def test_logged_in_can_create_order_no_item(logged_in_api_client, db, factories):
    url = reverse("api:v1:orders_importer:OrdersImporter-list")
    order = {"date": "2022-09-11T01:33:03Z", "order_number": "foo-bar-4242", "items": []}
    response = logged_in_api_client.post(url, order, format="json")

    assert response.status_code == 201

    item1 = factories["OrdersImporter.Item"](order_id=response.data["id"])

    # check again (exists)
    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": response.data["id"]})
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert response.data["date"] == "2022-09-11T01:33:03Z"
    assert response.data["order_number"] == "foo-bar-4242"
    assert response.data["status"] in ["UNKNOWN", "Unknown", "Fetched", "Imported", "Error"]
    assert response.data["import_state"] in [0, 1, 2, 99]
    assert len(response.data["items"]) == 1
    assert response.data["items"][0]["vendor_part_number"] == item1.vendor_part_number


def test_logged_in_can_create_order_with_item(logged_in_api_client, db, factories):
    url = reverse("api:v1:orders_importer:OrdersImporter-list")
    order = {
        "date": "2022-09-11T01:33:03Z",
        "order_number": "foo-bar-4242",
        "items": [
            {
                "vendor_part_number": "aaa",
                "mfr_part_number": "bbb",
                "description": "foo bar",
                "manufacturer": "baz",
            }
        ],
    }
    response = logged_in_api_client.post(url, order, format="json")

    assert response.status_code == 201

    # check again (exists)
    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": response.data["id"]})
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert response.data["date"] == "2022-09-11T01:33:03Z"
    assert response.data["order_number"] == "foo-bar-4242"
    assert response.data["status"] in ["UNKNOWN", "Unknown", "Fetched", "Imported", "Error"]
    assert response.data["import_state"] in [0, 1, 2, 99]
    assert len(response.data["items"]) == 1
    assert response.data["items"][0]["vendor_part_number"] == "aaa"
    assert response.data["items"][0]["mfr_part_number"] == "bbb"
    assert response.data["items"][0]["manufacturer"] == "baz"


def test_anonymous_cannot_edit_order(api_client, db, factories):
    distributor = factories["distributor.Distributor"]()
    order1 = factories["OrdersImporter.Order"](vendor_db=distributor)

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})
    response = api_client.put(url, {"order_number": 42})

    assert response.status_code == 401


def test_logged_in_can_edit_order(logged_in_api_client, db, factories):
    distributor = factories["distributor.Distributor"]()
    order1 = factories["OrdersImporter.Order"](vendor_db=distributor)
    order = {
        "order_number": 42,
        "date": order1.date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "items": [
            {
                "vendor_part_number": "aaa",
                "mfr_part_number": "bbb",
                "description": "foo bar",
                "manufacturer": "baz",
            }
        ],
    }

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})
    response = logged_in_api_client.put(url, order, format="json")

    assert response.status_code == 200
    assert response.data["order_number"] == "42"
    assert response.data["date"] == order1.date.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert response.data["status"] == order1.status
    assert response.data["import_state"] == order1.import_state
    assert len(response.data["items"]) == 1


def test_anonymous_cannot_patch_edit_order(api_client, db, factories):
    distributor = factories["distributor.Distributor"]()
    order1 = factories["OrdersImporter.Order"](vendor_db=distributor)

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})
    response = api_client.patch(url, {"order_number": 69})

    assert response.status_code == 401


def test_logged_in_can_patch_edit_order(logged_in_api_client, db, factories):
    distributor = factories["distributor.Distributor"]()
    order1 = factories["OrdersImporter.Order"](vendor_db=distributor)
    factories["OrdersImporter.Item"](order_id=order1.id)
    factories["OrdersImporter.Item"](order_id=order1.id)

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})
    response = logged_in_api_client.patch(url, {"order_number": 69})

    assert response.status_code == 200
    assert response.data["order_number"] == "69"
    assert response.data["date"] == order1.date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    assert response.data["status"] == order1.status
    assert response.data["import_state"] == order1.import_state
    assert len(response.data["items"]) == 2


def test_logged_in_can_delete_order(logged_in_api_client, factories):
    distributor = factories["distributor.Distributor"]()
    order1 = factories["OrdersImporter.Order"](vendor_db=distributor)

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})

    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # check again (empty)
    url = reverse("api:v1:orders_importer:OrdersImporter-list")
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


def test_anonymous_cannot_delete_order(api_client, factories):
    distributor = factories["distributor.Distributor"]()
    order1 = factories["OrdersImporter.Order"](vendor_db=distributor)

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})

    response = api_client.delete(url)

    assert response.status_code == 401


def test_anonymous_cannot_get_order_category_matchers(api_client, db):
    url = reverse("api:v1:orders_importer:CategoryMatcher-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_order_category_matchers(logged_in_api_client, db, factories):
    matcher1 = factories["OrdersImporter.CategoryMatcher"]()

    url = reverse("api:v1:orders_importer:CategoryMatcher-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["regexp"] == "capacitor"
    assert response.data[0]["category"]["id"] == matcher1.category.id


def test_anonymous_cannot_get_order_category_matcher(api_client, db, factories):
    matcher1 = factories["OrdersImporter.CategoryMatcher"]()

    url = reverse("api:v1:orders_importer:CategoryMatcher-detail", kwargs={"pk": matcher1.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_order_category_matcher(logged_in_api_client, db, factories):
    matcher1 = factories["OrdersImporter.CategoryMatcher"]()

    url = reverse("api:v1:orders_importer:CategoryMatcher-detail", kwargs={"pk": matcher1.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["regexp"] == "capacitor"
    assert response.data["category"]["id"] == matcher1.category.id


def test_anonymous_cannot_create_order_category_matchers(api_client, db):
    url = reverse("api:v1:orders_importer:CategoryMatcher-list")
    response = api_client.post(url, {"regexp": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_create_order_category_matchers(logged_in_api_client, db, factories):
    url = reverse("api:v1:orders_importer:CategoryMatcher-list")
    response = logged_in_api_client.post(url, {"regexp": "foobar"})

    assert response.status_code == 201

    # check again (exists)
    url = reverse("api:v1:orders_importer:CategoryMatcher-detail", kwargs={"pk": response.data["id"]})
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert response.data["regexp"] == "foobar"


def test_anonymous_cannot_edit_order_category_matcher(api_client, db, factories):
    matcher1 = factories["OrdersImporter.CategoryMatcher"]()

    url = reverse("api:v1:orders_importer:CategoryMatcher-detail", kwargs={"pk": matcher1.id})
    response = api_client.put(url, {"regexp": "void"})

    assert response.status_code == 401


def test_logged_in_can_edit_order_category_matcher(logged_in_api_client, db, factories):
    matcher1 = factories["OrdersImporter.CategoryMatcher"]()

    url = reverse("api:v1:orders_importer:CategoryMatcher-detail", kwargs={"pk": matcher1.id})
    response = logged_in_api_client.put(url, {"regexp": "awoo"}, format="json")

    assert response.status_code == 200
    assert response.data["regexp"] == "awoo"
    assert response.data["category"]["id"] == matcher1.category.id


def test_anonymous_cannot_patch_edit_order_category_matcher(api_client, db, factories):
    matcher1 = factories["OrdersImporter.CategoryMatcher"]()

    url = reverse("api:v1:orders_importer:CategoryMatcher-detail", kwargs={"pk": matcher1.id})
    response = api_client.patch(url, {"regexp": "42"})

    assert response.status_code == 401


def test_logged_in_can_patch_edit_order_category_matcher(logged_in_api_client, db, factories):
    matcher1 = factories["OrdersImporter.CategoryMatcher"]()

    url = reverse("api:v1:orders_importer:CategoryMatcher-detail", kwargs={"pk": matcher1.id})
    response = logged_in_api_client.patch(url, {"regexp": "bork"})

    assert response.status_code == 200
    assert response.data["regexp"] == "bork"
    assert response.data["category"]["id"] == matcher1.category.id


def test_logged_in_can_delete_order_category_matcher(logged_in_api_client, factories):
    matcher1 = factories["OrdersImporter.CategoryMatcher"]()

    url = reverse("api:v1:orders_importer:CategoryMatcher-detail", kwargs={"pk": matcher1.id})

    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # check again (empty)
    url = reverse("api:v1:orders_importer:CategoryMatcher-list")
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


def test_anonymous_cannot_delete_order_category_matcher(api_client, factories):
    matcher1 = factories["OrdersImporter.CategoryMatcher"]()

    url = reverse("api:v1:orders_importer:CategoryMatcher-detail", kwargs={"pk": matcher1.id})

    response = api_client.delete(url)

    assert response.status_code == 401


def test_anonymous_cannot_category_matcher_batch_update_update(api_client, db, factories):
    category1 = factories["categories.Category"]()

    matchers = {
        "delete": [],
        "update": [{"category": category1.id, "regexp": "foo"}, {"category": category1.id, "regexp": "bar"}],
    }

    url = reverse("api:v1:orders_importer:CategoryMatcher-Batch-Update")
    response = api_client.patch(url, matchers, format="json")

    assert response.status_code == 401


def test_logged_in_can_category_matcher_batch_update_update(logged_in_api_client, db, factories):
    category1 = factories["categories.Category"]()

    matchers = {
        "delete": [],
        "update": [{"category": category1.id, "regexp": "foo"}, {"category": category1.id, "regexp": "bar"}],
    }

    url = reverse("api:v1:orders_importer:CategoryMatcher-Batch-Update")
    response = logged_in_api_client.patch(url, matchers, format="json")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["regexp"] == "foo"
    assert response.data[0]["category"]["id"] == category1.id
    assert response.data[1]["regexp"] == "bar"
    assert response.data[1]["category"]["id"] == category1.id


def test_logged_in_can_category_matcher_batch_update_update_and_delete(logged_in_api_client, db, factories):
    category1 = factories["categories.Category"]()

    matchers = {
        "delete": [],
        "update": [{"category": category1.id, "regexp": "foo"}, {"category": category1.id, "regexp": "bar"}],
    }

    url = reverse("api:v1:orders_importer:CategoryMatcher-Batch-Update")
    response = logged_in_api_client.patch(url, matchers, format="json")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["regexp"] == "foo"
    assert response.data[0]["category"]["id"] == category1.id
    assert response.data[1]["regexp"] == "bar"
    assert response.data[1]["category"]["id"] == category1.id

    matchers = {
        "delete": [response.data[1]["id"]],
        "update": [{"id": response.data[0]["id"], "category": response.data[0]["category"]["id"], "regexp": "bar"}],
    }

    response = logged_in_api_client.patch(url, matchers, format="json")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["regexp"] == "bar"
    assert response.data[0]["category"]["id"] == category1.id


def test_anonymous_cannot_category_matcher_rematch(api_client, db, factories):
    factories["OrdersImporter.Order"]()
    factories["OrdersImporter.Order"]()
    factories["OrdersImporter.Order"]()

    url = reverse("api:v1:orders_importer:CategoryMatcher-Rematch")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_category_matcher_rematch(logged_in_api_client, db, factories):
    _ = factories["OrdersImporter.Order"]()
    _ = factories["OrdersImporter.Order"]()
    _ = factories["OrdersImporter.Order"]()

    url = reverse("api:v1:orders_importer:CategoryMatcher-Rematch")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["detail"] == "done"


def test_logged_in_can_category_matcher_rematch_no_orders(logged_in_api_client, db, factories):
    url = reverse("api:v1:orders_importer:CategoryMatcher-Rematch")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["details"] == "ok"


def test_anonymous_cannot_order_import_to_inventory(api_client, db, factories):
    order1 = factories["OrdersImporter.Order"]()

    url = reverse("api:v1:orders_importer:OrdersImporter-Import", kwargs={"pk": order1.id})
    response = api_client.post(url)

    assert response.status_code == 401


def test_logged_in_can_order_import_to_inventory(logged_in_api_client, db, factories):
    distributor = factories["distributor.Distributor"]()
    manufacturer = factories["manufacturer.Manufacturer"]()
    order1 = factories["OrdersImporter.Order"](vendor_db=distributor)
    factories["OrdersImporter.Item"](order=order1, manufacturer_db=manufacturer)
    factories["OrdersImporter.Item"](order=order1, manufacturer_db=manufacturer)
    factories["OrdersImporter.Item"](order=order1, manufacturer_db=manufacturer)

    url = reverse("api:v1:orders_importer:OrdersImporter-Import", kwargs={"pk": order1.id})
    response = logged_in_api_client.post(url)

    assert response.status_code == 200
    assert response.data["detail"] == "done"
    assert response.data["stats"]["created"] == 3
    assert response.data["stats"]["updated"] == 0
