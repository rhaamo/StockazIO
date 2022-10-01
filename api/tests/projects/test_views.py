from django.urls import reverse


def test_anonymous_cannot_get_projects(api_client, db, factories):
    factories["project.Project"](public=True)
    factories["project.Project"](public=False)

    url = reverse("api:v1:projects:Projects-list")
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_projects(logged_in_api_client, db, factories):
    factories["project.Project"](public=True)
    factories["project.Project"](public=False)

    url = reverse("api:v1:projects:Projects-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2


def test_anonymous_cannot_get_private_project(api_client, db, factories):
    project = factories["project.Project"](public=False)

    url = reverse("api:v1:projects:Projects-detail", kwargs={"pk": project.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_get_private_project(logged_in_api_client, db, factories):
    project = factories["project.Project"](public=False)

    url = reverse("api:v1:projects:Projects-detail", kwargs={"pk": project.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == project.id
    assert response.data["name"] == project.name


def test_logged_in_can_get_public_project(logged_in_api_client, db, factories):
    project = factories["project.Project"](public=True)

    url = reverse("api:v1:projects:Projects-detail", kwargs={"pk": project.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == project.id
    assert response.data["name"] == project.name


def test_anonymous_cannot_create_project(api_client, db):
    project = {
        "name": "foobar",
    }

    url = reverse("api:v1:projects:Projects-list")
    response = api_client.post(url, project)

    assert response.status_code == 401


def test_logged_in_can_create_project(logged_in_api_client, db):
    project = {
        "name": "foobar",
    }

    url = reverse("api:v1:projects:Projects-list")
    response = logged_in_api_client.post(url, project)

    assert response.status_code == 201
    assert response.data["id"]
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_rename_project(api_client, db, factories):
    project = factories["project.Project"]()

    url = reverse("api:v1:projects:Projects-detail", kwargs={"pk": project.id})
    response = api_client.put(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_rename_project(logged_in_api_client, db, factories):
    project = factories["project.Project"]()

    url = reverse("api:v1:projects:Projects-detail", kwargs={"pk": project.id})
    response = logged_in_api_client.put(url, {"name": "foobar"})

    assert response.status_code == 200
    assert response.data["id"] == project.id
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_update_project(api_client, db, factories):
    project = factories["project.Project"]()

    url = reverse("api:v1:projects:Projects-detail", kwargs={"pk": project.id})
    response = api_client.patch(url, {"name": "foobar"})

    assert response.status_code == 401


def test_logged_in_can_update_project(logged_in_api_client, db, factories):
    project = factories["project.Project"]()

    url = reverse("api:v1:projects:Projects-detail", kwargs={"pk": project.id})
    response = logged_in_api_client.patch(url, {"name": "foobar"})

    assert response.status_code == 201
    assert response.data["id"] == project.id
    assert response.data["name"] == "foobar"


def test_anonymous_cannot_delete_project(api_client, db, factories):
    project = factories["project.Project"]()

    url = reverse("api:v1:projects:Projects-detail", kwargs={"pk": project.id})
    response = api_client.delete(url)

    assert response.status_code == 401


def test_logged_in_can_delete_project(logged_in_api_client, db, factories):
    project = factories["project.Project"]()

    url = reverse("api:v1:projects:Projects-detail", kwargs={"pk": project.id})
    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # fetch again
    url = reverse("api:v1:projects:Projects-list")
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0


# ######


def test_anonymous_cannot_export_project_bom_csv(api_client, db, factories):
    project = factories["project.Project"]()
    factories["project.ProjectPart"](project=project, part_name="foobar")
    factories["project.ProjectPart"](project=project, part_name="bazqux")

    url = reverse("api:v1:projects:projects_export_bom_csv", kwargs={"project_id": project.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_export_project_bom_csv(logged_in_api_client, db, factories):
    project = factories["project.Project"]()
    part1 = factories["project.ProjectPart"](project=project, part_name="foobar")
    part2 = factories["project.ProjectPart"](project=project, part_name="bazqux")

    url = reverse("api:v1:projects:projects_export_bom_csv", kwargs={"project_id": project.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert "id,notes,part" in response.content.decode()
    assert part1.part_name in response.content.decode()
    assert part2.part_name in response.content.decode()


# TODO add anonymous cannot
# TODO FIXME
# def test_logged_in_can_export_project_bom_xlsx(logged_in_api_client, db, factories):
#     project = factories["project.Project"]()
#     part1 = factories["project.ProjectPart"](project=project, part_name="foobar")
#     part2 = factories["project.ProjectPart"](project=project, part_name="bazqux")

#     url = reverse("api:v1:projects:projects_export_bom_xlsx", kwargs={"project_id": project.id})
#     response = logged_in_api_client.get(url)

#     assert response.status_code == 200
#     assert "id,notes,part" in response.content.decode()


def test_anonymous_cannot_export_project_infos_txt(api_client, db, factories):
    project = factories["project.Project"]()
    factories["project.ProjectPart"](project=project, part_name="foobar")
    factories["project.ProjectPart"](project=project, part_name="bazqux")

    url = reverse("api:v1:projects:projects_export_infos", kwargs={"project_id": project.id})
    response = api_client.get(url)

    assert response.status_code == 401


def test_logged_in_can_export_project_infos_txt(logged_in_api_client, db, factories):
    project = factories["project.Project"]()
    factories["project.ProjectPart"](project=project, part_name="foobar")
    factories["project.ProjectPart"](project=project, part_name="bazqux")

    url = reverse("api:v1:projects:projects_export_infos", kwargs={"project_id": project.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert f"Name: {project.name}" in response.content.decode()


# ######

# project part add internal api:v1:projects:projects_parts
# project part add external api:v1:projects:projects_parts
# project part delete internal api:v1:projects:projects_parts
# project part delete external api:v1:projects:projects_parts

# ######

# project attachment gets api:v1:projects:projects_attachments
# project attachment create api:v1:projects:projects_attachments
# project attachment rename api:v1:projects:project_part
# project attachment update api:v1:projects:project_part
# project attachment delete api:v1:projects:project_part
