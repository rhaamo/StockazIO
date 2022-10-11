import factory
from controllers.factories import registry


@registry.register
class ProjectFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    description = factory.Faker("text")
    notes = factory.Faker("text")
    ibom_url = factory.Faker("url")
    state = factory.Faker("random_element", elements=(1, 2, 3, 4, 5, 99))
    state_notes = factory.Faker("text")
    public = factory.Faker("boolean")

    class Meta:
        model = "project.Project"
        django_get_or_create = ("name",)


@registry.register
class ProjectPartFactory(factory.django.DjangoModelFactory):
    project = factory.SubFactory(ProjectFactory)
    qty = factory.Faker("random_number")
    sourced = factory.Faker("boolean")
    notes = factory.Faker("text")

    class Meta:
        model = "project.ProjectPart"
        django_get_or_create = ("notes",)


@registry.register
class ProjectAttachmentFactory(factory.django.DjangoModelFactory):
    description = factory.Faker("text", max_nb_chars=99)
    file = factory.django.ImageField()
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = "project.ProjectAttachment"
        django_get_or_create = ("description",)
