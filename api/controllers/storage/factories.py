import factory
from controllers.factories import registry


@registry.register
class StorageCategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = "storage.StorageCategory"
        django_get_or_create = ("name",)


@registry.register
class StorageLocationFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    category = factory.SubFactory(StorageCategoryFactory)
    description = factory.Faker("text")
    picture = factory.django.ImageField(format="PNG", width=256, height=256)

    class Meta:
        model = "storage.StorageLocation"
        django_get_or_create = ("name",)
