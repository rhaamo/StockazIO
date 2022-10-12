import factory

from controllers.factories import registry


@registry.register
class FootprintCategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    description = factory.Faker("text")

    class Meta:
        model = "footprints.FootprintCategory"
        django_get_or_create = ("name",)


@registry.register
class FootprintFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    description = factory.Faker("text")
    picture = factory.django.ImageField(format="PNG", width=256, height=256)
    category = factory.SubFactory(FootprintCategoryFactory)

    class Meta:
        model = "footprints.Footprint"
        django_get_or_create = ("name",)
