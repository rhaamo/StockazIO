from django.urls import reverse


def test_anonymous_can_get_public_projects(api_client, db, factories):
    pp = factories["project.Project"](public=True)
    factories["project.Project"](public=False)

    url = reverse("api:v1:projects:Projects-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == pp.name


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

    assert response.status_code == 404


def test_anonymous_can_get_public_project(api_client, db, factories):
    project = factories["project.Project"](public=True)

    url = reverse("api:v1:projects:Projects-detail", kwargs={"pk": project.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == project.id
    assert response.data["name"] == project.name


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

    assert response.status_code == 200
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


def test_anonymous_cannot_export_private_project_bom_csv(api_client, db, factories):
    project = factories["project.Project"](public=False)
    factories["project.ProjectPart"](project=project, part_name="foobar")
    factories["project.ProjectPart"](project=project, part_name="bazqux")

    url = reverse("api:v1:projects:projects_export_bom_csv", kwargs={"project_id": project.id})
    response = api_client.get(url)

    assert response.status_code == 404


def test_anonymous_can_export_public_project_bom_csv(api_client, db, factories):
    project = factories["project.Project"](public=True)
    part1 = factories["project.ProjectPart"](project=project, part_name="foobar")
    part2 = factories["project.ProjectPart"](project=project, part_name="bazqux")

    url = reverse("api:v1:projects:projects_export_bom_csv", kwargs={"project_id": project.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert "id,notes,part" in response.content.decode()
    assert part1.part_name in response.content.decode()
    assert part2.part_name in response.content.decode()


def test_logged_in_can_export_project_bom_csv(logged_in_api_client, db, factories):
    project = factories["project.Project"](public=False)
    part1 = factories["project.ProjectPart"](project=project, part_name="foobar")
    part2 = factories["project.ProjectPart"](project=project, part_name="bazqux")

    url = reverse("api:v1:projects:projects_export_bom_csv", kwargs={"project_id": project.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert "id,notes,part" in response.content.decode()
    assert part1.part_name in response.content.decode()
    assert part2.part_name in response.content.decode()


#


def test_anonymous_cannot_export_private_project_bom_xlsx(api_client, db, factories):
    project = factories["project.Project"](public=False)
    factories["project.ProjectPart"](project=project, part_name="foobar")
    factories["project.ProjectPart"](project=project, part_name="bazqux")

    url = reverse("api:v1:projects:projects_export_bom_xlsx", kwargs={"project_id": project.id})
    response = api_client.get(url)

    assert response.status_code == 404


def test_anonymous_can_export_public_project_bom_xlsx(api_client, db, factories):
    project = factories["project.Project"](public=True)
    factories["project.ProjectPart"](project=project, part_name="foobar")
    factories["project.ProjectPart"](project=project, part_name="bazqux")

    url = reverse("api:v1:projects:projects_export_bom_xlsx", kwargs={"project_id": project.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert response.headers["content-disposition"].startswith("attachment; filename=")


def test_logged_in_can_export_project_bom_xlsx(logged_in_api_client, db, factories):
    project = factories["project.Project"](public=False)
    factories["project.ProjectPart"](project=project, part_name="foobar")
    factories["project.ProjectPart"](project=project, part_name="bazqux")

    url = reverse("api:v1:projects:projects_export_bom_xlsx", kwargs={"project_id": project.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert response.headers["content-disposition"].startswith("attachment; filename=")


#


def test_anonymous_cannot_export_private_project_infos_txt(api_client, db, factories):
    project = factories["project.Project"](public=False)
    factories["project.ProjectPart"](project=project, part_name="foobar")
    factories["project.ProjectPart"](project=project, part_name="bazqux")

    url = reverse("api:v1:projects:projects_export_infos", kwargs={"project_id": project.id})
    response = api_client.get(url)

    assert response.status_code == 404


def test_anonymous_can_export_public_project_infos_txt(api_client, db, factories):
    project = factories["project.Project"](public=True)
    factories["project.ProjectPart"](project=project, part_name="foobar")
    factories["project.ProjectPart"](project=project, part_name="bazqux")

    url = reverse("api:v1:projects:projects_export_infos", kwargs={"project_id": project.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert f"Name: {project.name}" in response.content.decode()


def test_logged_in_can_export_project_infos_txt(logged_in_api_client, db, factories):
    project = factories["project.Project"](public=False)
    factories["project.ProjectPart"](project=project, part_name="foobar")
    factories["project.ProjectPart"](project=project, part_name="bazqux")

    url = reverse("api:v1:projects:projects_export_infos", kwargs={"project_id": project.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert f"Name: {project.name}" in response.content.decode()


# ######


def test_anonymous_cannot_add_internal_part(api_client, db, factories):
    project = factories["project.Project"](public=False)
    part = factories["part.Part"]()

    project_part = {"project": project.id, "part": part.id, "qty": 42}

    url = reverse("api:v1:projects:projects_parts", kwargs={"project_id": project.id})
    response = api_client.post(url, project_part)

    assert response.status_code == 401


def test_logged_in_can_add_internal_part(logged_in_api_client, db, factories):
    project = factories["project.Project"](public=False)
    part = factories["part.Part"]()

    project_part = {"project": project.id, "part": part.id, "qty": 42}

    url = reverse("api:v1:projects:projects_parts", kwargs={"project_id": project.id})
    response = logged_in_api_client.post(url, project_part)

    assert response.status_code == 201
    assert response.data["id"]
    assert response.data["qty"] == 42
    assert response.data["project"] == project.id


def test_anonymous_cannot_add_external_part(api_client, db, factories):
    project = factories["project.Project"](public=False)

    project_part = {"project": project.id, "part_name": "foobar", "qty": 42}

    url = reverse("api:v1:projects:projects_parts", kwargs={"project_id": project.id})
    response = api_client.post(url, project_part)

    assert response.status_code == 401


def test_logged_in_can_add_external_part(logged_in_api_client, db, factories):
    project = factories["project.Project"](public=False)

    project_part = {"project": project.id, "part_name": "foobar", "qty": 42}

    url = reverse("api:v1:projects:projects_parts", kwargs={"project_id": project.id})
    response = logged_in_api_client.post(url, project_part)

    assert response.status_code == 201
    assert response.data["id"]
    assert response.data["qty"] == 42
    assert response.data["part_name"] == "foobar"
    assert response.data["project"] == project.id


def test_anonymous_cannot_delete_internal_part(api_client, db, factories):
    project = factories["project.Project"](public=False)
    part = factories["part.Part"]()
    project_part = factories["project.ProjectPart"](part=part, project=project)

    url = reverse("api:v1:projects:project_part", kwargs={"project_id": project.id, "pk": project_part.id})
    response = api_client.delete(url)

    assert response.status_code == 401


def test_logged_in_can_delete_internal_part(logged_in_api_client, db, factories):
    project = factories["project.Project"](public=False)
    part = factories["part.Part"]()
    project_part = factories["project.ProjectPart"](part=part, project=project)

    url = reverse("api:v1:projects:project_part", kwargs={"project_id": project.id, "pk": project_part.id})

    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # fetch again
    url = reverse("api:v1:projects:Projects-detail", kwargs={"pk": project.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == project.name
    assert len(response.data["project_parts"]) == 0


def test_anonymous_cannot_delete_external_part(api_client, db, factories):
    project = factories["project.Project"](public=False)
    project_part = factories["project.ProjectPart"](part_name="foobar", project=project)

    url = reverse("api:v1:projects:project_part", kwargs={"project_id": project.id, "pk": project_part.id})

    response = api_client.delete(url)

    assert response.status_code == 401


def test_logged_in_can_delete_external_part(logged_in_api_client, db, factories):
    project = factories["project.Project"](public=False)
    project_part = factories["project.ProjectPart"](part_name="foobar", project=project)

    url = reverse("api:v1:projects:project_part", kwargs={"project_id": project.id, "pk": project_part.id})

    response = logged_in_api_client.delete(url)

    assert response.status_code == 204

    # fetch again
    url = reverse("api:v1:projects:Projects-detail", kwargs={"pk": project.id})
    response = logged_in_api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == project.name
    assert len(response.data["project_parts"]) == 0


# ######


def test_anonymous_cannot_create_project_attachment(api_client, db, factories, image_file):
    project = factories["project.Project"]()

    project_attachment = {"description": "foobar", "project": project.id, "file": image_file}

    url = reverse("api:v1:projects:projects_attachments-list", kwargs={"project_id": project.id})
    response = api_client.post(url, project_attachment)

    assert response.status_code == 401


def test_logged_in_can_create_project_attachment(logged_in_api_client, db, factories, image_file):
    project = factories["project.Project"]()

    project_attachment = {"description": "foobar", "project": project.id, "file": image_file}

    url = reverse("api:v1:projects:projects_attachments-list", kwargs={"project_id": project.id})
    response = logged_in_api_client.post(url, project_attachment)

    assert response.status_code == 201
    assert response.data["description"] == "foobar"
    assert response.data["project"] == project.id
    assert "png" in response.data["file"]


def test_anonymous_cannot_rename_project_attachment(api_client, db, factories):
    project_attachment = factories["project.ProjectAttachment"]()

    url = reverse(
        "api:v1:projects:projects_attachments-detail",
        kwargs={"pk": project_attachment.id, "project_id": project_attachment.project.id},
    )
    response = api_client.put(url, {"description": "foobar"}, format="json")

    assert response.status_code == 401


def test_logged_in_can_rename_project_attachment(logged_in_api_client, db, factories):
    project_attachment = factories["project.ProjectAttachment"]()

    url = reverse(
        "api:v1:projects:projects_attachments-detail",
        kwargs={"pk": project_attachment.id, "project_id": project_attachment.project.id},
    )
    response = logged_in_api_client.put(
        url, {"description": "foobar", "project": project_attachment.project.id}, format="json"
    )

    assert response.status_code == 200
    assert response.data["description"] == "foobar"


def test_anonymous_cannot_update_project_attachment(api_client, db, factories):
    project_attachment = factories["project.ProjectAttachment"]()

    url = reverse(
        "api:v1:projects:projects_attachments-detail",
        kwargs={"project_id": project_attachment.project.id, "pk": project_attachment.id},
    )
    response = api_client.patch(url, {"description": "foobar"}, format="json")

    assert response.status_code == 401


def test_logged_in_can_update_project_attachment(logged_in_api_client, db, factories):
    project_attachment = factories["project.ProjectAttachment"]()

    url = reverse(
        "api:v1:projects:projects_attachments-detail",
        kwargs={"pk": project_attachment.id, "project_id": project_attachment.project.id},
    )
    response = logged_in_api_client.patch(url, {"description": "foobar"}, format="json")

    assert response.status_code == 200
    assert response.data["description"] == "foobar"


def test_anonymous_cannot_delete_project_attachment(api_client, db, factories):
    project_attachment = factories["project.ProjectAttachment"]()

    url = reverse(
        "api:v1:projects:projects_attachments-detail",
        kwargs={"pk": project_attachment.id, "project_id": project_attachment.project.id},
    )
    response = api_client.delete(url)

    assert response.status_code == 401


def test_logged_in_can_delete_project_attachment(logged_in_api_client, db, factories):
    project_attachment = factories["project.ProjectAttachment"]()

    url = reverse(
        "api:v1:projects:projects_attachments-detail",
        kwargs={"pk": project_attachment.id, "project_id": project_attachment.project.id},
    )
    response = logged_in_api_client.delete(url)

    assert response.status_code == 204
    url = reverse(
        "api:v1:projects:projects_attachments-detail",
        kwargs={"pk": project_attachment.id, "project_id": project_attachment.project.id},
    )
    response = logged_in_api_client.delete(url)
    assert response.status_code == 404
