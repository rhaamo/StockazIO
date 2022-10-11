from django.urls import reverse


def test_anonymous_cannot_get_footprints_tree(api_client, db):
    url = reverse("api:v1:footprints:FootprintsTree-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_footprints_tree(logged_in_api_client, db, factories):
    footprint1 = factories["footprints.Footprint"]()

    url = reverse("api:v1:footprints:FootprintsTree-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == footprint1.category.name
    assert response.data[0]["footprint_set"][0]["name"] == footprint1.name


def test_anonymous_cannot_get_footprints(api_client, db):
    url = reverse("api:v1:footprints:Footprints-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_footprints(logged_in_api_client, db, factories):
    footprint1 = factories["footprints.Footprint"]()

    url = reverse("api:v1:footprints:Footprints-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == footprint1.name


def test_anonymous_cannot_get_footprints_with_category_id(api_client, db):
    url = reverse("api:v1:footprints:Footprints-list") + "?category_id=1"
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_footprints_with_category_id(logged_in_api_client, db, factories):
    footprint1 = factories["footprints.Footprint"]()
    _ = factories["footprints.Footprint"]()

    url = reverse("api:v1:footprints:Footprints-list") + f"?category_id={footprint1.category.id}"
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == footprint1.name


def test_anonymous_cannot_rename_footprint(api_client, db, factories):
    footprint1 = factories["footprints.Footprint"]()

    url = reverse("api:v1:footprints:Footprints-detail", kwargs={"pk": footprint1.id})
    response = api_client.put(url, {"name": "foobar", "category": footprint1.category.id})

    assert response.status_code == 401


def test_logged_in_can_rename_footprint(logged_in_api_client, db, factories):
    footprint1 = factories["footprints.Footprint"]()

    url = reverse("api:v1:footprints:Footprints-detail", kwargs={"pk": footprint1.id})
    response = logged_in_api_client.put(url, {"name": "foobar", "category": footprint1.category.id})

    assert response.status_code == 200
    assert response.data["name"] == "foobar"
    assert response.data["id"] == footprint1.id


def test_anonymous_cannot_delete_footprint(api_client, factories):
    footprint1 = factories["footprints.Footprint"]()

    url = reverse("api:v1:footprints:Footprints-detail", kwargs={"pk": footprint1.id})
    response = api_client.delete(url)

    assert response.status_code == 401


def test_logged_in_can_delete_footprint(logged_in_api_client, factories):
    footprint1 = factories["footprints.Footprint"]()

    url = reverse("api:v1:footprints:Footprints-detail", kwargs={"pk": footprint1.id})

    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # check again (empty)
    url = reverse("api:v1:footprints:Footprints-list")
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


def test_anonymous_cannot_get_categories(api_client, db):
    url = reverse("api:v1:footprints:FootprintCategories-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_categories(logged_in_api_client, db, factories):
    category1 = factories["footprints.FootprintCategory"]()

    url = reverse("api:v1:footprints:FootprintCategories-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == category1.name


def test_anonymous_cannot_rename_category(api_client, db, factories):
    category1 = factories["footprints.FootprintCategory"]()

    url = reverse("api:v1:footprints:FootprintCategories-detail", kwargs={"pk": category1.id})
    response = api_client.put(url, {"name": "foobar", "category": category1.id})

    assert response.status_code == 401


def test_logged_in_can_rename_category(logged_in_api_client, db, factories):
    category1 = factories["footprints.FootprintCategory"]()

    url = reverse("api:v1:footprints:FootprintCategories-detail", kwargs={"pk": category1.id})
    response = logged_in_api_client.put(url, {"name": "foobar", "category": category1.id})

    assert response.status_code == 200
    assert response.data["name"] == "foobar"
    assert response.data["id"] == category1.id


def test_anonymous_cannot_delete_category(api_client, factories):
    category1 = factories["footprints.FootprintCategory"]()

    url = reverse("api:v1:footprints:FootprintCategories-detail", kwargs={"pk": category1.id})
    response = api_client.delete(url)

    assert response.status_code == 401


def test_logged_in_can_delete_category(logged_in_api_client, factories):
    category1 = factories["footprints.FootprintCategory"]()

    url = reverse("api:v1:footprints:FootprintCategories-detail", kwargs={"pk": category1.id})

    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # check again (empty)
    url = reverse("api:v1:footprints:FootprintCategories-list")
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0
