from django.urls import reverse


def test_anonymous_cannot_get_orders(api_client, db):
    url = reverse("api:v1:orders_importer:OrdersImporter-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_orders(logged_in_api_client, db, factories):
    order1 = factories["OrdersImporter.Order"]()

    url = reverse("api:v1:orders_importer:OrdersImporter-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["date"] == order1.date.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert response.data[0]["order_number"] == order1.order_number
    assert response.data[0]["status"] == "Fetched"
    assert response.data[0]["import_state"] == 1


def test_anonymous_cannot_get_order(api_client, db, factories):
    order1 = factories["OrdersImporter.Order"]()

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_order(logged_in_api_client, db, factories):
    order1 = factories["OrdersImporter.Order"]()

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["date"] == order1.date.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert response.data["order_number"] == order1.order_number
    assert response.data["status"] == "Fetched"
    assert response.data["import_state"] == 1


def test_anonymous_cannot_create_orders(api_client, db):
    url = reverse("api:v1:orders_importer:OrdersImporter-list")
    response = api_client.post(url, {"date": "2022-09-11T01:33:03Z", "order_number": "foo-bar-4242"})

    assert response.status_code == 401


def test_logged_in_can_create_orders(logged_in_api_client, db, factories):
    url = reverse("api:v1:orders_importer:OrdersImporter-list")
    response = logged_in_api_client.post(url, {"date": "2022-09-11T01:33:03Z", "order_number": "foo-bar-4242"})

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


def test_anonymous_cannot_edit_order(api_client, db, factories):
    order1 = factories["OrdersImporter.Order"]()

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})
    response = api_client.put(url, {"order_number": 42})

    assert response.status_code == 401


def test_logged_in_can_edit_order(logged_in_api_client, db, factories):
    order1 = factories["OrdersImporter.Order"]()

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})
    response = logged_in_api_client.put(url, {"order_number": 42, "date": order1.date.strftime("%Y-%m-%dT%H:%M:%SZ")})

    assert response.status_code == 200
    assert response.data["order_number"] == "42"
    assert response.data["date"] == order1.date.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert response.data["status"] == order1.status
    assert response.data["import_state"] == order1.import_state


def test_anonymous_cannot_patch_edit_order(api_client, db, factories):
    order1 = factories["OrdersImporter.Order"]()

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})
    response = api_client.patch(url, {"order_number": 69})

    assert response.status_code == 401


def test_logged_in_can_patch_edit_order(logged_in_api_client, db, factories):
    order1 = factories["OrdersImporter.Order"]()

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})
    response = logged_in_api_client.patch(url, {"order_number": 69})

    assert response.status_code == 200
    assert response.data["order_number"] == "69"
    assert response.data["date"] == order1.date.strftime("%Y-%m-%dT%H:%M:%SZ")
    assert response.data["status"] == order1.status
    assert response.data["import_state"] == order1.import_state


def test_logged_in_can_delete_order(logged_in_api_client, factories):
    order1 = factories["OrdersImporter.Order"]()

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})

    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # check again (empty)
    url = reverse("api:v1:orders_importer:OrdersImporter-list")
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


def test_anonymous_cannot_delete_order(api_client, factories):
    order1 = factories["OrdersImporter.Order"]()

    url = reverse("api:v1:orders_importer:OrdersImporter-detail", kwargs={"pk": order1.id})

    response = api_client.delete(url)

    assert response.status_code == 401


# Get matchers api:v1:orders_importer:CategoryMatcher-list
# Get matcher api:v1:orders_importer:CategoryMatcher-detail
# Create matcher
# Rename matcher
# Delete matcher

# Batch update api:v1:orders_importer:category_matcher_batch_update (patch)
# Rematch api:v1:orders_importer:category_matcher_rematch
# Import to inventory api:v1:orders_importer:import_to_inventory
