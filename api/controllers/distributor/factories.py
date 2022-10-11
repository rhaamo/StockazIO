import factory
from controllers.factories import registry


@registry.register
class DistributorFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    address = factory.Faker("address")
    url = factory.Faker("url")
    email = factory.Faker("email")
    comment = factory.Faker("text")
    phone = factory.Faker("phone_number")
    fax = factory.Faker("phone_number")
    datasheet_url = factory.Faker("url")

    class Meta:
        model = "distributor.Distributor"
        django_get_or_create = ("name",)
