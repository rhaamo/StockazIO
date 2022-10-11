import factory
from controllers.factories import registry

@registry.register
class StorageFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    description = factory.Faker("text")
    picture = factory.django.ImageField(format="PNG", width=256, height=256)

    class Meta:
        model = "storage.Storage"
        django_get_or_create = ("name",)
