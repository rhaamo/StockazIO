from django.urls import reverse


def test_anonymous_cannot_get_labeltemplates(api_client, db):
    url = reverse("api:v1:labeltemplates:LabelTemplate-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_labeltemplates(logged_in_api_client, db):
    url = reverse("api:v1:labeltemplates:LabelTemplate-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0


def test_anonymous_cannot_create_labeltemplates(api_client, db):
    url = reverse("api:v1:labeltemplates:LabelTemplate-list")
    response = api_client.post(
        url,
        {"name": "test label", "width": 12, "height": 24, "template": "{}", "text_template": "{name} {description}"},
    )

    assert response.status_code == 401


def test_logged_in_can_create_labeltemplates(logged_in_api_client, db):
    url = reverse("api:v1:labeltemplates:LabelTemplate-list")
    response = logged_in_api_client.post(
        url,
        {"name": "test label", "width": 12, "height": 24, "template": "{}", "text_template": "{name} {description}"},
    )

    assert response.status_code == 201

    # check again (exists)
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "test label"
    assert response.data[0]["width"] == 12
    assert response.data[0]["height"] == 24
    assert response.data[0]["text_template"] == "{name} {description}"


def test_anonymous_cannot_get_labeltemplate(api_client, db, factories):
    label1 = factories["labeltemplate.LabelTemplate"]()

    url = reverse("api:v1:labeltemplates:LabelTemplate-detail", kwargs={"pk": label1.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_labeltemplate(logged_in_api_client, db, factories):
    label1 = factories["labeltemplate.LabelTemplate"]()

    url = reverse("api:v1:labeltemplates:LabelTemplate-detail", kwargs={"pk": label1.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == label1.name
    assert response.data["width"] == label1.width
    assert response.data["height"] == label1.height
    assert response.data["text_template"] == label1.text_template


def test_anonymous_cannot_update_labeltemplate(api_client, db, factories):
    label1 = factories["labeltemplate.LabelTemplate"]()

    url = reverse("api:v1:labeltemplates:LabelTemplate-detail", kwargs={"pk": label1.id})
    response = api_client.put(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_update_labeltemplate(logged_in_api_client, db, factories):
    label1 = factories["labeltemplate.LabelTemplate"]()

    url = reverse("api:v1:labeltemplates:LabelTemplate-detail", kwargs={"pk": label1.id})
    response = logged_in_api_client.put(
        url,
        {
            "name": "foobar",
            "width": label1.width,
            "height": label1.height,
            "text_template": label1.text_template,
            "template": label1.template,
        },
    )

    assert response.status_code == 200
    assert response.data["name"] == "foobar"
    assert response.data["width"] == label1.width
    assert response.data["height"] == label1.height
    assert response.data["text_template"] == label1.text_template


def test_anonymous_cannot_delete_labeltemplate(api_client, db, factories):
    label1 = factories["labeltemplate.LabelTemplate"]()

    url = reverse("api:v1:labeltemplates:LabelTemplate-detail", kwargs={"pk": label1.id})
    response = api_client.delete(url)

    assert response.status_code == 401


def test_logged_in_can_delete_labeltemplate(logged_in_api_client, db, factories):
    label1 = factories["labeltemplate.LabelTemplate"]()

    url = reverse("api:v1:labeltemplates:LabelTemplate-detail", kwargs={"pk": label1.id})
    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # check again (empty)
    url = reverse("api:v1:labeltemplates:LabelTemplate-list")
    response = logged_in_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0
