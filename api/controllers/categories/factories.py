import factory

from controllers.factories import registry


@registry.register
class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = "categories.Category"
        django_get_or_create = ("name",)
