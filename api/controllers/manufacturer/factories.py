import factory
from controllers.factories import registry


@registry.register
class ManufacturerFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    address = factory.Faker("address")
    url = factory.Faker("url")
    email = factory.Faker("email")
    comment = factory.Faker("text")
    phone = factory.Faker("phone_number")
    fax = factory.Faker("phone_number")
    datasheet_url = factory.Faker("url")
    logo = factory.django.ImageField(format="PNG", width=256, height=256)
    aliases = "foo, bar, baz"

    class Meta:
        model = "manufacturer.Manufacturer"
        django_get_or_create = ("name",)
